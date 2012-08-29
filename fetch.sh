#! /bin/bash

# fetches summary of a manga from mangahere.com
# $1 - name of the manga (not case sensitive)

SCRIPT_DIR=$(dirname $0)

. $SCRIPT_DIR/globals.sh

BASE_URL="http://www.mangahere.com/manga"

if ! [ "$1" = "" ]
then
	NAME="$1"
	FORMATTED_NAME=$(echo "$1" | sed -e 's/ /_/g' | tr [A-Z] [a-z])
fi

if ! [ -d "$FORMATTED_NAME" ]
then
	mkdir "$FORMATTED_NAME"
fi

SUMMARY_PAGE_URL="$BASE_URL/$FORMATTED_NAME/"
SUMMARY_PAGE_FILE="$FORMATTED_NAME/summary"

mytrace "summary page url: $SUMMARY_PAGE_URL"

mytrace "fetching summary from $SUMMARY_PAGE_URL"
curl $CURL_OPTS "$SUMMARY_PAGE_URL" > "$SUMMARY_PAGE_FILE"

REGEX=$(printf "$SUMMARY_PAGE_URL"; printf "v[0-9]*/c[0-9\.]*/")

mytrace "regex to find chapters urls: $REGEX"

CHAPTER_URLS_FILE=$(printf "$SUMMARY_PAGE_FILE" ; printf "_chapter_urls")

cat "$SUMMARY_PAGE_FILE" | grep -o -E "$REGEX" > "$CHAPTER_URLS_FILE"

URLS=$(tac "$CHAPTER_URLS_FILE")
URLS_COUNT=$(cat "$CHAPTER_URLS_FILE" | wc -l)

mytrace "chapter urls found: $URLS_COUNT"

MY_PROC_COUNT=0
MY_PROC=""

for URL in $URLS
do
	mytrace "running processes: $MY_PROC_COUNT"
	
	while [ $MY_PROC_COUNT -ge $MAX_PROC ]
	do
		sleep 5
		
		
		for PROC in $MY_PROC
		do
			if ! ps -p $PROC > /dev/null
			then
				mytrace "process $PROC terminated"
				MY_PROC=$(echo "$MY_PROC" | sed "s/$PROC //")
				MY_PROC_COUNT=$(echo "$MY_PROC" | wc -w)
			fi
		done
		
		mytrace "running pids: $MY_PROC"
	done

	sh $SCRIPT_DIR/fetchChapter.sh "$URL" &
	NEW_PROC="$!"
	MY_PROC="$NEW_PROC $MY_PROC"
	
	MY_PROC_COUNT=$(echo "$MY_PROC" | wc -w)
	
	mytrace "spawned new process: $NEW_PROC"
done
