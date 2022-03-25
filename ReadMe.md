# Docker Minecraft Server and Autobackup
This project utilizes [itzg's minecraft docker image](https://hub.docker.com/r/itzg/minecraft-server) to spin up a local Minecraft Java Edition server . It's a fun & simple project to familarize yourself with container technology & cron and it's a great alternative to paying monthly subscription for Minecraft Realms subscription or other SaaS/IaaS fees especially if you live in a household of gamers.

## Create a Minecraft Server
1. ``` cd docker-minecraft-server-autobackup```
2. Modify docker-compose.yml for your host. At minimum, change the volume to a local path on your host. This is where Minecraft will store persistent data for your server. Modify or add any environment variables to suit your needs. For example, xcodegenie is my gamertag, so I set myself as an admin of the server. You can also modify the difficulty of the server, memory used (I recommend to increasing memory for 2x# of expected simulatenous players), and much more. For more options on configuring your minecraft server, refer to [itzg's documentation on github](https://github.com/itzg/docker-minecraft-server/blob/master/README.md)
3. Run the minecraft server ```docker compose up```
4. Open up Minecraft application, select Play > Multiplayer > Add Server, and fill in the IP of host (127.0.0.1 if local) and port in docker-compose.yml
4. Start playing!

If you have trouble connecting:
1. Try connecting on the host, 127.0.0.1:25565
2. Check health of the container - it may still be starting up. ```docker container ls```
3. If you are trying to connect to the server from a host on the network, check that your router isn't blocking access
### Backup your server
Modify [backup.py's](backup.py) configuration variables to suite your needs.

- DOCKER_NAME: The name of your minecraft docker image
- SERVER_PATH: The parent directory of your docker volume
- BACKUP_LENGTH: # of days you would like to store backups locally
- PUSH_TO_GITHUB: Push backup to github (yay free storage!). Must have a .git in the path of backup.py & SSH keys for github oon host

Run with ```python3 ./backup.py```

## How to CronJob
CronJobs are meant for performing regular scheduled actions such as backups, report generation, and so on. Each of those tasks should be configured to recur indefinitely (for example: once a day / week / month). Utilizing Cron on MacOS is similar to Linux since they are both unix-based. The steps below focus on creating a CronJob on MacOS to backup our minecraft server.

Format of a CronJob:
```<minute[*,0–59]>    <hour[*,0–23]>     <dayOfMonth[*,1–31]>     <month[*,1–12]>     <dayOfWeek[*,0–6]>     <shell command>```

Shorthand for CronJobs:
- @reboot         Run once, at startup.
- @yearly         Run once a year, "0 0 1 1 *"
- @annually       (same as @yearly)
- @monthly        Run once a month, "0 0 1 * *"
- @weekly         Run once a week, "0 0 * * 0"
- @daily          Run once a day, "0 0 * * *"
- @midnight       (same as @daily)
- @hourly         Run once an hour, "0 * * * *"

### Autobackup minecraft-server as a CronJob - MacOS instructions

1. Check if you have any existing CronJobs: ```crontab -l```
2. Change the configuration variables in [backup.py](backup.py) to reflect your install & backup needs (See Backup your server)
3. Place your backup.py in a permenant location on your host machine
4. Then, create a new CronJob using the format above: ```crontab -e```

For example, I want my minecraft server to be backed up once a week on Sunday, so my CronJob looks like the following:
```0       0       *       *       0       python3 /Users/meganbailey/Minecraft/minecraft-server/autobackup/backup.py```
