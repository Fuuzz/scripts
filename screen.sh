#!/bin/bash

set -e

sourcefile=""

while getopts "n:d:f:" arg; do
  case "${arg}" in
    n)
	name=${OPTARG} 
      ;;
    
    d)
	directory=${OPTARG}
      ;;

    f)
	sourcefile=${OPTARG}
      ;;
    *)
	echo "Invalid argument \n
	./screen [-n][-d][-f]
	-n: screen name
	-d: start.sh script directory
	-f: list file for multiple start.sh scripts"
      ;;
  esac
done

shift $((OPTIND -1))

if [ -n "${name}" ] && [ -n "${directory}" ] ; then

	screen -dmS ${name}  bash -c "cd ${directory}; ./start.sh"

else
	if [ -n "${sourcefile}" ] ; then
	
	while IFS=";" read -r directory name;
		do

			screen -dmS ${name}  bash -c "cd ${directory}; ./start.sh"

		done < ${sourcefile}
	fi
fi
