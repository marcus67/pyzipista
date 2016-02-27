# This is a self-extracting archive. Copy this script into a '.py' file located in the root
# directory of Pythonista and call the script. It will unzip the data and extract all files to an
# immediate sub directory of the root directory.
#
# This file was generated using pyzipista (see https://github.com/marcus67/pyzipista)
#
# Zipped Application:    [APPNAME]
# Application Home Page: [APPURL]

import zipfile
import base64
import six
import sys
import os

zip_string='''
[BASE64]
'''

mod_times=[
[MOD_TIMES]
]

def extract(path='.'):

  try:  
    print ("Decoding base64 encoded ZIP archive into string...")
    binary_zip_string = base64.b64decode(zip_string, '_&')
    binary_zip_input = six.BytesIO(binary_zip_string)
    print ("Opening string as ZIP file...")
    zip_file = zipfile.ZipFile(binary_zip_input, "r")
    zip_file.printdir()
    print ("Extracting to directory '%s'..." % path)
    zip_file.extractall(path=path)
    print ("All files successfully extracted into directory '%s'." % path)
  
  except Exception as e:
    sys.stderr.write("ERROR '%s' while extracting files!" % str(e))
    return
    
  try:
    print ("Setting modification times...")
    
    for (filename, epoch) in mod_times:
      effective_path = os.path.join(path, filename)
      os.utime(effective_path, (epoch, epoch))
    
    print ("All timestamps successfully updated.")

  except Exception as e:
    sys.stderr.write("ERROR '%s' while updating modification times!" % str(e))
    return
        
def main():
  extract('.')
  
if __name__ == '__main__':
  main()
  
