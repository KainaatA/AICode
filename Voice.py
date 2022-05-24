import speech_recognition as sr
from file import convert
from remote_video_storage import RemoteStorage
import os
from __params import AudioCredentials
r = sr.Recognizer()
r = sr.Recognizer()

# def Voice(filename):
def main(filename):
# if __name__ == "__main__":
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        text=''.join(set(text.split(' ')))
        print("The attendance is:"+ text)
        return text

# if __name__ == "__main__":
#     remote_storage=RemoteStorage()
#     remote_storage.download_files(remote_dir=AudioCredentials.get('REMOTE_DIRECTORY'),local_dir=AudioCredentials.get('LOCAL_DOWNLOAD_DIRECTORY'))


#     audio_list1 = [os.path.join('temp_audios', f) for f in os.listdir('temp_audios')]
#     for audio1 in audio_list1:
#         convert(audio1)
        
        
#     audio_list = [os.path.join('audios', f) for f in os.listdir('audios')]
#     for audio in audio_list:
#         audio_result = Voice(audio)
#         student_name=os.path.basename(audio).split('.')[0]
#         print(student_name)
#         print(audio_result)
        
# initialize the recognizer
