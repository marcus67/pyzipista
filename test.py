# coding: utf-8
# This file is part of https://github.com/marcus67/pyzipista

import six

import log
import pyzipista

if six.PY3:
	from importlib import reload	

reload(log)
reload(pyzipista)

global logger

logger = log.open_logging('test', reload=True)  

def test():

  global logger

  pyzipista.load_config_file_and_check_zip_required('etc/pyzipista_config')  
  
if __name__ == '__main__':
  test()
