'''
Entry points for the segd module.

@author: Gautham Ganapathy
@organization: Halliburton (http://www.halliburton.com)
@contact: gautham@lisphacker.org
'''

def isSEGD(filename):
    '''
    Checks whether or not the given file is a SEG D file.

    @param filename: File to be checked
    @type  filename: str

    @return: Flag indicating if the file is a SEG D file or not.
    @rtype bool
    '''

    print 'Checking {0} for SEGD'.format(filename)
    return True


def readSEGD(filename, headers_only = False, byte_order = None,
             textual_header_encoding = None, unpack_trace_headers = False,
             **kw_args):
    '''
    as
    
    '''

    print 'Reading file ', filename
    return None


    
def writeSEGD(stream, filename, data_encoding = None, byte_order = None,
              textual_header_encoding = None, **kwargs):
    '''
    '''

    print 'Writing file ', filename
    return None
