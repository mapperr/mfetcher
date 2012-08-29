#! /bin/bash

# fetches a chapter of a manga from mangahere.com
# $1 - url of the chapter

SCRIPT_DIR=$(dirname $0)

. $SCRIPT_DIR/globals.sh

URL="$1"
COUNTER=1
URL_EXISTS=0

NAME=$(printf "$URL" | grep -o -E "manga/[a-z_]*" | sed 's/manga\///g' )

if ! [ -d "$NAME" ]
then
	mkdir "$NAME"
fi

CHAPTER_NUMBER=$(printf "$URL" | grep -o -E "/c[0-9\.]*" | tr -d "/")

#( debug
	i=0
#) debug

while [ "$URL_EXISTS" -eq "0" ]
do
	IMG_FILE=$(printf "$NAME/" ; printf "$CHAPTER_NUMBER" ; printf "_" ; printf "$COUNTER" | sed -e 's/\b[0-9]\b/00&/' -e 's/\b[0-9][0-9]\b/0&/' ; printf ".jpg")
	
	PAGE_URL=$(printf "$URL" ; printf "$COUNTER.html")
	
	if [ $COUNTER -eq 1 ]
	then
		PAGE_URL="$URL"
	fi
	
	mytrace "page url is: $PAGE_URL"
	
	IMG_URL=$(curl $CURL_OPTS "$PAGE_URL" | grep -o -E 'src="http://c.mhcdn.net/store/manga/[0-9]*/[0-9\.\-]*/compressed/.*\.jpg"' | grep -v cover | tr -d '"' | sed 's/src=//g')
	
	mytrace "fetching $IMG_FILE from $IMG_URL"

	if [ $DEBUG -eq 0 ]
	then
		URL_EXISTS=0
		if [ $i -ge 5 ]
		then
			URL_EXISTS=1
		fi
		i=$(expr $i + 1)
	else
		curl $CURL_OPTS "$IMG_URL" > "$IMG_FILE"
		URL_EXISTS="$?"
	fi

	if [ $URL_EXISTS -ne 0 ]
	then
		if [ -f "$IMG_FILE" ]
		then
			rm -f "$IMG_FILE"
		fi
	fi
	
	COUNTER=$(expr $COUNTER + 1)
done

myinfo "fetched chapter $CHAPTER_NUMBER"
