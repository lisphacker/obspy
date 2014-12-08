import numpy as np

def read_bytes(file_obj, count):
    return np.frombuffer(file_obj.read(count), dtype = np.uint8)

def bytes_to_nibbles(byte_buffer):
    nibble_buffer = np.empty(byte_buffer.size * 2, dtype = byte_buffer.dtype)
    for i in xrange(0, nibble_buffer.size, 2):
        j = int(i / 2)
        nibble_buffer[i] = (byte_buffer[j] >> 4) & 0xf
        nibble_buffer[i + 1] = byte_buffer[j] & 0xf
    return nibble_buffer

def read_nibbles(file_obj, count):
    return bytes_to_nibbles(read_bytes(file_obj, int(count / 2)))
            
def ffff(nibbles):
    return np.all(nibbles == 0xf)

def read_bcd(nibbles):
    val = 0
    for nibble in nibbles:
        val = val * 10 + nibble
    return val

def read_uint_from_bytes(bytes):
    val = 0
    for byte in bytes:
        val = val * 256 + int(byte)
    return val

def read_sint_from_bytes(bytes):
    val = 0
    for byte in bytes:
        val = val * 256 + int(byte)
    return val

def read_q13_from_bytes(bytes):
    msb = 1
    lsb = 0
    
    s = bytes[msb] >> 7
    c = (bytes[msb] >> 2) & 31
    q = ((int(bytes[msb]) & 3) << 8) | int(bytes[lsb])

    sign = 1 if s == 0 else -1
    
    return sign * (float(c) + float(q) / 1024.0)

def read_double(bytes):
    return np.frombuffer(bytes, dtype = '>f8', count = 1)[0]

def read_float(bytes):
    return np.frombuffer(bytes, dtype = '>f4', count = 1)[0]
