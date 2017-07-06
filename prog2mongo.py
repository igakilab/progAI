#command
#python prog2mongo.py ../result-padv17-lec05-2017-0518

import datetime
import os
import sys
import re
import mongo_controller as mc

#各ファイルの情報を追加
def add_cfile_status(sid,file,filepath):
    update_time = datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime)
    print(filepath)
    contents = open(filepath).read()
    file_dict = {'sid':sid,'source':file,'source_update_time':update_time,'contents':contents}
    print(file_dict)
    mongo = mc.MongoController()
    mongo.add_post(file_dict)

#各ファイルの情報を追加
def add_exefile_status(sid,file,filepath):
    create_time = datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime)
    source = None
    source_update_time = None
    for line in open(filepath):
        line = line[:-1]
        if len(line.split()) > 3 and line.split()[2] == 'src':
            source = line.split()[3]
            #ソースファイルが作成された日時
            source_update_time = datetime.datetime.strptime(' '.join(line.split()[0:2]),'%Y/%m/%d %H:%M:%S')
    #print(filepath,flush=True)
    if source is None or source_update_time is None:
        file_dict = {'sid':sid,'exefile':file,'exe_create_time':create_time}
    else:
        file_dict = {'sid':sid,'exefile':file,'source':source,'exe_create_time':create_time,'source_update_time':source_update_time}
    print(file_dict)
    mongo = mc.MongoController()
    mongo.add_post(file_dict)

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

def main(args):
    #print(os.listdir(args[1]))
    for td in os.listdir(args[1]):
        siddirs = args[1]+'/'+td
        if os.path.isdir(siddirs)==True:
            for sid in os.listdir(siddirs):#student directory name
                siddir = siddirs +'/'+sid
                if os.path.isdir(siddir)==True:
                    add_sid_dir(sid,siddir)

if __name__ == '__main__':
    main(sys.argv)
