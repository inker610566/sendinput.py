import ctypes
from ctypes import c_int, c_wchar_p, WINFUNCTYPE, windll, create_string_buffer, byref
from ctypes import Structure, Union, cast, POINTER
from ctypes.wintypes import HWND
from ctypes.wintypes import HWND, LPCSTR, UINT, LPARAM, BOOL, LONG, WORD, DWORD, LPVOID
from ctypes import cdll
import re

__all__ = [
    'Window',
    'FindWindowByName'
]
WINDOW_NAME_LENGTH = 100
# http://stackoverflow.com/questions/9226516/python-windows-console-and-encodings-cp-850-vs-cp1252
import locale
os_encoding = locale.getpreferredencoding()
#os_encoding = 'cp' + str(cdll.kernel32.GetACP())

class Window:
    def __init__(self, hwnd):
        self.hwnd = hwnd

    def SetForeground(self):
        ctypes.windll.User32.SetForegroundWindow(self.hwnd)
        ctypes.windll.User32.ShowWindow(self.hwnd, c_int(10))

class EnumWinResult(Structure):
    _fields_ = [
        ("subname", c_wchar_p),
        ("hwnd", HWND)
    ]

def FindWindowByName(subname):
    '''
    :Args:
        - subname: find windows title contain subname
    :Returns:
        - Window object
    '''
    # https://msdn.microsoft.com/zh-tw/library/windows/desktop/ms633497(v=vs.85).aspx
    WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
    cb = WNDENUMPROC(_EnumWindowsCallback)
    res = EnumWinResult()
    res.subname = subname
    res.hwnd = 0
    ctypes.windll.User32.EnumWindows(cb, byref(res))
    return Window(res.hwnd) if res.hwnd else None

def _EnumWindowsCallback(hwnd, lparam):
    global WINDOW_NAME_LENGTH
    p = create_string_buffer(WINDOW_NAME_LENGTH)
    ctypes.windll.User32.GetWindowTextA(hwnd, byref(p), WINDOW_NAME_LENGTH)
    rp = cast(lparam, POINTER(EnumWinResult))
    subname = rp.contents.subname
    #print(p.value)
    #print(subname)
    p = p.value.decode(os_encoding)
    if p.find(subname) != -1:
        rp.contents.hwnd = hwnd
        return 0
    return 1
