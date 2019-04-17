#!/usr/bin/env bash

rm -rf ./.DS_Store
cd ..
tar --exclude **/*.pyc --exclude .git --exclude .idea -zcvf gifshow.tar.gz gifshow