#!/bin/bash

KNRM="\033[0m"
KRED="\033[0;31m"
KGRN="\033[0;32m"
KYEL="\x1B[33m"
KBLU="\033[0;34m"
KMAG="\x1B[35m"
KCYN="\x1B[36m"
KWHT="\x1B[37m"

VERSION='2.3.2'
if [[ -n $1 ]]; then
    VERSION="$1"
fi

#BSURL="http://twitter.github.io/bootstrap/assets/bootstrap.zip"
BSURL="http://getbootstrap.com/$VERSION/assets/bootstrap.zip"

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OLDDIR="$THIS_DIR"

which curl
res=$?

if [[ "$res" != "0" ]]; then
    echo "Please install curl"
    exit 1
fi

echo -e "$KGRN Downloading Bootstrap from $BSURL ...$KNRM"

curl -L -o "/tmp/$$bootstrap.zip"  "$BSURL"

cd "$THIS_DIR"
mkdir -p static
cd static
unzip "/tmp/$$bootstrap.zip"
cd -

# Grab the bootswatch themes
bs_themes="amelia cerulean cosmo cyborg flatly journal readable simplex slate spacelab superhero united"
for theme in $bs_themes ; do
    echo -e "$KGRN Downloading theme $theme ...$KNRM"

    outdir="./static/css/bsthemes/$theme"
    mkdir -p "$outdir"

    curl -L -o  "$outdir/bootstrap.min.css" "http://bootswatch.com/$theme/bootstrap.min.css"
    curl -L -o "$outdir/bootstrap.css" "http://bootswatch.com/$theme/bootstrap.css"
done
