#!/bin/sh

set -x

SETUPDIR=`dirname $0`

. $SETUPDIR/setup-common.sh

if [ ! -d $OURDIR ]; then
    mkdir -p $OURDIR
fi

if [ -f $OURDIR/setup-e2-bindings-done ]; then
    echo "setup-e2-bindings already ran; not running again"
    exit 0
fi

#logtstart "e2-bindings"

if [ ! -e $OURDIR/E2AP-v01.00-generated-bindings.tar.gz ]; then
    wget -O $OURDIR/E2AP-v01.00-generated-bindings.tar.gz \
        https://www.emulab.net/downloads/johnsond/profile-oai-oran/E2AP-v01.00-generated-bindings.tar.gz
    tar -xzvf $OURDIR/E2AP-v01.00-generated-bindings.tar.gz -C $OURDIR
fi
if [ ! -e $OURDIR/E2AP-v01.01-generated-bindings.tar.gz ]; then
    wget -O $OURDIR/E2AP-v01.01-generated-bindings.tar.gz \
        https://www.emulab.net/downloads/johnsond/profile-oai-oran/E2AP-v01.01-generated-bindings.tar.gz
    tar -xzvf $OURDIR/E2AP-v01.01-generated-bindings.tar.gz -C $OURDIR
fi
if [ ! -e $OURDIR/E2SM-KPM-generated-bindings.tar.gz ]; then
    wget -O $OURDIR/E2SM-KPM-generated-bindings.tar.gz \
        https://www.emulab.net/downloads/johnsond/profile-oai-oran/E2SM-KPM-generated-bindings.tar.gz
    tar -xzvf $OURDIR/E2SM-KPM-generated-bindings.tar.gz -C $OURDIR
fi
if [ ! -e $OURDIR/E2SM-NI-generated-bindings.tar.gz ]; then
    wget -O $OURDIR/E2SM-NI-generated-bindings.tar.gz \
        https://www.emulab.net/downloads/johnsond/profile-oai-oran/E2SM-NI-generated-bindings.tar.gz
    tar -xzvf $OURDIR/E2SM-NI-generated-bindings.tar.gz -C $OURDIR
fi
if [ ! -e $OURDIR/E2SM-GNB-NRT-generated-bindings.tar.gz ]; then
    wget -O $OURDIR/E2SM-GNB-NRT-generated-bindings.tar.gz \
        https://www.emulab.net/downloads/johnsond/profile-oai-oran/E2SM-GNB-NRT-generated-bindings.tar.gz
    tar -xzvf $OURDIR/E2SM-GNB-NRT-generated-bindings.tar.gz -C $OURDIR
fi

#logtend "e2-bindings"

touch $OURDIR/setup-e2-bindings-done
