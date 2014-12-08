'''
Entry points for the segd module.

@author: Gautham Ganapathy
@contact: gautham@lisphacker.org
'''

from obspy.segd.reader import SEGDReader
from obspy import Stream, Trace
from obspy.core import AttribDict

def isSEGD(filename):
    '''
    Checks whether or not the given file is a SEG D file.

    @param filename: File to be checked
    @type  filename: str

    @return: Flag indicating if the file is a SEG D file or not.
    @rtype bool
    '''

    with open(filename) as f:
        reader = SEGDReader(f, headers_only = True)
        segd = reader.read()
        if segd.file_headers.general_header1.format_code == 8058:
            return True

    return False


def readSEGD(filename, headers_only = False, byte_order = False,
             textual_header_encoding = None, unpack_trace_headers = False,
             **kw_args):
    '''
    as
    
    '''

    stream = Stream()
    stream.stats = AttribDict()
    
    with open(filename) as f:
        reader = SEGDReader(f, headers_only = headers_only)
        segd = reader.read()

    #print segd.file_headers.general_header1
    #print segd.file_headers.general_header2
    #print segd.file_headers.general_headerN[0]
    #print 'num ch sets', len(segd.file_headers.channel_set_headers)
    #print segd.file_headers.channel_set_headers[0]
    print segd.file_headers.extended_headers[0]
    print segd.file_headers.extended_headers[1]
    print segd.file_headers.extended_headers[2]
    
    return stream
    

    
def writeSEGD(stream, filename, data_encoding = None, byte_order = None,
              textual_header_encoding = None, **kwargs):
    '''
    '''

    pass
