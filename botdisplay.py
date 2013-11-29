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
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time
import argparse
#import threading
#import time
import concurrent.futures


driver = None

def close():
  global driver
  print 'About to try closing browser.'
  if driver:
    print 'Attempting to close browser.'
    driver.quit()
    driver = None

def show_page(browser, url, time_to_display=30.0):
  '''
  Drive browser to page url for x seconds

  :arg browser: instance of selenium webdriver
  :type browser: selenium.webdriver
  :arg url: url to point browser to
  :type url: string
  :arg time_to_display: time in seconds to display page before completion
  :type time_to_display: float

  '''
  browser.get(url)
  time.sleep(time_to_display)
  print('Showed {} for {} seconds'.format(url, time_to_display))
  return sleepTime

def async_show_page(thread_pool, browser, url, time_to_display=30.0):
  '''
  Drive browser to page asynchronously

  TODO: this could be revised to be method decorator

  :returns concurrency.future of task completion
  '''
  future = thread_pool.submit(show_page, browser, url, time_to_display)
  return future
  
def main():
  #TODO: move towards DB driven list of urls and other events
  #TODO: embed in cyclone(?) web app framework
  urls = [
      'http://nyaa.eu/',
      'http://drudgereport.com/',
      'http://google.com'
    ]

  #spin off tasks asynchronously
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as thread_pool:
    #browser =  webdriver.chrome()
    browser =  webdriver.Firefox()
  
    for url in urls:
      future = async_show_page(thread_pool, browser, url, time_to_display=10.0)
      while future.running():
        pass#we could be doing something here.

    browser.quit()

    print 'Program exit.'

if __name__ == '__main__':
  main()
