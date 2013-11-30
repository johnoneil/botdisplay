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
  
def main():
  #TODO: move towards DB driven list of urls and other events
  #TODO: embed in cyclone(?) web app framework
  #TODO: regex check for youtube links and reformat them as:
  #original link: http://www.youtube.com/v/GsF1jnTjRLo
  #fullscreen autoplaying link: https://youtube.googleapis.com/v/GsF1jnTjRLo%26hd=1%20%26autoplay=1
  #where  '&autoplay=1' specifies autoplay and  '&hd=1' is hd version,
  #and using youtube.googleapis.com goes fullscreen
  urls = [
      #'http://192.168.1.3/',
      local_file('./media/spooky_skeleton_1.gif'),
      'http://nyaa.eu/',
      'http://youtube.googleapis.com/v/a_6CZ2JaEuc&autoplay=1',
      'http://drudgereport.com/',
      local_file('./media/smiling_white_dog.jpg'),
      'http://google.com'
    ]

  #spin off tasks asynchronously
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as thread_pool:
    #browser =  webdriver.chrome()
    browser =  webdriver.Firefox()
  
    for url in urls:
      print 'opening ' + url
      future = async_show_page_with_timeout(thread_pool, browser, url, time_to_display=10.0)
      while not future.done():
        pass#we could be doing something here.

    browser.quit()

    print 'Program exit.'

if __name__ == '__main__':
  main()
