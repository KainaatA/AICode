from remote_storage import RemoteStorage
from plagiarism_scoring import PlagiarismScoring
from database import Database

# Dropbox:
# kainaata.2000@gmail.com
# TestPassword123
#
# Database:
# hamza54834@gmail.com
# #hamzaOo0#12

# dropbox link
# from flask import Flask
# #-------------------------------------------------------------------------------------------------
# app = Flask(__name__)
# @app.route("/PlagCode")

# def PlagCode():
# def main():
if __name__ == "__main__":
    remote_storage = RemoteStorage()
    plagiarism_scoring = PlagiarismScoring()
    database = Database()

    # remote_storage.upload_files()
    fpaths = remote_storage.download_files()

    scores = plagiarism_scoring.resolve_score(fpaths=fpaths)
    
    documents = database.prepare_document(data=scores)

    database.insert_documents(documents)


    #return {"members":["Member 1", "Member 2", "Member 3"]}

# if __name__ == "__main__":
#     app.run()
    
