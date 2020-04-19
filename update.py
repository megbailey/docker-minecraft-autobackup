import os
import time
import shutil
import hashlib
import time
from datetime import datetime
import logging
import requests
import glob

#docker run -e EULA=TRUE -p 25565:25565 -v /Users/meganbailey/Documents/Minecraft/minecraft-server/data:/data --name minecraft-server itzg/minecraft-server

# CONFIGURATION
DOCKER_NAME = 'minecraft-server'
BACKUP_DIR = '../world_backups' 
LOG_FILENAME = 'world_backups/auto_updater.log'
cserver_fpath = glob.glob('data/minecraft_server*.jar')

logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print('Stopping server..')

os.system('docker stop ' + DOCKER_NAME)

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

backupDateTime = datetime.now().isoformat().replace(':', '-')
backupFileName = "world" + "_backup_" + backupDateTime

backupPath = os.path.join( BACKUP_DIR, backupFileName )
shutil.copytree("../data", backupPath) 
shutil.make_archive(backupPath, 'zip', backupPath)

logging.info(datetime.now().isoformat() + ' : Backed up world and all other files.')



'''
# retrieve version manifest
response = requests.get(MANIFEST_URL)
data = response.json()

if UPDATE_TO_SNAPSHOT:
    minecraft_ver = data['latest']['snapshot']
else:
    minecraft_ver = data['latest']['release']

nserver_name = 'minecraft_server_' + minecraft_ver + '.jar'
nserver_fpath = '../data/' + nserver_name
cserver_fpath = glob.glob('../data/minecraft_server*.jar')[0]

# get checksum of running server 
if os.path.exists(cserver_fpath): #CHANGED
    sha = hashlib.sha1()
    f = open(cserver_fpath, 'rb') #CHANGED
    sha.update(f.read())
    cur_ver = sha.hexdigest()
    print(cur_ver)
else:
    cur_ver = ""

for version in data['versions']:
    if version['id'] == minecraft_ver:
        jsonlink = version['url']
        jar_data = requests.get(jsonlink).json()
        jar_sha = jar_data['downloads']['server']['sha1']

        logging.info('Your sha1 is ' + cur_ver + '. Latest version is ' + str(minecraft_ver) + " with sha1 of " + jar_sha)

        if cur_ver != jar_sha:
            logging.info('Updating server...')
            link = jar_data['downloads']['server']['url']
            logging.info('Downloading .jar from ' + link + '...')
            response = requests.get(link)
            with open(nserver_name, 'wb') as jar_file:
                jar_file.write(response.content)
            logging.info('Downloaded.')
            print('ATTENTION: Server will shutdown for 1 minutes to update in 30 seconds')
            #os.system('screen -S minecraft -X stuff \'say ATTENTION: Server will shutdown for 1 minutes to update in 30 seconds.^M\'')
            logging.info('Shutting down server in 30 seconds.')

            for i in range(20, 9, -10):
                time.sleep(10)
                print('Shutdown in ' + str(i) + ' seconds')
                #os.system('screen -S minecraft -X stuff \'say Shutdown in ' + str(i) + ' seconds^M\'')

            for i in range(9, 0, -1):
                time.sleep(1)
                print('Shutdown in ' + str(i) + ' seconds')
                #os.system('screen -S minecraft -X stuff \'say Shutdown in ' + str(i) + ' seconds^M\'')
            time.sleep(1)

            logging.info('Stopping server.')
            #os.system('screen -S minecraft -X stuff \'stop^M\'')
            time.sleep(5)
            logging.info('Backing up world...')

            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)

            backupPath = os.path.join(
                BACKUP_DIR,
                "world" + "_backup_" + datetime.now().isoformat().replace(':', '-') + "_sha=" + cur_ver)
            shutil.copytree("../data/world", backupPath) #changed

            logging.info('Backed up world.')
            logging.info('Updating server .jar')
            
            if os.path.exists(cserver_fpath): #Changed
                os.remove(cserver_fpath) #Changed 

            os.rename(nserver_name, nserver_fpath) #TODO: Change this
            logging.info('Starting server...')
            os.chdir("..")
            #os.system('screen -S minecraft -d -m java -Xms16G -Xmx16G -jar ' + nserver_name) #TODO: CHANGE THIS

        else:
            logging.info('Server is already up to date.')

        break
'''
