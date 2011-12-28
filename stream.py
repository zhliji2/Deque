from ctypes import cdll, c_void_p
from ctypes.util import find_library

avformat = cdll.LoadLibrary(find_library('ApplicationServices '))