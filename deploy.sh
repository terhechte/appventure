#!/bin/bash
#rsync --progress --exclude ".DS_Store" -avz html/ digitalocean:/usr/local/www/web/appventure4.me/
rsync --progress --exclude ".DS_Store" -avz html/ root@165.227.254.111:/usr/local/www/web/appventure4.me/
