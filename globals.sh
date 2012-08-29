#! /bin/bash

DEBUG=0
CURL_OPTS="-s"
#CURL_OPTS=""

mytrace()
{
	if [ "$DEBUG" -eq 0 ]
	then
		echo "$1"
	fi
}
