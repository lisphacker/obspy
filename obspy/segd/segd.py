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

class ChannelSetHeader(AttributeEnumerable):
    def __init__(self):
        self.scan_type = 0
        self.channel_set = 0
        self.start_time = 0
        self.end_time = 0
        self.mp_factor = 1
        self.num_channels = 0
        self.channel_type = 0
        self.num_sub_scans = 0
        self.gain_control_method = 0
        self.alias_filter_frequency = 0
        self.alias_filter_slope = 0
        self.low_cut_filter_frequency = 0
        self.low_cut_filter_slope = 0
        self.first_notch_frqeuency = 0
        self.second_notch_frqeuency = 0
        self.third_notch_frqeuency = 0
        self.extended_channel_set = 0
        self.extended_header_flag = 0
        self.num_trace_header_extensions = 0
        self.vertical_stack = 0
        self.streamer_cable_number = 0
        self.array_forming = 0

    def populate_from_buffer(self, byte_buffer):
        nibble_buffer = bytes_to_nibbles(byte_buffer)
        
        self.scan_type = read_bcd(nibble_buffer[0:2])
        self.channel_set = -1 if ffff(nibble_buffer[0:2]) else read_bcd(nibble_buffer[0:2])
        self.start_time = read_uint_from_bytes(byte_buffer[2:4])
        self.end_time = read_uint_from_bytes(byte_buffer[4:6])
        self.mp_factor = read_q13_from_bytes(byte_buffer[6:8])
        self.num_channels = read_bcd(nibble_buffer[16:20])
        self.channel_type = int(nibble_buffer[20])
        self.num_sub_scans = int(nibble_buffer[22])
        self.gain_control_method = int(nibble_buffer[23])
        self.alias_filter_frequency = read_bcd(nibble_buffer[24:28])
        self.alias_filter_slope = read_bcd(nibble_buffer[29:32])
        self.low_cut_filter_frequency = read_bcd(nibble_buffer[32:36])
        self.low_cut_filter_slope = read_bcd(nibble_buffer[37:40])
        self.first_notch_frqeuency = read_bcd(nibble_buffer[40:44])
        self.second_notch_frqeuency = read_bcd(nibble_buffer[44:48])
        self.third_notch_frqeuency = read_bcd(nibble_buffer[48:52])
        self.extended_channel_set = read_uint_from_bytes(byte_buffer[26:28])
        self.extended_header_flag = int(nibble_buffer[56])
        self.num_trace_header_extensions = int(nibble_buffer[57])
        self.vertical_stack = int(byte_buffer[29])
        self.streamer_cable_number = int(byte_buffer[30])
        self.array_forming = int(byte_buffer[31])

    def __repr__(self):
        return '<Channel set header {1} - {{{0}}}>'.format(self.enumerate_attributes(), self.channel_set)

class ExtendedHeader(AttributeEnumerable):
    def __init__(self):
        self.seg_manufacturing_code = 0
        self.manufacturing_sponsorship_code = 0
        self.content_type = 0
        self.content_version = 0
        self.content_compat_version = 0
        self.total_number_of_32byte_blocks = 0

    def populate_from_buffer(self, byte_buffer):
        nibble_buffer = bytes_to_nibbles(byte_buffer)

        self.seg_manufacturing_code = read_uint_from_bytes(byte_buffer[0:1])
        self.manufacturing_sponsorship_code = read_uint_from_bytes(byte_buffer[1:3])
        self.content_type = read_uint_from_bytes(byte_buffer[3:4])
        self.content_version = read_uint_from_bytes(byte_buffer[4:5])
        self.content_compat_version = read_bcd(nibble_buffer[20:21])
        self.total_number_of_32byte_blocks = read_uint_from_bytes(byte_buffer[6:8])

    def __repr__(self):
        return '<Extended header - {{{0}}}>'.format(self.enumerate_attributes())


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

class GeneralTraceHeader(AttributeEnumerable):
    def __init__(self):
        self.file_number = 0
        self.scan_type_number = 0
        self.channel_set_number = 0
        self.trace_number = 0
        self.first_timing_word = 0
        self.number_of_THEs = 0
        self.sample_skew = 0
        self.trace_edit = 0
        self.time_break_window = 0
        self.extended_channel_set_number = 0
        self.extended_file_number = 0
        
    def populate_from_buffer(self, byte_buffer):
        nibble_buffer = bytes_to_nibbles(byte_buffer)

        self.file_number = read_bcd(nibble_buffer[0:4])
        self.scan_type_number = read_bcd(nibble_buffer[5:6])
        self.channel_set_number = read_bcd(nibble_buffer[6:8])
        self.trace_number = read_bcd(nibble_buffer[8:12])
        self.first_timing_word = read_uint_from_bytes(byte_buffer[6:9])
        self.number_of_THEs = read_bcd(nibble_buffer[18:20])
        self.sample_skew = read_uint_from_bytes(byte_buffer[10:11])
        self.trace_edit = read_uint_from_bytes(byte_buffer[11:12])
        self.time_break_window = read_uint_from_bytes(byte_buffer[12:15])
        self.extended_channel_set_number = read_uint_from_bytes(byte_buffer[15:17])
        self.extended_file_number = read_uint_from_bytes(byte_buffer[17:20])

    def __repr__(self):
        return '<General trace header {1} - {{{0}}}>'.format(self.enumerate_attributes(), self.trace_number)

class TraceHeaderExtension(AttributeEnumerable):
    def __init__(self):
        pass
    
    def populate_from_buffer(self, byte_buffer):
        pass

    def __repr__(self):
        return '<Trace header extension>'

class TraceHeaderExtension1(TraceHeaderExtension):
    def __init__(self):
        TraceHeaderExtension.__init__(self)
        
        self.receiver_line_number = 0
        self.receiver_point_number = 0
        self.receiver_point_index = 0
        self.samples_per_trace = 0
        self.extended_receiver_line_number = 0
        self.extended_receiver_point_number = 0
        self.sensor_type = 0
    
    def populate_from_buffer(self, byte_buffer):
        self.receiver_line_number = read_uint_from_bytes(byte_buffer[0:3])
        self.receiver_point_number = read_uint_from_bytes(byte_buffer[3:6])
        self.receiver_point_index = read_uint_from_bytes(byte_buffer[6:7])
        self.samples_per_trace = read_uint_from_bytes(byte_buffer[7:10])
        self.extended_receiver_line_number = float(read_uint_from_bytes(byte_buffer[10:15])) / 65535.0
        self.extended_receiver_point_number = float(read_uint_from_bytes(byte_buffer[15:20])) / 65535.0
        self.sensor_type = read_uint_from_bytes(byte_buffer[20:21])
    
    def __repr__(self):
        return '<Trace header extension 1 - {{{0}}}>'.format(self.enumerate_attributes())


class TraceHeaderExtension2(TraceHeaderExtension):
    def __init__(self):
        TraceHeaderExtension.__init__(self)

        self.easting = 0
        self.northing = 0
        self.elevation = 0
        self.sensor_orientation = 0
    
    def populate_from_buffer(self, byte_buffer):
        nibble_buffer = bytes_to_nibbles(byte_buffer)

        self.easting = read_double(byte_buffer[0:8])
        self.northing = read_double(byte_buffer[8:16])
        self.elevation = read_float(byte_buffer[16:20])
        self.sensor_orientation = read_bcd(nibble_buffer[49:50])
                                   
    def __repr__(self):
        return '<Trace header extension 2 - {{{0}}}>'.format(self.enumerate_attributes())

class TraceHeaders(object):
    def __init__(self):
        self.general_trace_header = GeneralTraceHeader()
        self.trace_header_extensions = []
    
class Trace(object):
    def __init__(self):
        self.trace_headers = TraceHeaders()
        self.data = None

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

    def get_num_channels(self):
        return self.get_num_traces()
    
    def get_num_traces(self):
        return reduce(lambda x, y: x + y, [ch_set_hdr.num_channels for ch_set_hdr in self.file_headers.channel_set_headers])

    def get_sample_interval(self, trace_idx):
        sample_microsecs = (self.file_headers.general_header1.base_scan_interval * 1000) / 16
        return float(sample_microsecs) * 0.000001
        
    def get_samples_per_trace(self, trace_idx):
        the1 = self.traces[trace_idx].trace_header_extensions[0]
        
        if the1 is not None:
            return the1.samples_per_trace
        else:
            fh = self.file_headers
            if fh.general_header1.record_length == 1665:
                trace_time = float(fh.general_header2.record_length) * .001
            else:
                trace_time = float(fh.general_header1.record_length) * .5 * 1.024

            sample_interval = self.get_sample_interval(trace_idx)

            return int(trace_time / sample_interval + 0.5) + 1

    def __iter__(self):
        return iter(self.traces)
