import os 

CREDENTIALS = {
    'REMOTE_DIRECTORY': '/data',
    'DATABASE_NAME': 'myFirstDatabase',
    'COLLECTION_NAME': 'plagscores',
    'LOCAL_UPLOAD_DIRECTORY': os.path.join(os.getcwd(), 'uploads'),
    'LOCAL_DOWNLOAD_DIRECTORY': os.path.join(os.getcwd(), 'downloads'),
    'TOKEN': 'HkS3AmvwAaEAAAAAAAAAAcuqg8SY7OJKWvWB86uK5eMEllPM1S6YyCaNYFGYlV6a',
    'DATABASE_URL': 'mongodb+srv://hamzaali:#hamzaOo0#12@cluster0.rkpc2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
   }

VideoCredentials={
    'dropbox_email':'kainaata.2000@gmail.com',
    'dropbox_password':'TestPassword123',
    'REMOTE_DIRECTORY': '/test Videos',
    'RESULTS_DIRECTORY': '/Results',
    'TOKEN': 'HkS3AmvwAaEAAAAAAAAAAcuqg8SY7OJKWvWB86uK5eMEllPM1S6YyCaNYFGYlV6a',
    'LOCAL_UPLOAD_DIRECTORY': os.path.join(os.getcwd(), 'results'),
    'LOCAL_DOWNLOAD_DIRECTORY': os.path.join(os.getcwd(), 'videos'),
    }

AudioCredentials={
    'dropbox_email':'kainaata.2000@gmail.com',
    'dropbox_password':'TestPassword123',
    'REMOTE_DIRECTORY': '/Audio_Records',
    'TOKEN': 'HkS3AmvwAaEAAAAAAAAAAcuqg8SY7OJKWvWB86uK5eMEllPM1S6YyCaNYFGYlV6a',
    'LOCAL_DOWNLOAD_DIRECTORY': os.path.join(os.getcwd(), 'temp_audios'),
    }
ImageCredentials={
    'dropbox_email':'kainaata.2000@gmail.com',
    'dropbox_password':'TestPassword123',
    'REMOTE_DIRECTORY': '/Image',
    'TOKEN': 'HkS3AmvwAaEAAAAAAAAAAcuqg8SY7OJKWvWB86uK5eMEllPM1S6YyCaNYFGYlV6a',
    'LOCAL_DOWNLOAD_DIRECTORY': os.path.join(os.getcwd(), 'ImagesAttendance'),
    }