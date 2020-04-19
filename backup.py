import os
import time
import shutil
import time
import datetime
from datetime import datetime, timedelta, date
import logging
import glob

#docker run -e EULA=TRUE -p 25565:25565 -v /Users/meganbailey/Documents/Minecraft/minecraft-server/data:/data --name minecraft-server itzg/minecraft-server

# CONFIGURATION
DOCKER_NAME = 'minecraft-server'
BACKUP_DIR = '../world_backups' 
ZIP_BACKUP_DIR = BACKUP_DIR + '/zipped_backups' 
BACKUP_LENGTH = 1 #days until the backup folder is deleted
LOG_FILENAME = 'world_backups/auto_updater.log'
cserver_fpath = glob.glob('data/minecraft_server*.jar')


print('\n------------------ RUNNING BACKUP ------------------\n')
logging.info(datetime.now().isoformat() + ' : ----------------- RUNNING BACKUP ------------------') 


logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


print('\nSTOPPING SERVER\n')
logging.info(datetime.now().isoformat() + ' : Stopping Server')


os.system('docker stop ' + DOCKER_NAME)


#Creating directories that may not exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)
if not os.path.exists(ZIP_BACKUP_DIR):
    os.makedirs(ZIP_BACKUP_DIR)


backupDateTime = datetime.now().isoformat()
backupFileName = "world" + "_backup_" + backupDateTime
backupPath = os.path.join( BACKUP_DIR, backupFileName )
newBackupPathZips = os.path.join( BACKUP_DIR, 'zipped_backups', backupFileName + '.zip' )

shutil.copytree("../data", backupPath) 
zippedLocation = shutil.make_archive(backupPath, 'zip')

os.rename(zippedLocation, newBackupPathZips)


print('\n' + datetime.now().isoformat() + ' : Backed up world and all other files.\n')
logging.info(datetime.now().isoformat() + ' : Backed up world and all other files.')

#Removing folder backups longer than a specified number of days
results = os.popen('find "../world_backups" -name "world_backup*-*.*" -type d').read().split('\n')

for name in results:
    if os.path.exists(name):
        creationDateTime = datetime.fromisoformat(name.split('_')[3])
        difference = datetime.utcnow() - creationDateTime
        #if difference.days > BACKUP_LENGTH:
            #os.remove(name)
