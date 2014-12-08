'''
Functions and classes for reading a SEGD file.

@author: Gautham Ganapathy
@contact: gautham@lisphacker.org
'''

GENERAL_HEADER1_SIZE = 32
GENERAL_HEADER2_SIZE = 32
GENERAL_HEADERN_SIZE = 32
CHANNEL_SET_HEADER_SIZE = 32
EXTENDED_HEADER_SIZE = 32
GENERAL_TRACE_HEADER_SIZE = 20
TRACE_HEADER_EXTENSION_SIZE = 32

import os
import numpy as np
from obspy.segd.segd import *
from obspy.segd.bcd import *

class SEGDReader(object):
    def __init__(self, file_obj, headers_only = False):
        assert file_obj is not None

        self.file_obj = file_obj
        self.headers_only = headers_only
        
    def read(self):
        segd = SEGD()

        ### Read file headers ###

        fh = segd.file_headers

        # Read general file headers
        fh.general_header1 = self.read_general_header1()
        if fh.general_header1.num_additional_general_headers >= 1:
            fh.general_header2 = self.read_general_header2()
        for i in xrange(1, fh.general_header1.num_additional_general_headers):
            fh.general_headerN.append(self.read_general_headerN())

        # Read channel set headers
        num_channel_sets = segd.get_num_channel_sets()
        for i in xrange(num_channel_sets):
            fh.channel_set_headers.append(self.read_channel_set_header())

        # Read extended headers
        for i in xrange(segd.file_headers.general_header1.num_extended_headers):
            ext_hdr = self.read_extended_header()
            fh.extended_headers.append(ext_hdr)

            for i in xrange(1, ext_hdr.total_number_of_32byte_blocks):
                read_bytes(self.file_obj, EXTENDED_HEADER_SIZE)

        ### Read traces ###
        for i in xrange(segd.get_num_traces()):
            trace = Trace()
            trace.trace_headers.general_trace_header = self.read_general_trace_header()

            nTHEs = trace.trace_headers.general_trace_header.number_of_THEs
            trace.trace_headers.trace_header_extensions = [None] * nTHEs
            for j in xrange(nTHEs):
                the = self.read_trace_header_extension(j + 1)
                trace.trace_headers.trace_header_extensions[j] = the

            trace_len_bytes = segd.get_samples_per_trace(i) * 4

            if self.headers_only:
                self.file_obj.seek(trace_len_bytes, os.SEEK_CUR)
            else:
                raise 'Trace data read not supported yet'

            segd.traces.append(trace)
        
        return segd

    def read_general_header1(self):
        byte_buffer = read_bytes(self.file_obj, GENERAL_HEADER1_SIZE)
        genhdr1 = GeneralHeader1()
        genhdr1.populate_from_buffer(byte_buffer)
        return genhdr1
    
    def read_general_header2(self):
        byte_buffer = read_bytes(self.file_obj, GENERAL_HEADER2_SIZE)
        genhdr2 = GeneralHeader2()
        genhdr2.populate_from_buffer(byte_buffer)
        return genhdr2
    
    def read_general_headerN(self):
        byte_buffer = read_bytes(self.file_obj, GENERAL_HEADERN_SIZE)
        genhdrN = GeneralHeaderN()
        genhdrN.populate_from_buffer(byte_buffer)
        return genhdrN

    def read_channel_set_header(self):
        byte_buffer = read_bytes(self.file_obj, CHANNEL_SET_HEADER_SIZE)
        chsethdr = ChannelSetHeader()
        chsethdr.populate_from_buffer(byte_buffer)
        return chsethdr

    def read_extended_header(self):
        byte_buffer = read_bytes(self.file_obj, EXTENDED_HEADER_SIZE)
        exthdr = ExtendedHeader()
        exthdr.populate_from_buffer(byte_buffer)
        return exthdr
    
    def read_general_trace_header(self):
        byte_buffer = read_bytes(self.file_obj, GENERAL_TRACE_HEADER_SIZE)
        gentrchdr = GeneralTraceHeader()
        gentrchdr.populate_from_buffer(byte_buffer)
        return gentrchdr
    
    def read_trace_header_extension(self, idx):
        byte_buffer = read_bytes(self.file_obj, TRACE_HEADER_EXTENSION_SIZE)
        if idx == 1:
            the = TraceHeaderExtension1()
        elif idx == 2:
            the = TraceHeaderExtension2()
        else:
            the = TraceHeaderExtension2()
        the.populate_from_buffer(byte_buffer)
        return the