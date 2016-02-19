# coding: utf-8
# This file is part of https://github.com/marcus67/pyzipista

import logging
import sys
import os
import zipfile
import re
import base64
import StringIO

import log
import config
import zip_handler_config

reload(log)
reload(config)
reload(zip_handler_config)

global logger

logger = log.open_logging('pyzipista', reload=True)  

UNZIP_TEMPLATE_FILE = '../pyzipista/etc/zip_template.py'
BASE64_PLACEHOLDER = '[BASE64]'
MOD_TIMES_PLACEHOLDER = '[MOD_TIMES]'
APP_NAME_PLACEHOLDER = '[APPNAME]'
APP_URL_PLACEHOLDER = '[APPURL]'
GIT_IGNORE_FILE = '.gitignore'
PYZIPISTA_CONFIG_FILE = 'pyzipista_config'
CONFIG_FILE_SEARCH_PATH = [ '.', 'etc' ]
GITSYNCHISTA_IGNORE_FILE = 'gitsynchista_ignore'
GITSYNCHISTA_IGNORE_FILE_2 = 'gitsynchista_ignore.txt'
PYZIPISTA_IGNORE_FILE = 'pyzipista_ignore'
PYZIPISTA_IGNORE_FILE_2 = 'pyzipista_ignore.txt'

ADDITIONAL_IGNORE_PATTERNS = '|\..*'

class File(object):
  
  def __init__(self, name, physical_name, base_name, modification_time, is_ignored=False):
    
    self.name = name
    self.physical_name = physical_name
    self.base_name = base_name
    self.modification_time = modification_time
    self.is_ignored = is_ignored
    
  def is_directory(self):

    return self.sub_files != None
    
  def __str__(self):
    return "log=%s phys=%s dir=%s ign=%s %s" % (self.name, self.physical_name, self.is_directory(), self.is_ignored, time.ctime(self.mtime))
  
class IgnoreInfo(object):
  
  def __init__(self, file_string):
    
    global logger
    
    if len(file_string) > 0:
      pattern_string = ('^' + file_string.replace('.','\.').replace('*', '.*').replace('\n','$|^') + '$').replace('|^$', '')
      logger.info("Created IgnoreInfo with pattern regex '%s'" % pattern_string)
      self.regex = re.compile(pattern_string)     
    else:
      self.regex = None   
    
  def is_ignored(self, name):
    
    if self.regex:
      return self.regex.match(name) != None
    else:
      return False
    
global_ignore_info = IgnoreInfo(ADDITIONAL_IGNORE_PATTERNS)
    
class FileAccess(object):
  
  def __init__(self, root_path):
    
    self.root_path = root_path
  
  def load_directory(self, base_path=None, parent_is_ignored=False):
    
    if not base_path:
      base_path = self.root_path
    logger.info("Loading file directory '%s'" % base_path)
    files = []
    github_ignore_info = self.load_ignore_info(os.path.join(base_path, GIT_IGNORE_FILE))
    gitsynchista_ignore_info = self.load_ignore_info(os.path.join(base_path, GITSYNCHISTA_IGNORE_FILE))
    gitsynchista_ignore_info_2 = self.load_ignore_info(os.path.join(base_path, GITSYNCHISTA_IGNORE_FILE_2))
    pyzipista_ignore_info = self.load_ignore_info(os.path.join(base_path, PYZIPISTA_IGNORE_FILE))
    pyzipista_ignore_info_2 = self.load_ignore_info(os.path.join(base_path, PYZIPISTA_IGNORE_FILE_2))
    
    for f in os.listdir(base_path):
      is_ignored = parent_is_ignored or github_ignore_info.is_ignored(f) or gitsynchista_ignore_info.is_ignored(f) or gitsynchista_ignore_info_2.is_ignored(f) or pyzipista_ignore_info.is_ignored(f) or pyzipista_ignore_info_2.is_ignored(f)
      path = os.path.join(base_path, f)
      attr = os.stat(path)
      isDirectory = os.path.isdir(path)
      if isDirectory:
        sub_files = self.load_directory(base_path=path, parent_is_ignored=is_ignored)
        files.extend(sub_files)
      else:
      
        file = File(name=path.replace(self.root_path, '.', 1), physical_name=path, base_name=f, is_ignored=is_ignored, modification_time=attr.st_mtime)
        
        files.append(file)
    
    return files
       
  def file_exists(self, path):
    
    return os.path.exists(path)
    
  def load_into_string(self, path):
    
    return open(path, "rb").read()    
    
  def load_ignore_info(self, ignore_file):

    global logger
  
    if self.file_exists(ignore_file):
      ignore_patterns = self.load_into_string(ignore_file)
      logger.info("Loading ignore file '%s'" % ignore_file)    
      return IgnoreInfo(ignore_patterns)
    else:
      return IgnoreInfo('')   
  

class ZipHandler(object):
  
  def __init__(self, config):
    
    self.config = config
    
    if self.config.general.app_directory == None:  
      raise Exception("ERROR: [general].app_directory not set in configuration file!")
    
    
  def get_latest_timestamp(self):
    
    global logger
  
    file_access = FileAccess(self.config.general.root_path)  
    base_path = os.path.join(self.config.general.root_path, self.config.general.app_directory)
    files = file_access.load_directory(base_path)
    latest_timestamp = -1    
    
    for file in files:
      if not file.is_ignored:
        if file.modification_time > latest_timestamp:
          latest_timestamp = file.modification_time

    return latest_timestamp

      
  def get_zip_filename(self):
    return os.path.join(self.config.general.root_path, self.config.general.app_directory, self.config.general.zip_filename)
    
  def get_zip_timestamp(self):
    zip_filename = self.get_zip_filename()
    
    if os.path.exists(zip_filename):
      attr = os.stat(zip_filename)
      return attr.st_mtime
      
    else:
      return -1
    
    
  def create_zip_file(self):
    
    global logger
  
    app_name = self.config.general.app_name
    if not app_name:
      app_name = self.config.general.app_directory
    app_url = self.config.general.app_url 
    if not app_url:
      app_url = "[not available]"
    file_access = FileAccess(self.config.general.root_path)  
    base_path = os.path.join(self.config.general.root_path, self.config.general.app_directory)
    files = file_access.load_directory(base_path)
    
    zip_string_output = StringIO.StringIO()
    zip_file = zipfile.ZipFile(file=zip_string_output, mode="w", compression=zipfile.ZIP_DEFLATED)
    
    zip_file.comment = 'Generated by pyzipista.py (see https://github.com/marcus67/pyzipista).'
    zip_file.debug = 3
    
    count = 0
    mod_times_string = ''
    for file in files:
      
      if not file.is_ignored:
        logger.debug("Adding file '%s' as '%s' to zip file" % ( file.physical_name, file.name ))
        zip_file.write(filename=file.physical_name, arcname=file.name)
        mod_times_string = "%s\n( '%s' , %d ), " % (mod_times_string, file.name, file.modification_time)
        count = count + 1
        
    zip_file.close()
    binary_zip_string = zip_string_output.getvalue()
    
    logger.info("Adding %d files to ZIP archive" % count)
    logger.info("ZIP archive has %d bytes" % len(binary_zip_string))
    
    base64_string = base64.b64encode(binary_zip_string, '_&')
    unzip_template_file_as_string = file_access.load_into_string(UNZIP_TEMPLATE_FILE)    
    unzip_file_as_string = unzip_template_file_as_string.replace(BASE64_PLACEHOLDER, base64_string).replace(APP_NAME_PLACEHOLDER, app_name).replace(APP_URL_PLACEHOLDER, app_url).replace(MOD_TIMES_PLACEHOLDER, mod_times_string)
    
    zip_filename = self.get_zip_filename()
    with open(zip_filename, "w") as unzip_file:
      unzip_file.write(unzip_file_as_string)
    logger.info("Wrote self-extracting archive to '%s'" % zip_filename)
      
    
def load_config_file_and_zip(config_filename):
  global logger
  
  pyzipista_config = None
  logger.info("Starting application for config %s", config_filename)
  
  try:
    config_handler = config.ConfigHandler(zip_handler_config.ZipHandlerConfig())
    pyzipista_config = config_handler.read_config_file(config_filename)
  
  except Exception as e:    
    logger.exception("Error '%s' while reading configuration file %s" % (str(e), config_filename))  
    
  if not pyzipista_config:
    logger.warn('Could not read config %s', config_filename)
    
  try:
    pyzipista_config.dump()
    zip_handler = ZipHandler(pyzipista_config)
    zip_handler.create_zip_file()
  
  except Exception as e:
    logger.exception("Error '%s' while writing zip file" % str(e))  
    
  logger.info("Terminating application")
  
  
def load_config_file_and_check_zip_required(config_filename):
  
  global logger
  
  latest_timestamp = None
  handler_config = None
  zip_required = False
  
  logger.info("Start checking file status for '%s'" % config_filename)
  try:
    config_handler = config.ConfigHandler(zip_handler_config.ZipHandlerConfig())
    handler_config = config_handler.read_config_file(config_filename)
  
  except Exception as e:
    
    logger.error("Error '%s' while reading configuration file" % str(e))  
    return None

  try:
    zip_handler = ZipHandler(handler_config)
    latest_timestamp = zip_handler.get_latest_timestamp()
    zip_timestamp = zip_handler.get_zip_timestamp()
    zip_required = latest_timestamp > zip_timestamp
  
  except Exception as e:
    
    logger.error("Error '%s' checking file status" % str(e))  
    return None
      
  logger.info("Returning status 'zip required': %s" % str(zip_required))   
  return zip_required
  
  
def main():
  
  if len(sys.argv) == 2:  
    load_config_file_and_zip(sys.argv[1])
  else:
    logger.warning("pyzipista must called with filename of configuration file")
if __name__ == '__main__':
  main()
  