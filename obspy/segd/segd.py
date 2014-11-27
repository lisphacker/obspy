'''
Classes for managing data in a SEGD file.

@author: Gautham Ganapathy
@contact: gautham@lisphacker.org
'''

from obspy.segd.bcd import *

class AttributeEnumerable(object):
    def enumerate_attributes(self):
        keys = self.__dict__.keys()
        keys.sort()
        return ', '.join(['{0}: {1}'.format(k, self.__dict__[k]) for k in keys])
            
    
class GeneralHeader1(AttributeEnumerable):
    def __init__(self):
        self.file_number = -1
        self.format_code = 0
        self.year2 = 0
        self.num_additional_general_headers = 1
        self.julian_day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.manufacturers_code = 0
        self.base_scan_interval = 0
        self.polarity = 0
        self.record_type = 0
        self.record_length = 0
        self.scan_types_per_record = 0
        self.channel_sets_per_scan_type = 0
        self.sample_skew_length = 0
        self.num_extended_headers = 0
        self.num_external_headers = 0

    def populate_from_buffer(self, byte_buffer):
        nibble_buffer = bytes_to_nibbles(byte_buffer)
        
        self.file_number = -1 if ffff(nibble_buffer[0:4]) else read_bcd(nibble_buffer[0:4])
        self.format_code = read_bcd(nibble_buffer[4:8])
        self.year2 = read_bcd(nibble_buffer[20:22])
        self.num_additional_general_headers = int(nibble_buffer[22])
        self.julian_day = read_bcd(nibble_buffer[23:26])
        self.hour = read_bcd(nibble_buffer[26:28])
        self.minute = read_bcd(nibble_buffer[28:30])
        self.second = read_bcd(nibble_buffer[30:32])
        self.manufacturers_code = read_bcd(nibble_buffer[32:34])
        self.base_scan_interval = read_bcd(nibble_buffer[44:46])
        self.polarity = int(nibble_buffer[46])
        self.record_type = int(nibble_buffer[50])
        self.record_length = read_bcd(nibble_buffer[51:54])
        self.scan_types_per_record = read_bcd(nibble_buffer[54:56])
        self.channel_sets_per_scan_type = -1 if ffff(nibble_buffer[56:58]) else read_bcd(nibble_buffer[56:58])
        self.sample_skew_length = read_bcd(nibble_buffer[58:60])
        self.num_extended_headers = -1 if ffff(nibble_buffer[60:62]) else read_bcd(nibble_buffer[60:62])
        self.num_external_headers = -1 if ffff(nibble_buffer[62:64]) else read_bcd(nibble_buffer[62:64])

    def __repr__(self):
        return '<General Header 1 - {{{0}}}>'.format(self.enumerate_attributes())

class GeneralHeader2(AttributeEnumerable):
    def __init__(self):
        self.file_number = 0
        self.channel_sets_per_scan_type = 0
        self.num_extended_headers = 0
        self.num_external_headers = 0
        self.segd_major_version = 0
        self.segd_minor_version = 0
        self.num_general_trailers = 0
        self.record_length = 0
        self.block_number = 0
        self.sequence_number = 0

    def populate_from_buffer(self, byte_buffer):
        self.file_number = read_uint_from_bytes(byte_buffer[0:3])
        self.channel_sets_per_scan_type = read_uint_from_bytes(byte_buffer[3:5])
        self.num_extended_headers = read_uint_from_bytes(byte_buffer[5:7])
        self.num_external_headers = read_uint_from_bytes(byte_buffer[7:9])
        self.segd_major_version = int(byte_buffer[10])
        self.segd_minor_version = int(byte_buffer[11])
        self.num_general_trailers = read_uint_from_bytes(byte_buffer[12:14])
        self.record_length = read_uint_from_bytes(byte_buffer[14:17])
        self.block_number = int(byte_buffer[18])
        self.sequence_number = read_uint_from_bytes(byte_buffer[20:22])

    def __repr__(self):
        return '<General Header 2 - {{{0}}}>'.format(self.enumerate_attributes())
    
class GeneralHeaderN(AttributeEnumerable):
    def __init__(self):
        self.file_number = 0
        self.source_line_number_int = 0
        self.source_line_number_frac = 0
        self.source_point_number_int = 0
        self.source_point_number_frac = 0
        self.source_point_index = 0
        self.phase_control = 0
        self.vibrator_type = 0
        self.phase_angle = 0
        self.block_number = 0
        self.source_set_number = 0

    def populate_from_buffer(self, byte_buffer):
        self.file_number = read_uint_from_bytes(byte_buffer[0:3])
        self.source_line_number_int = read_sint_from_bytes(byte_buffer[3:6])
        self.source_line_number_frac = read_uint_from_bytes(byte_buffer[6:8])
        self.source_point_number_int = read_sint_from_bytes(byte_buffer[8:11])
        self.source_point_number_frac = read_uint_from_bytes(byte_buffer[11:13])
        self.source_point_index = int(byte_buffer[13])
        self.phase_control = int(byte_buffer[14])
        self.vibrator_type = int(byte_buffer[15])
        self.phase_angle = read_sint_from_bytes(byte_buffer[16:18])
        self.block_number = int(byte_buffer[18])
        self.source_set_number = int(byte_buffer[19])

    def __repr__(self):
        return '<General Header {1} - {{{0}}}>'.format(self.enumerate_attributes(), self.block_number)

class ChannelSetHeader(object):
    pass

class ExtendedHeader(object):
    pass

class ExternalHeader(object):
    pass

class FileHeaders(object):
    def __init__(self):
        self.general_header1 = None
        self.general_header2 = None
        self.general_headerN = []

        self.channel_set_headers = []
        self.extended_headers = []
        self.external_headers = []

class TraceHeader(object):
    pass

class TraceHeaderExtension(object):
    pass

class TraceHeaderExtension1(TraceHeaderExtension):
    pass

class TraceHeaders(object):
    pass
    
class Trace(object):
    pass

class SEGDException(Exception):
    pass

class SEGD(object):
    def __init__(self):
        self.file_headers = FileHeaders()
        self.traces = []

    def get_num_channel_sets(self):
        fh = self.file_headers
        
        if fh.general_header1 is None:
            raise SEGDException('General header 1 missing')
        channel_sets_per_scan_type = fh.general_header1.channel_sets_per_scan_type
        scan_types_per_record = fh.general_header1.scan_types_per_record
        if channel_sets_per_scan_type >= 0:
            return scan_types_per_record * channel_sets_per_scan_type

        if fh.general_header2 is None:
            raise SEGDException('General header 2 missing')
        channel_sets_per_scan_type = fh.general_header2.channel_sets_per_scan_type
        if channel_sets_per_scan_type >= 0:
            return scan_types_per_record * channel_sets_per_scan_type

        for gen_hdr in fh.general_headerN:
            channel_sets_per_scan_type = gen_hdr.channel_sets_per_scan_type
            if channel_sets_per_scan_type >= 0:
                return scan_types_per_record * channel_sets_per_scan_type

        raise SEGDException('Unable to compute number of channel sets')

        
             
    def __iter__(self):
        return iter(self.traces)
