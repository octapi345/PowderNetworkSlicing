#!/bin/sh

set -x

SETUPDIR=`dirname $0`

. $SETUPDIR/setup-common.sh

if [ ! -d $OURDIR ]; then
    mkdir -p $OURDIR
fi

if [ -f $OURDIR/setup-asn1c-done ]; then
    echo "setup-asn1c already ran; not running again"
    exit 0
fi

#logtstart "asn1c"

cd $OURDIR
rm -rf $OURDIR/asn1c
# GIT_SSL_NO_VERIFY=true
git clone https://gitlab.eurecom.fr/oai/asn1c.git
cd asn1c
# better to use a given commit than a branch in case the branch
# is updated and requires modifications in the source of OAI
#git checkout velichkov_s1ap_plus_option_group
git checkout f12568d617dbf48497588f8e227d70388fa217c9
autoreconf -iv
./configure
make -j`nproc`
$SUDO make install
cd ..
$SUDO ldconfig

#logtend "asn1c"

touch $OURDIR/setup-asn1c-done
