#
# Client-side python app for photoapp, this time working with
# web service, which in turn uses AWS S3 and RDS to implement
# a simple photo application for photo storage and viewing.
#
# Project 02 for CS 310
#
# Authors:
#   Jingze Cheng
#   Prof. Joe Hummel (initial template)
#   Northwestern University
#   CS 310
#

import requests  # calling web service
import jsons  # relational-object mapping

import uuid
import pathlib
import logging
import sys
import os
import base64

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img


###################################################################
#
# classes
#
class User:
  userid: int  # these must match columns from DB table
  email: str
  lastname: str
  firstname: str
  bucketfolder: str


class Asset:
  assetid: int  # these must match columns from DB table
  userid: int
  assetname: str
  bucketkey: str


class BucketItem:
  Key: str      # these must match columns from DB table
  LastModified: str
  ETag: str
  Size: int
  StorageClass: str


###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """
  print()
  print(">> Enter a command:")
  print("   0 => end")
  print("   1 => stats")
  print("   2 => users")
  print("   3 => assets")
  print("   4 => download")
  print("   5 => download and display")
  print("   6 => bucket contents")

  cmd = int(input())
  return cmd


###################################################################
#
# stats
#
def stats(baseurl):
  """
  Prints out S3 and RDS info: bucket status, # of users and 
  assets in the database
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/stats'
    url = baseurl + api

    res = requests.get(url)
    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract stats:
    #
    body = res.json()
    #
    print("bucket status:", body["message"])
    print("# of users:", body["db_numUsers"])
    print("# of assets:", body["db_numAssets"])

  except Exception as e:
    logging.error("stats() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# users
#
def users(baseurl):
  """
  Prints out all the users in the database
  
  Parameters
  ----------
  baseurl: baseurl for web service
  
  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/users'
    url = baseurl + api

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract users:
    #
    body = res.json()
    #
    # let's map each dictionary into a User object:
    #
    users = []
    for row in body["data"]:
      user = jsons.load(row, User)
      users.append(user)
    #
    # Now we can think OOP:
    #
    for user in users:
      print(user.userid)
      print(" ", user.email)
      print(" ", user.lastname, ",", user.firstname)
      print(" ", user.bucketfolder)

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
###################################################################
#
# assets
#
def assets(baseurl):
  """
  Prints out all the assets in the database

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    #
    # call the web service:
    #
    api = '/assets'
    url = baseurl + api

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    #
    # deserialize and extract users:
    #
    body = res.json()
    #
    # let's map each dictionary into a Asset object:
    #
    assets = []
    for row in body["data"]:
      asset = jsons.load(row, Asset)
      assets.append(asset)
    #
    # Now we can think OOP:
    #
    for asset in assets:
      print(asset.assetid)
      print(" ", asset.userid)
      print(" ", asset.assetname)
      print(" ", asset.bucketkey)

  except Exception as e:
    logging.error("assets() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
###################################################################
#
# download and display
#
def download_display(baseurl,display=True):
  print("Enter asset id>")
  id=input()
  api = '/download/' + str(id)
  url = baseurl + api
  try:
      res = requests.get(url)

      # Step 3: Handle status codes other than 200
      if res.status_code != 200:
        # failed:
        print("Failed with status code:", res.status_code)
        print("url: " + url)
        if res.status_code == 400:  # we'll have an error message
          body = res.json()
          print("Error message:", body["message"])
        
        return
    # Step 4: Handle a successful response
      body = res.json()
      data = body["data"]
    
      if len(body) == 0:
        print("No such asset...")
      else:
        print("userid: ", body["user_id"])
        print("asset name: ", body["asset_name"])
        print("bucket key: ", body["bucket_key"])
      
      
      
      asset_name = body["asset_name"]

      # Step 5: Decode and write the binary data to a file
      with open(asset_name, "wb") as outfile:
          outfile.write(base64.b64decode(data))
          print(f"Downloaded from S3 and saved as ' {asset_name} '")
  #display
      if display:
        image =img.imread(body["asset_name"])
        plt.imshow(image)
        plt.show()
  except Exception as e:
    logging.error("assets() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


###################################################################
#
# buckets
#
def bucketContent(baseurl):
  try:
    #
    # call the web service:
    #
    api = '/bucket'
    url = baseurl + api

    res = requests.get(url)
   
    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      #
      return

    buckets = res.json()["data"]
    
    while True:

      if len(buckets) == 0:
        break
      
      for bucket in buckets:
        print(bucket["Key"])
        print(" ", bucket["LastModified"])
        print(" ", bucket["Size"])

      user_input = input("another page? [y/n]" + "\n")

      if user_input == "y":
        lastBucketKey = buckets[-1]["Key"]
        bucketUrl = url + '?startafter=' + lastBucketKey
        res = requests.get(bucketUrl)
        buckets = res.json()["data"]
      else:
        break

    return


    
      
      

    # res_data = res.json()["data"]

    # for data in res_data:
    #     print(data.Key)
    #     print()
    

    #
    # deserialize and extract users:
    #
    #from collections import ChainMap
    #body = dict(ChainMap(res.json(), res_next.json()))
    #
    # let's map each dictionary into a Asset object:
    #
    # buckets = []
    # for row in res.json()["data"]:
    #   bucket = jsons.load(row, BucketItem)
    #   buckets.append(bucket)
    # #
    # # Now we can think OOP:
    # #
    # #print(len(buckets))

    # start = 12
    
    # for i in range(0, min(12, len(buckets)), 1):
    #   print(bucket.Key)
    #   print(" ", bucket.LastModified)
    #   print(" ", bucket.Size)

    #   user_input = input("another page? [y/n]"+'\n')
    #   if user_input.lower() != 'y':
    #       break
    #   else:
    #       continue
        

  except Exception as e:
    logging.error("bucketContent() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#########################################################################
# main
#
print('** Welcome to PhotoApp v2 **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'photoapp-client-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-client-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print("**ERROR: config file '", config_file, "' does not exist, exiting")
  sys.exit(0)

#
# setup base URL to web service:
#
configur = ConfigParser()
configur.read(config_file)
baseurl = configur.get('client', 'webservice')

# print(baseurl)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  #
  if cmd == 1:
    stats(baseurl)
  elif cmd == 2:
    users(baseurl)
  elif cmd == 3:
    assets(baseurl)
  elif cmd == 4:
    download_display(baseurl,display=False)
  elif cmd == 5:
    download_display(baseurl,display=True)
  elif cmd == 6:
    bucketContent(baseurl)
  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')
