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
import StringIO

zip_string='''
[BASE64]
'''

def main():

  try:  

    print "Decoding base64 encoded ZIP archive into string..."
    binary_zip_string = base64.b64decode(zip_string, '_&')
    binary_zip_input = StringIO.StringIO(binary_zip_string)
  
    print "Opening string as ZIP file..."
    zip_file = zipfile.ZipFile(binary_zip_input, "r")
  
    zip_file.printdir()
    
    print "Extracting ..."
    
    zip_file.extractall()
    
    print "All files successfully extracted into local directory."
  
  except Exception as e:
    
    sys.stderr.write("ERROR '%s' while extracting files!" % str(e))
    
if __name__ == '__main__':
  main()
  
