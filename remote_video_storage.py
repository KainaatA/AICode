import os
import dropbox
from __params import VideoCredentials

class RemoteStorage:

    def __init__(self):

        self.client = self._setup()

    def _setup(self):
        
        client, exists = dropbox.Dropbox(oauth2_access_token=VideoCredentials.get('TOKEN')), False
        
        for item in client.files_list_folder(path='').entries:
            if item.path_display == VideoCredentials.get('REMOTE_DIRECTORY'): exists = True

        if not exists: client.files_create_folder(VideoCredentials.get('REMOTE_DIRECTORY'))
        # if not os.path.isdir(VideoCredentials.get('LOCAL_UPLOAD_DIRECTORY')): os.makedirs(VideoCredentials.get('LOCAL_UPLOAD_DIRECTORY'))
        if not os.path.isdir(VideoCredentials.get('LOCAL_DOWNLOAD_DIRECTORY')): os.makedirs(VideoCredentials.get('LOCAL_DOWNLOAD_DIRECTORY'))

        print('INFO: Remote storage setup completed.')    
        
        return client

    def upload_files(self):
        
        fpaths = []
        
        for _, __, filenames in os.walk(VideoCredentials.get('LOCAL_UPLOAD_DIRECTORY')):
            fpaths = [os.path.join(VideoCredentials.get('LOCAL_UPLOAD_DIRECTORY'), fpath) for fpath in filenames]

        if not fpaths:
            print('WARN: No content found in local directory to upload.')
            return
        for fpath in fpaths:
            with open(file=fpath, mode='rb') as file:
                fname = os.path.basename(file.name)#file.name.split("/")[-1]
                self.client.files_upload(f=file.read(), path=VideoCredentials.get('RESULTS_DIRECTORY')+'/'+fname, mode=dropbox.files.WriteMode.overwrite)
        else: print('INFO: Uploaded content to remote directory.')


    def download_files(self,remote_dir,local_dir):
        fpaths = []
        for file in self.client.files_list_folder(path=remote_dir).entries:
            fpath = os.path.join(local_dir, os.path.basename(file.path_lower))
            self.client.files_download_to_file(download_path=fpath, path=file.path_lower)
            fpaths.append(fpath)

        print('INFO: Downloaded content from remote directory.')
        return fpaths
