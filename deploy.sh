#! /bin/sh

DEPLOYDIR="/root/bin"
FILEARRAY="fetcher.py bulkrename.sh"

case $1 in
	"deploy")
		for file in $FILEARRAY
		do
			cp $file "$DEPLOYDIR/"
		done
	;;
	"undeploy")
		for file in $FILEARRAY
		do
			rm "$DEPLOYDIR/$file"
		done
	;;
	* )
		echo "usage: $0 deploy | undeploy"
	;;
esac
