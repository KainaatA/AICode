import datetime
import os
import shutil

import cv2 as cv
import dropbox
from pymongo import MongoClient

import AttendanceProject
import mouth_opening_detector
import person_and_phone
from __params import VideoCredentials,AudioCredentials
from remote_video_storage import RemoteStorage
import Voice
from AttendanceProject import ImageRemoteStorage
from file import convert
#Flask Implementation
# from flask import Flask
# #-------------------------------------------------------------------------------------------------
# app = Flask(__name__)
# @app.route("/AICode")

# def AICode():
if __name__ == "__main__":
    #-------------------------------------------------
    remote_storage_images = ImageRemoteStorage()
    remote_storage_images.download_files()
    #-------------------------------------------------
    remote_storage=RemoteStorage()
    remote_storage.download_files(remote_dir=VideoCredentials.get('REMOTE_DIRECTORY'),local_dir=VideoCredentials.get('LOCAL_DOWNLOAD_DIRECTORY'))

    remote_storage.download_files(remote_dir=AudioCredentials.get('REMOTE_DIRECTORY'),local_dir=AudioCredentials.get('LOCAL_DOWNLOAD_DIRECTORY'))

    #Video
    video_list=[os.path.join('videos',f) for f in os.listdir('videos')]
    data_list=[]
    # video_list=[]
    for video_path in video_list:
        ap_name,ap_time=AttendanceProject.main(video_path),datetime.datetime.now().strftime('%H:%M:%S')
        # ap_name,ap_time='unknown',datetime.datetime.now().strftime('%H:%M:%S')
        mop_detection_result,mop_reason=mouth_opening_detector.main(video_path)
        pnp_detection_result,pnp_reasons=person_and_phone.main(video_path)

        #write results to a temp directory
        if os.path.exists('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')
        student_name=os.path.basename(video_path).split('.')[0]
        print(student_name)
        if mop_detection_result is not None:
            cv.imwrite('temp\\mop_detection_result-'+student_name+'.png',mop_detection_result)
        if pnp_detection_result is not None:
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(pnp_detection_result, '\n'.join(pnp_reasons), (30, 30), font,
                        1, (0, 255, 255), 2)
            cv.imwrite('temp\\pnp_detection_result-' + student_name + '.png', pnp_detection_result)


        #iterate over the images and upload them to dropbox
        for fpath in os.listdir('temp'):
            fpath='temp/'+str(fpath)
            with open(file=fpath, mode='rb') as file:
                fname = os.path.basename(file.name)  # file.name.split("/")[-1]
                remote_storage.client.files_upload(f=file.read(), path=VideoCredentials.get('RESULTS_DIRECTORY') + '/' + fname,
                                         mode=dropbox.files.WriteMode.overwrite)
        else:
            print('INFO: Uploaded content to remote directory.')



        data = {
            '_id': str(student_name),
            'name':str(student_name),
            'Attendence':'{}__{}'.format(ap_name,ap_time),
            'MouthOpeningDetector': mop_reason,
            'PersonAndPhoneDetector_MobilePhone': 'Mobile Phone detected' if 'Mobile Phone detected' in pnp_reasons else None,
            'PersonAndPhoneDetector_NoPersonDetected': 'No person detected' if 'No person detected' in pnp_reasons else None,
            'PersonAndPhoneDetector_MorePersonsDetected': 'More than one person detected' if 'More than one person detected' in pnp_reasons else None,

        }
        data_list.append(data)

    # upload results to mongodb
    client = MongoClient("DB Link")
    database = client['myFirstDatabase']
    collection = database['feedbacks']
    for data in data_list:
        try:
            collection.update_one(data,{"$set": data},upsert=True) #upsert true k sath update
        except:
            collection.update_one(data,{"$set": data},upsert=False)

    # collection.insert_many(data_list)
    audio_list1 = [os.path.join('temp_audios', f) for f in os.listdir('temp_audios')]
    for audio1 in audio_list1:
        convert(audio1)
        
        
    audio_list = [os.path.join('audios', f) for f in os.listdir('audios')]
    for audio in audio_list:
        audio_result = Voice.main(audio)
        student_name=os.path.basename(audio).split('.')[0]
        print(student_name)
        try:
            collection.update_many({"_id": student_name}, {"$set": {'AudioDetection':str(audio_result),'name':str(student_name)}}, upsert=True)  # upsert true k sath update
        except:
            collection.update_many({"_id": student_name}, {"$set": {'AudioDetection':str(audio_result),'name':str(student_name)}}, upsert=False)


    #return {"members":["Member 1", "Member 2", "Member 3"]}

# if __name__ == "__main__":
#     app.run()
    
