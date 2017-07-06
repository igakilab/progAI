
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import sys

class MongoController:
    def __init__(self):
        self.client = MongoClient('150.89.234.232',27017)
        self.db = self.client.works
        self.coll = self.db.work_col

    def add_post(self,post):
        #post = {"author": "Mike",
            #"text": "My first blog post!",
            #"tags": ["mongodb", "python", "pymongo"],
            #"date": datetime.datetime.utcnow()}
        if self.coll.find(post).count() == 0:
            post_id = self.coll.insert_one(post).inserted_id
            print(post_id)
        else:
            print("Already existed")
    #file_dictをadd_postすると同時に，file_dictに指定されたupdate_timeよりsource_update_timeが6分前までで最新の対応するsourceのドキュメントにstatusとmessageを追加する
    def update_source_status(self, file_dict):
        time_range2 = file_dict["check_time"]
        time_range1 = time_range2 - datetime.timedelta(minutes=6)
        #print(str(time_range1) + '~~~~' + str(time_range2))
        
        key_src = {'sid':file_dict['sid'],'source':file_dict['source'],'source_update_time':{'$gt':time_range1,'$lt':time_range2},'contents':{'$exists':True}}
        key_exe = {'sid':file_dict['sid'],'source':file_dict['source'],'source_update_time':{'$gt':time_range1,'$lt':time_range2},'exefile':{'$exists':True}}
        try:
            oid_src = self.coll.find(key_src).sort('source_update_time',-1).limit(1)[0]['_id']
            self.coll.update({'_id':ObjectId(oid_src)},{'$set':{'check_time':file_dict['check_time'],'status':file_dict['status'],'message':file_dict['message']}})
            oid_exe = self.coll.find(key_exe).sort('source_update_time',-1).limit(1)[0]['_id']
            self.coll.update({'_id':ObjectId(oid_exe)},{'$set':{'check_time':file_dict['check_time'],'status':file_dict['status'],'message':file_dict['message']}})
        except (IndexError):
            pass
