from pymongo import MongoClient
from __params import CREDENTIALS

class Database:
    
    def __init__(self):
        self.client = MongoClient(CREDENTIALS.get('DATABASE_URL'))
        database = self.client[CREDENTIALS.get('DATABASE_NAME')]
        self.collection = database[CREDENTIALS.get('COLLECTION_NAME')]
        #print('here')

    def prepare_document(self, data):
        documents = []
        for key, value in data.items():
            fname = key.split('/')[-1]
            roll_number = fname.split('__')[0].lower()
            name = fname.split('__')[1].lower()
            file_name = fname.split('__')[2].lower()
            document = {
                '_id': f'{roll_number}__{file_name}',
                'roll_number': roll_number,
                'name': name,
                'file_name': file_name,
                'plagiarism_score': round(value, 3)
            }
            documents.append(document)
        return documents

    def insert_documents(self, documents):
        try:
            self.collection.insert_many(documents)
            print('INFO: Documents have been stored to database.')
        except Exception as e:
            print('ERROR: ', e)

db = Database()