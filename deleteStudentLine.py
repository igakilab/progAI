#command
#python prog2mongo.py ../result-padv17-lec05-2017-0518
#テストのために不要な学生データをshowlogall.txtから間引く
#original fileはshowlogall.txt.orgとして保存

import os
import sys
import shutil

def delete_studentline_from_showlog(siddir):
    shutil.copy2(siddir,siddir+'.org')
    os.remove(siddir)
    original = open(siddir+'.org', 'r')
    decimated_file_name = siddir
    decimated = open(decimated_file_name,'w')
    
    original_lines = original.readlines()
    original.close()
    
    for line in original_lines:
        #line = line[:-1]
        if line.startswith('e1q') or line.startswith('e1n') or line.startswith('e1c'):
            pass
        elif line.startswith('e1b') and line.split()[2] == '★':
            pass
        else:
            decimated.write(line)
    decimated.close()

def main(args):
    #print(os.listdir(args[1]))
    for td in os.listdir(args[1]):
        siddirs = args[1]+'/'+td
        if os.path.isdir(siddirs)==True:
            for sid in os.listdir(siddirs):#student directory name
                siddir = siddirs +'/'+sid
                if os.path.isdir(siddir)==True:
                    pass
                elif sid == 'showlogall.txt':                    
                    delete_studentline_from_showlog(siddir)

if __name__ == '__main__':
    main(sys.argv)
    