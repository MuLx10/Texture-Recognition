import os
from os import scandir
def has_subdir(path):
    """directory names not starting with '.' under given path."""
    y=True
    for entry in scandir(path):
        if not((not entry.name.startswith('.') and entry.is_dir()) or ".html" in entry.name):
            y=False
    if y:
    	return True
    return False

#s="ufraw-batch --out-type=jpeg --out-path=. ./*.NEF"
import sys
path = sys.argv[1]

def apply_recursive(path):
    if has_subdir(path):
       for sub_dir in scandir(path):
        if not ".html" in sub_dir.name:
          apply_recursive(path+'/'+sub_dir.name)
          # break
    else:
      p=path.replace(' ','\ ')
      for f in scandir(path):
        # if not "_bg_" in f.name:
        #   os.system("rm "+p+"/"+f.name)
        if ".NEF" in f.name:
          os.system("ufraw-batch --out-type=jpeg --out-path="+p+" "+p+"/"+f.name)
          os.system('rm '+p+"/"+f.name)
          os.system("python bg_removal.py "+p+"/"+f.name.split('.')[0]+'.jpg')
          print(p+"/"+f.name.split('.')[0]+'.jpg')
      os.system('rm '+p+'/*.NEF')


apply_recursive(path)