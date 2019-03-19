#!/bin/bash
rsync --progress --exclude ".DS_Store" -avz html/ digitalocean:/usr/local/www/web/appventure4.me/
