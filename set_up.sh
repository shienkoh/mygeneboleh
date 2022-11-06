#!/bin/sh
yes | sudo apt install virtualenv
virtualenv env
env/bin/pip install pandas
env/bin/pip install sklearn