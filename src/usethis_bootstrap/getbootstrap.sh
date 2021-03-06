#!/bin/bash

KNRM="\033[0m"
KRED="\033[0;31m"
KGRN="\033[0;32m"
KYEL="\x1B[33m"
KBLU="\033[0;34m"
KMAG="\x1B[35m"
KCYN="\x1B[36m"
KWHT="\x1B[37m"

export BS_VERSION='3.3.5'
if [[ -n $1 ]]; then
    BS_VERSION="$1"
fi

export BS_JQ_VERSION='2.1.4'
JQ_BASE_URL="http://code.jquery.com"
JQ_COMPRESSED="jquery-${BS_JQ_VERSION}.min.js"
JQ_DEFLATED="jquery-${BS_JQ_VERSION}.js"

BSURL="https://github.com/twbs/bootstrap/releases/download/v${BS_VERSION}/bootstrap-${BS_VERSION}-dist.zip"

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OLDDIR="$THIS_DIR"

which curl
res=$?

if [[ "$res" != "0" ]]; then
    echo "Please install curl"
    exit 1
fi

rm -fr "$THIS_DIR/static"

echo -e "$KGRN Downloading Bootstrap from $BSURL ...$KNRM"

curl -L -o "/tmp/$$bootstrap.zip"  "$BSURL"

# cd "$THIS_DIR"
mkdir -p static
cd static
unzip "/tmp/$$bootstrap.zip"

if [[ -d  "bootstrap-${BS_VERSION}-dist/" ]]; then
    mv  "bootstrap-${BS_VERSION}-dist/" "bootstrap-${BS_VERSION}/"
else
    mv  "dist/" "bootstrap-${BS_VERSION}/"
fi
cd -

# Get Jquery
mkdir -p "$THIS_DIR/static/bootstrap-$BS_VERSION/js"
curl -L -o  "$THIS_DIR/static/bootstrap-$BS_VERSION/js/$JQ_COMPRESSED" "$JQ_BASE_URL/$JQ_COMPRESSED"
curl -L -o  "$THIS_DIR/static/bootstrap-$BS_VERSION/js/$JQ_DEFLATED" "$JQ_BASE_URL/$JQ_DEFLATED"

# Grab the bootswatch themes
export BSW_API_VERSION=3
export BSW_OUTDIR="$THIS_DIR/static/bootstrap-$BS_VERSION"

$THIS_DIR/getbswatch.py
