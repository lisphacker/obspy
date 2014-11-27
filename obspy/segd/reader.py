'''
Functions and classes for reading a SEGD file.

@author: Gautham Ganapathy
@contact: gautham@lisphacker.org
'''

GENERAL_HEADER1_SIZE = 32

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
        
        segd.file_headers.general_header1 = self.read_general_header1()

        return segd

    def read_general_header1(self):
        byte_buffer = read_bytes(self.file_obj, GENERAL_HEADER1_SIZE)
        genhdr1 = GeneralHeader1()
        genhdr1.populate_from_buffer(byte_buffer)
        return genhdr1
