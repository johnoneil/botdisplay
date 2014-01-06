#!/usr/bin/python
# vim: set ts=2 expandtab:
"""
Module: botdisplay.py
Desc: drive a browser window via database URLs
Author: John O'Neil
Email: oneil.john@gmail.com
DATE: Thursday, November 7th 2013

  bot that drives browser (currently Firefox)
  to a sequence of URLs and then exits.
  
"""


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time
import argparse
import os
import concurrent.futures
import sys

try:
  #we try to access django settings for the web interface to access
  #the same sqlite3 database file
  from botdisplay_webinterface import settings as bd_settings
  #from botdisplay_webinterface import botdisplay as bd
  #from botdisplay.models import botdisplay.models.URLDisplay
  #from botdisplay_webinterface.botdisplay.models import URLDisplay
  db_settings = bd_settings.DATABASES['default']
  print 'engine is ' + db_settings['ENGINE']
  print str(db_settings)
  from django.conf import settings
  settings.configure(
    DATABASE_ENGINE = db_settings['ENGINE'],
    DATABASE_NAME = db_settings['NAME'],
    DATABASE_USER = db_settings['USER'],
    DATABASE_PASSWORD = db_settings['PASSWORD'],
    DATABASE_HOST = db_settings['HOST'],
    DATABASE_PORT = db_settings['PORT'],
    #TIME_ZONE = db_settings['TIME_ZONE'],
    )
  from botdisplay_webinterface import botdisplay as bd
  from botdisplay_webinterface.botdisplay import models as bdmodels                  
except ImportError:
  print 'Could not import django settings file to access database.'
  sys.exit(-1)

def local_file(relative_url):
  '''
  :arg relative_url: relative url to local file
  :type relative_url: string (should be path to existing file)
  :returns absolute URL suitable for browser
  '''
  return 'file://'+os.path.abspath(relative_url)


def show_page(browser, url):
  '''
  Drive browser to page url

  :arg browser: instance of selenium webdriver
  :type browser: selenium.webdriver
  :arg url: url to point browser to
  :type url: string

  '''
  browser.get(url)

def timeout(seconds):
  '''
    Simple wrapper for sleep call, meant to be used via concurrency

    :arg seconds: time to sleep in seconds
    :type seconds: int
  '''
  time.sleep(seconds)

def show_page_with_timeout(thread_pool, browser, url, time_to_display):
  '''
  Drive browser to page url for x seconds
  With parallel timer thread killing display if browser.get()
  never completes (due to page not loading?)

  :arg browser: instance of selenium webdriver
  :type browser: selenium.webdriver
  :arg url: url to point browser to
  :type url: string
  :arg time_to_display: time in seconds to display page before completion
  :type time_to_display: float

  '''
  show_page(browser, url)
  timer_future = thread_pool.submit(timeout, time_to_display)

  while not timer_future.done():
    pass

  return time_to_display

def async_show_page_with_timeout(thread_pool, browser, url, time_to_display):
  '''
  Show a page, timing out if it doesn't load or something.
  
  arg: thread_pool: concurrency.threadpool to add tasks to
  arg: browser: selenium browser remote control to manipulate
  arg: url: standard URL to resource appropriate for browser
  arg: time_to_display: time in seconds to keep page up
  '''
  future = thread_pool.submit(show_page_with_timeout, thread_pool, browser, url, time_to_display)
  return future

def update_urls_from_database():
  '''
    Provided we have a Django settings module, we can use it
    to look for an associated database, and return a list of URLs
    from the database.
    arg: settings Django settings.py file that provides database info
    returns: :urls list of URLs from database
    type: :urls list of url strings
  '''
  urls = []
  '''
  urls = [
        local_file('./media/spooky_skeleton_1.gif'),
        'http://nyaa.eu/',
        'http://youtube.googleapis.com/v/a_6CZ2JaEuc&autoplay=1',
        'http://drudgereport.com/',
        local_file('./media/smiling_white_dog.jpg'),
        'http://google.com'
      ]
  '''
  #try to access database and return contents as list
  urls_db = bdmodels.URLDisplay.objects.all()
  urls = []
  for url in urls_db:
    urls.append(url.url)
  return urls
  
def main():
  parser = argparse.ArgumentParser(description='Drive browser via Selenium to N URLs in a cycle.')
  #parser.add_argument('infile', help='Input domain specific text description of C++ structures to generate.')
  parser.add_argument('-v','--verbose', help='Verbose operation. Print status messages during processing', action="store_true")
  #parser.add_argument('-s','--settings', help='Django settings.py file containing database info to drive display',default=None)
  args = parser.parse_args()

  db_settings = {}
   
  #TODO: regex check for youtube links and reformat them as:
  #original link: http://www.youtube.com/v/GsF1jnTjRLo
  #fullscreen autoplaying link: https://youtube.googleapis.com/v/GsF1jnTjRLo%26hd=1%20%26autoplay=1
  #where  '&autoplay=1' specifies autoplay and  '&hd=1' is hd version,
  #and using youtube.googleapis.com goes fullscreen
  urls = update_urls_from_database()

  print 'urls are ' + str(urls)

  #spin off tasks asynchronously
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as thread_pool:
    #browser =  webdriver.chrome()
    browser =  webdriver.Firefox()
  
    while len(urls)>0:
      for url in urls:
        if args.verbose:
          print 'opening ' + url
        show_page(browser, url)
        timeout(30.0)
        #future = async_show_page_with_timeout(thread_pool, browser, url, time_to_display=10.0)
        #while not future.done():
        #  pass#we could be doing something here.
        #at end of page display, updae URL list, detect changes and go back to start on change
        current_urls=set(urls)
        new_urls=update_urls_from_database()
        if len(set(new_urls)-current_urls)>0:
          urls = new_urls
          break

    browser.quit()

    print 'Program exit.'

if __name__ == '__main__':
  main()
