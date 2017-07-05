#command
#python prog2mongo.py ../result-padv17-lec05-2017-0518
#テストのために不要な学生データを間引く

import shutil
import os
import sys

def main(args):
    #print(os.listdir(args[1]))
    for td in os.listdir(args[1]):
        siddirs = args[1]+'/'+td
        if os.path.isdir(siddirs)==True:
            for sid in os.listdir(siddirs):#student directory name
                siddir = siddirs +'/'+sid
                if os.path.isdir(siddir)==True and not sid.startswith('e1b'):
                    shutil.rmtree(siddir)

if __name__ == '__main__':
    main(sys.argv)
    