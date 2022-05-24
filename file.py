import os
from os import path
from pydub import AudioSegment
import speech_recognition as sr

def convert (source):
# if __name__ == "__main__": 
    print(source)
    temp = os.path.basename(source).split('/')[-1]        
    print(temp)
    src = source
    dst = "audios/"+temp
    print(dst)
    sound = AudioSegment.from_file(src)
    sound.export(dst, format="wav")
    print(source+"converted")
    r = sr.Recognizer()