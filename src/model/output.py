# *- coding: utf-8 -*-
import sys
import logging
from accessible_output2 import outputs # type: ignore

log = logging.getLogger("model.output")

speaker = None

def speak(text, interrupt=0, speech=True, braille=True):
    global speaker
    if not speaker:
        setup()
    if speech:
        speaker.speak(text, interrupt)
    if braille:
        speaker.braille(text)

def setup ():
    global speaker
    logging.debug("Initializing output subsystem.")
    try:
        #  speaker = speech.Speaker(speech.outputs.Sapi5())
        #  else:
        speaker = outputs.auto.Auto()
    except:
        return logging.exception("Output: Error during initialization.")

def copy(text):
    import win32clipboard # type: ignore
    #Copies text to the clipboard.
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
