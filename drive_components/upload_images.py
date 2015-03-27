
import glob
import os.path
import json

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

folder = drive.ListFile({'q':"'root' in parents and title='dmvimages'"}).GetList()
if len(folder) > 1:
  print("Found too many dmvimages folders");
  exit(-1);
else:
  folder = folder[0]

update = False

name_to_id = {}
for f in glob.glob('../plots/*.svg'):
  curFile = os.path.basename(f)
  gfile = drive.CreateFile()
  gfile.SetContentFile(f)
  gfile['title'] = curFile
  gfile['parents'] = [ {"kind":"drive#fileLink", "id":folder['id']}]
  #TODO SET SHARED TRUE!
  gfile.Upload()
  name_to_id[curFile.replace('.svg','')] = gfile['id']


fout = open('name_to_id.js','w')
json.dump(name_to_id,fout)
fout.close()
  

