import ctypes
import time

SendInput = ctypes.windll.user32.SendInput
space_pressed = 0x39  # Spacebar

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),  # Virtual key code
                ("wScan", ctypes.c_ushort),  # Scan code (set to 0)
                ("dwFlags", ctypes.c_ulong),  # Flags
                ("time", ctypes.c_ulong),     # Timestamp
                ("dwExtraInfo", PUL)]         # Extra info

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0, 0, 0, ctypes.pointer(extra))  # Corrected flags
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0, 0x0002, 0, ctypes.pointer(extra))  # Release flag
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    PressKey(space_pressed)
    time.sleep(1)
    ReleaseKey(space_pressed)