#command
#python update_source_status.py ../result-padv17-lec05-2017-0518

import datetime
import os
import sys
import re
import mongo_controller as mc

#showlogall.txt内の課題毎コンパイル情報を追加
def add_showlog(showlogfile):
    print("showlogall:"+showlogfile)
    for line in open(showlogfile):
        line = line[:-1]
        if line.startswith('=='):
            try:
                #"=="で始まる行からチェック時刻を取得する
                check_time = datetime.datetime.strptime(line.split()[2][0:16],'%Y-%m%d-%H%M%S')
                #print(check_date)
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
                file_dict = {'sid':sid,'source':source,'check_time':check_time,'status':status,'message':message}
                #print(file_dict)
                mongo = mc.MongoController()
                mongo.update_source_status(file_dict)

def main(args):
    #print(os.listdir(args[1]))
    for td in os.listdir(args[1]):
        siddirs = args[1]+'/'+td
        if os.path.isdir(siddirs)==True:
            for sid in os.listdir(siddirs):#student directory name
                siddir = siddirs +'/'+sid
                if sid == 'showlogall.txt':
                    add_showlog(siddir)

if __name__ == '__main__':
    main(sys.argv)
