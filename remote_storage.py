import os
import dropbox
from __params import CREDENTIALS

class RemoteStorage:

    def __init__(self):

        self.client = self._setup()

    def _setup(self):
        
        client, exists = dropbox.Dropbox(oauth2_access_token=CREDENTIALS.get('TOKEN')), False
        
        for item in client.files_list_folder(path='').entries:
            if item.path_display == CREDENTIALS.get('REMOTE_DIRECTORY'): exists = True

        if not exists: client.files_create_folder(CREDENTIALS.get('REMOTE_DIRECTORY'))
        if not os.path.isdir(CREDENTIALS.get('LOCAL_UPLOAD_DIRECTORY')): os.makedirs(CREDENTIALS.get('LOCAL_UPLOAD_DIRECTORY'))
        if not os.path.isdir(CREDENTIALS.get('LOCAL_DOWNLOAD_DIRECTORY')): os.makedirs(CREDENTIALS.get('LOCAL_DOWNLOAD_DIRECTORY'))

        print('INFO: Remote storage setup completed.')    
        
        return client

    def upload_files(self):
        
        fpaths = []
        
        for _, __, filenames in os.walk(CREDENTIALS.get('LOCAL_UPLOAD_DIRECTORY')):
            fpaths = [os.path.join(CREDENTIALS.get('LOCAL_UPLOAD_DIRECTORY'), fpath) for fpath in filenames]

        if not fpaths:
            print('WARN: No content found in local directory to upload.')
            return
        for fpath in fpaths:
            with open(file=fpath, mode='rb') as file:
                fname = file.name.split("/")[-1]
                self.client.files_upload(f=file.read(), path=os.path.join(CREDENTIALS.get('REMOTE_DIRECTORY'), fname), mode=dropbox.files.WriteMode.overwrite)    
        else: print('INFO: Uploaded content to remote directory.')
    
    def download_files(self):

        fpaths = []
        for file in self.client.files_list_folder(path=CREDENTIALS.get('REMOTE_DIRECTORY')).entries:
            fpath = os.path.join(CREDENTIALS.get('LOCAL_DOWNLOAD_DIRECTORY'), file.path_lower.split('/')[-1])
            self.client.files_download_to_file(download_path=fpath, path=file.path_lower)
            fpaths.append(fpath)

        print('INFO: Downloaded content from remote directory.')
        return fpaths
