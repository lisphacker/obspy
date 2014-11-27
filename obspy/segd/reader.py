'''
Functions and classes for reading a SEGD file.

@author: Gautham Ganapathy
@contact: gautham@lisphacker.org
'''

GENERAL_HEADER1_SIZE = 32
GENERAL_HEADER2_SIZE = 32
GENERAL_HEADERN_SIZE = 32

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

        # Read general headers
        segd.file_headers.general_header1 = self.read_general_header1()
        if segd.file_headers.general_header1.num_additional_general_headers >= 1:
            segd.file_headers.general_header2 = self.read_general_header2()
        for i in xrange(1, segd.file_headers.general_header1.num_additional_general_headers):
            segd.file_headers.general_headerN.append(self.read_general_headerN())

        # Read channel set headers
        num_channel_sets = segd.get_num_channel_sets()
        print num_channel_sets
        
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
