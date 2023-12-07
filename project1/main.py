#
# Main program for photoapp program using AWS S3 and RDS to
# implement a simple photo application for photo storage and
# viewing.
#
# Authors:
#   Jingze Cheng
#   Prof. Joe Hummel (initial template)
#   Northwestern University
#   Fall 2023
#

import datatier  # MySQL database access
import awsutil  # helper functions for AWS
import boto3  # Amazon AWS

import uuid
import pathlib
import logging
import sys
import os

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img


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
  print("   6 => upload")
  print("   7 => add user")

  cmd = int(input())
  return cmd


###################################################################
#
# stats
#
def stats(bucketname, bucket, endpoint, dbConn):
  """
  Prints out S3 and RDS info: bucket name, # of assets, RDS 
  endpoint, and # of users and assets in the database
  
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """
  #
  # bucket info:
  #
  print("S3 bucket name:", bucketname)

  assets = bucket.objects.all()
  print("S3 assets:", len(list(assets)))

  #
  # MySQL info:
  #
  print("RDS MySQL endpoint:", endpoint)

  #number of users
  users_sql="SELECT COUNT(*) FROM users;"
  users_num=datatier.retrieve_one_row(dbConn, users_sql)
  if users_num:
    print("# of users:", users_num[0])
  #number of assets
  assets_sql="SELECT COUNT(*) FROM assets;"
  assets_num=datatier.retrieve_one_row(dbConn, assets_sql)
  if assets_num:
    print("# of assets:", assets_num[0])

  
  # sql = """
  
  # select now();

  
  # """

  # row = datatier.retrieve_one_row(dbConn, sql)
  # if row is None:
  #   print("Database operation failed...")
  # elif row == ():
  #   print("Unexpected query failure...")
  # else:
  #   print(row[0])

###################################################################
#
# users
#
def users(dbConn):
  """
  retrieves and outputs the users in the users table. The users are     
  output in descending order by user id

  Parameters
  ----------
  dbConn: open connection to MySQL server
  """
  
  users_sql="SELECT userid, email, lastname, firstname, bucketfolder From users ORDER BY userid DESC;"
  #retrieve users
  users=datatier.retrieve_all_rows(dbConn, users_sql)
  #Check if users in database
  if not users:
    print("No users in database.")
    return 
  #Output users
  for user in users:
    userid = user[0]
    email = user[1]
    lastname = user[2]
    firstname = user[3]
    bucketfolder = user[4]
    print(f"User id: {userid}\n  Email: {email}\n  Name: {lastname} , {firstname}\n  Folder: {bucketfolder} ")
    
  
###################################################################
#
# assets
#
def assets(dbConn):
  """
  retrieves and outputs the assets in the assets table. The assets are    
  output in descending order by asset id

  Parameters
  ----------
  dbConn: open connection to MySQL server
  """
  assets_sql="SELECT assetid, userid, assetname, bucketkey From assets ORDER BY assetid DESC;"
  #retrieve assets
  assets=datatier.retrieve_all_rows(dbConn, assets_sql)
  #Check if assets in database
  if not assets:
    print("No assets in database.")
    return 
  #Output assets
  for asset in assets:
    assetid = asset[0]
    userid = asset[1]
    assetname = asset[2]
    bucketkey = asset[3]
    
    print(f"Asset id: {assetid}\n User id: {userid}\n Original name: {assetname}\n Key name: {bucketkey} ")


###################################################################
#
# download and display
#
def download_display(dbConn,display=True):
  print("Enter asset id>")
  id=input()
  assets_sql="SELECT assetname, bucketkey From assets where assetid = %s;"

  assets=datatier.retrieve_all_rows(dbConn, assets_sql, [id])
  
  if len(assets) == 0:
    print("No such asset...")
  else:
    #print(assets)
    key=assets[0][1]
    filename=awsutil.download_file(bucket, key)
    # testname = "test01.jpg"
    os.rename(filename,assets[0][0])
    print("Downloaded from S3 and saved as "+ "' " + assets[0][0] + " '")
    
    if display:
      image =img.imread(assets[0][0])
      plt.imshow(image)
      plt.show()
    

###################################################################
#
# upload
#
def upload(dbConn): 
  local_file=input("Enter local filename>").strip()
  if not os.path.exists(local_file):
    print("Local file" ,local_file, "does not exist.")
    return
  user_id=input("Enter user id>")
  users_sql="""SELECT bucketfolder From users WHERE userid=%s;"""
  users=datatier.retrieve_all_rows(dbConn, users_sql, [user_id])
  
  if len(users)==0:
    print("No such user")
    return
  
  key=users[0][0]+"/"+str(uuid.uuid4())+local_file[-4:]
  key=awsutil.upload_file(local_file, bucket, key)
  if key is None:
    print("Upload failed.")
    return
  upload_sql="""INSERT INTO assets (userid, assetname, bucketkey)
VALUES (%s, %s, %s);"""
  assets=datatier.perform_action(dbConn, upload_sql, [user_id,local_file, key])
  if assets != -1:
    sql = """SELECT LAST_INSERT_ID();"""
    new_asset=datatier.retrieve_one_row(dbConn,sql)
    print(new_asset[0])
  else:
    return
    
  
  

###################################################################
#
# add user
#
def add_user(dbConn):
  print("Enter user's email>")
  user_email=input()
  print("Enter user's last (family) name>")
  user_lastname=input()
  print("Enter user's first (given) name>")
  user_firstname=input()
  filename = str(uuid.uuid4())

 
  user_sql="""INSERT INTO users (email, lastname, firstname, bucketfolder) VALUES (%s,%s,%s,%s);"""
  datatier.perform_action(dbConn, user_sql, [user_email,user_lastname,user_firstname,filename])
  sql="""SELECT LAST_INSERT_ID();"""
  newuser=datatier.retrieve_one_row(dbConn, sql)
  print("Recorded in RDS under user id"+str(newuser[0]))
  


  
#########################################################################
# main
#
print('** Welcome to PhotoApp **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'photoapp-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-config.ini),")
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
# gain access to our S3 bucket:
#
s3_profile = 's3readwrite'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

boto3.setup_default_session(profile_name=s3_profile)

configur = ConfigParser()
configur.read(config_file)
bucketname = configur.get('s3', 'bucket_name')

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketname)


#
# now let's connect to our RDS MySQL server:
#
endpoint = configur.get('rds', 'endpoint')
portnum = int(configur.get('rds', 'port_number'))
username = configur.get('rds', 'user_name')
pwd = configur.get('rds', 'user_pwd')
dbname = configur.get('rds', 'db_name')

dbConn = datatier.get_dbConn(endpoint, portnum, username, pwd, dbname)

if dbConn is None:
  print('**ERROR: unable to connect to database, exiting')
  sys.exit(0)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  #
  if cmd == 1:
    stats(bucketname, bucket, endpoint, dbConn)
  elif cmd==2:
    users(dbConn)
  elif cmd==3:
    assets(dbConn)
  elif cmd==4:
    download_display(dbConn,display=False)
  elif cmd==5:
    download_display(dbConn,display=True)
  elif cmd==6:
    upload(dbConn)
  elif cmd==7:
    add_user(dbConn)
  #
  # TODO
  #
  #
  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')
