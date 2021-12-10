import win32clipboard
import pyttsx3


def speak():
    voice = pyttsx3.init()
    rate = voice.getProperty('rate')
    voice.setProperty('rate', rate + 50)
    voice.say(get_clip_board())
    try:
        voice.runAndWait()
    except RuntimeError:
        voice.stop()


def get_clip_board():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data
