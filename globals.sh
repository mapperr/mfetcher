#! /bin/bash

DEBUG=1
LOGLVL=1
CURL_OPTS="-s"
#CURL_OPTS=""

MAX_PROC=8

mytrace()
{
	if [ "$LOGLVL" -eq 0 ]
	then
		MYTS=$(date '+%H:%m:%S')
		printf "\nTRACE - $MYTS - $1"
	fi
}

myinfo()
{
	if [ "$LOGLVL" -eq 1 ]
	then
		printf "\nINFO - $1"
	fi
}
