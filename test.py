# coding: utf-8
# This file is part of https://github.com/marcus67/pyzipista

import log
import pyzipista


reload(log)

global logger

logger = log.open_logging('test', reload=True)  

def test():

  global logger
  
  pyzipista.load_config_file_and_check_zip_required('etc/pyzipista_config')
  
  
if __name__ == '__main__':
  test()