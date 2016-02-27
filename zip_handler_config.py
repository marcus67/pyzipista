# coding: utf-8
# This file is part of https://github.com/marcus67/pyzipista

import platform
import config
import six

if six.PY3:
	from importlib import reload
	
reload(config)

class GeneralConfig(config.BaseConfig):
  
  def __init__(self):

    self.root_path = '..'
    self.app_directory = None
    self.app_name = None
    self.app_url = None
    self.zip_filename = None

class ZipHandlerConfig(config.BaseConfig):
  
  def __init__(self):

    self.general = GeneralConfig()    
