import os
import shutil
import time
import datetime
from datetime import datetime, timedelta, date
import logging
import glob

# CONFIGURATION
DOCKER_NAME = 'minecraft-server'
BACKUP_DIR = '../world_backups' 
SERVER_PATH = '/Users/meganbailey/Documents/Minecraft/minecraft-server/'
PUSH_TO_GITHUB = True
ZIP_BACKUP_DIR = BACKUP_DIR + '/zipped_backups' 
BACKUP_LENGTH = 7 #days until the backup folder is deleted
LOG_FILENAME = 'world_backups/auto_updater.log'
cserver_fpath = glob.glob('data/minecraft_server*.jar')


print('\n---------------------------------------- STARTING BACKUP ----------------------------------------\n')
logging.info(datetime.now().isoformat() + ' : ----------------------------------------STARTING BACKUP ----------------------------------------') 


logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def removeOldBackups():
    print('\n' + datetime.now().isoformat()  + ' : Reviewing backups for removal. Backup(s) will be deleted if older than ' + str(BACKUP_LENGTH) + ' day(s)')
    logging.info(datetime.now().isoformat() + ' : Reviewing backups for removal. Backup(s) will be deleted if older than ' + str(BACKUP_LENGTH) + ' day(s)')

    #Removing folder backups longer than a specified number of days
    results = os.popen('find "../world_backups" -name "world_backup*-*.*" -type d').read().split('\n')
    removal_count = 0

    for backup_name in results:
        if os.path.exists(backup_name):
            creationDateTime = datetime.fromisoformat(backup_name.split('_')[3])
            difference = datetime.utcnow() - creationDateTime
            if difference.days > BACKUP_LENGTH:
                shutil.rmtree(backup_name)
                removal_count += 1

    print(str(removal_count) + " server backup(s) have been deleted")



def backupWorld():
    #Creating directories that may not exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    if not os.path.exists(ZIP_BACKUP_DIR):
        os.makedirs(ZIP_BACKUP_DIR)

    #os.system('docker container restart ' + DOCKER_NAME)

    backupDateTime = datetime.now().isoformat()
    backupFileName = "world" + "_backup_" + backupDateTime
    backupPath = os.path.join( BACKUP_DIR, backupFileName )
    newBackupPathZips = os.path.join( BACKUP_DIR, 'zipped_backups', backupFileName + '.zip' )

    shutil.copytree("../data", backupPath) 
    zippedLocation = shutil.make_archive(backupPath, 'zip')

    os.rename(zippedLocation, newBackupPathZips)


    print('\n' + datetime.now().isoformat()  + ' : Backed up world and all other files. ' + backupFileName + ' created.')
    logging.info(datetime.now().isoformat()  + ' : Backed up world and all other files. ' + backupFileName + ' created.')


def pushToGithub():
    #Push to github all files
    os.chdir(SERVER_PATH)
    if PUSH_TO_GITHUB and os.path.exists('.git'):
        os.system('git add .')
        os.system('git commit -m " AUTOBACKUP:' + datetime.now().isoformat()+ '"')
        os.system('git push')
    elif PUSH_TO_GITHUB:
        print('Cannot find a .git. Ensure you have a .git at the following location: ' +  SERVER_PATH)
    else: 
        print('If you would like to have the script push the sever and backups to github, please set the configuration variable PUSH_TO_GITHUB to True and ensure you have a .git at the following location: ' +  SERVER_PATH)

        
def notifyServer():
    #print('\nRestarting Server\n')
    #logging.info(datetime.now().isoformat() + ' : Restarting Server')
    os.system('docker exec minecraft-server rcon-cli say ATTENTION: Server will shutdown soon to update.')
    time.sleep(60)
    os.system('docker exec minecraft-server rcon-cli say ATTENTION: Server will shutdown in 1 minute and 30 seconds.')
    time.sleep(30)
    os.system('docker exec minecraft-server rcon-cli say Server will shutdown in 1 minute')
    time.sleep(30)
    os.system('docker exec minecraft-server rcon-cli say Server will shutdown in 30 seconds')
    time.sleep(20)

    for i in range(10, 0, -1):
        time.sleep(1)
        os.system('docker exec minecraft-server rcon-cli say Server will shutdown in ' + str(i) + ' seconds')