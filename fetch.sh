#! /bin/bash

# fetches summary of a manga from mangahere.com
# $1 - name of the manga (not case sensitive)

. ./globals.sh

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

echo "fetching summary from $SUMMARY_PAGE_URL"
curl $CURL_OPTS "$SUMMARY_PAGE_URL" > "$SUMMARY_PAGE_FILE"

REGEX=$(printf "$SUMMARY_PAGE_URL"; printf "v[0-9]*/c[0-9\.]*/")

mytrace "regex to find chapters urls: $REGEX"

CHAPTER_URLS_FILE=$(printf "$SUMMARY_PAGE_FILE" ; printf "_chapter_urls")

cat "$SUMMARY_PAGE_FILE" | grep -o -E "$REGEX" > "$CHAPTER_URLS_FILE"

URLS=$(tac "$CHAPTER_URLS_FILE")
URLS_COUNT=$(cat "$CHAPTER_URLS_FILE" | wc -l)

mytrace "chapter urls found: $URLS_COUNT"

for URL in $URLS
do
	mytrace "fetching $URL"
	sh fetchChapter.sh "$URL"
done
