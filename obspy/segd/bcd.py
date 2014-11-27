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
