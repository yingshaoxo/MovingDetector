#!/bin/bash

pull() {
    git fetch --all
    git reset --hard origin/master
}

push() {
    clear
    git add .
    git commit -m "update"
    git push origin
}

clear() {
    rm nohup.out 
    rm app/nohup.out
    rm -fr __pycache__
    rm -fr app/__pycache__
}

if [ "$1" == "pull" ]; then
    pull

elif [ "$1" == "push" ]; then
    push

elif [ "$1" == "clear" ]; then
    clear

elif [ "$1" == "" ]; then
    echo "pull
push
clear"

fi
