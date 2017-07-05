#command
#python prog2mongo.py ../result-padv17-lec05-2017-0518

from pymongo import MongoClient
import datetime
import os
import sys
import re

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

#各ファイルの情報を追加
def add_cfile_status(sid,file,filepath):
    update_time = datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime)
    print(filepath)
    contents = open(filepath).read()
    file_dict = {'sid':sid,'source':file,'source_update_time':update_time,'contents':contents}
    print(file_dict)
    mc = MongoController()
    mc.add_post(file_dict)

#各ファイルの情報を追加
def add_exefile_status(sid,file,filepath):
    create_time = datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime)
    for line in open(filepath):
        line = line[:-1]
        if line.split()[2] == 'src':
            source = line.split()[3]
            #ソースファイルが作成された日時
            source_update_time = datetime.datetime.strptime(' '.join(line.split()[0:2]),'%Y/%m/%d %H:%M:%S')
    file_dict = {'sid':sid,'exefile':file,'source':source,'exe_create_time':create_time,'source_update_time':source_update_time}
    print(file_dict)
    mc = MongoController()
    mc.add_post(file_dict)

#student dir配下のファイルそれぞれについて情報を追加
def add_sid_dir(sid,siddir):
    for sfile in os.listdir(siddir):
        if re.compile(r'^_|^\.|^#|~$|.pdf$').search(sfile):
            pass
        elif re.compile(r'.c$').search(sfile):
            sourcefile = siddir+'/'+sfile
            if os.path.isdir(sourcefile)!=True:
                add_cfile_status(sid,sfile,siddir+'/'+sfile)

        elif re.compile(r'.exe.txt$').search(sfile):
            sourcefile = siddir+'/'+sfile
            if os.path.isdir(sourcefile)!=True:
                add_exefile_status(sid,sfile,siddir+'/'+sfile)

#showlogall.txt内の課題毎コンパイル情報を追加
def add_showlog(showlogfile):
    print("showlogall:"+showlogfile)
    for line in open(showlogfile):
        line = line[:-1]
        if line.startswith('=='):
            try:
                #"=="で始まる行からチェック時刻を取得する
                check_date = datetime.datetime.strptime(line.split()[2][0:16],'%Y-%m%d-%H%M%S')
                print(check_date)
            except (ValueError):
                pass
        elif line.startswith('e1'):
            if line.split()[2] == '★':
                pass
            else:
                #print(line)
                sid = line.split()[0]
                source = line.split()[1]+'.c'
                status = line.split()[2]
                message = ' '.join(line.split()[3:])
                #print(message)
                file_dict = {'sid':sid,'source':source,'update_time':check_date,'status':status,'message':message}
                print(file_dict)
                mc = MongoController()
                mc.add_post(file_dict)

def main(args):
    #print(os.listdir(args[1]))
    for td in os.listdir(args[1]):
        siddirs = args[1]+'/'+td
        if os.path.isdir(siddirs)==True:
            for sid in os.listdir(siddirs):#student directory name
                siddir = siddirs +'/'+sid
                if os.path.isdir(siddir)==True:
                    add_sid_dir(sid,siddir)
                elif sid == 'showlogall.txt':                    
                    pass #add_showlog(siddir)

if __name__ == '__main__':
    main(sys.argv)
