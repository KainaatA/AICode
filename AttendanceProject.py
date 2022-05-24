import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
# from PIL import ImageGrab
#-----------------------------------------------------------------------------------------------
import dropbox
from __params import ImageCredentials

class ImageRemoteStorage:
    
    def __init__(self):

        self.client = self._setup()

    def _setup(self):
        
        client, exists = dropbox.Dropbox(oauth2_access_token=ImageCredentials.get('TOKEN')), False
        
        for item in client.files_list_folder(path='').entries:
            if item.path_display == ImageCredentials.get('REMOTE_DIRECTORY'): exists = True

        if not exists: client.files_create_folder(ImageCredentials.get('REMOTE_DIRECTORY'))
        if not os.path.isdir(ImageCredentials.get('LOCAL_DOWNLOAD_DIRECTORY')): os.makedirs(ImageCredentials.get('LOCAL_DOWNLOAD_DIRECTORY'))

        print('INFO: Remote storage setup completed.')    
        
        return client
    
    def download_files(self):
    
        fpaths = []
        for file in self.client.files_list_folder(path=ImageCredentials.get('REMOTE_DIRECTORY')).entries:
            fpath = os.path.join(ImageCredentials.get('LOCAL_DOWNLOAD_DIRECTORY'), file.path_lower.split('/')[-1])
            self.client.files_download_to_file(download_path=fpath, path=file.path_lower)
            fpaths.append(fpath)

        print('INFO: Downloaded content from remote directory.')
        return fpaths
#--------------------------------------------------------------------------------------------------  
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'{name},{dtString}')
 
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

def main(video_path):
    path = 'ImagesAttendance'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        print(classNames)

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(video_path)

    while True:
        success, img = cap.read()
        if img is None:
            break
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
            if faceDis[matchIndex]< 0.50:
                name = classNames[matchIndex].upper()
                return name
                # markAttendance(name)
            else:
                name = 'Unknown'
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        # cv2.imshow('Webcam',img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()
    return 'Unknown'