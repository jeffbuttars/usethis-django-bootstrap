#!/bin/bash

KNRM="\033[0m"
KRED="\033[0;31m"
KGRN="\033[0;32m"
KYEL="\x1B[33m"
KBLU="\033[0;34m"
KMAG="\x1B[35m"
KCYN="\x1B[36m"
KWHT="\x1B[37m"

BS_VERSION='3.1.1'
if [[ -n $1 ]]; then
    BS_VERSION="$1"
fi


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

cd "$THIS_DIR"
mkdir -p static
cd static
unzip "/tmp/$$bootstrap.zip"

mv  "bootstrap-${BS_VERSION}-dist/" "bootstrap-${BS_VERSION}/"
rm -fr dist
cd -

export BSW_API_VERSION=3
export BSW_OUTDIR="$THIS_DIR/static/bootstrap-$BS_VERSION/${theme}_css"

./getbswatch.py

# # Grab the bootswatch themes
# bs_themes="amelia cerulean cosmo cupid cyborg flatly journal lumen readable
# simplex slate spacelab superhero united yeti"
# for theme in $bs_themes ; do
#     echo -e "$KGRN Downloading theme $theme ...$KNRM"

#     outdir="$PWD/static/bootstrap-$BS_VERSION/${theme}_css"
#     mkdir -p "$outdir"

#     curl -L -o  "$outdir/bootstrap.min.css" "http://bootswatch.com/$theme/bootstrap.min.css"
#     curl -L -o "$outdir/bootstrap.css" "http://bootswatch.com/$theme/bootstrap.css"
# done
