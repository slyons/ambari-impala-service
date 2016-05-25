#!/bin/bash

# Use at your own risk, no liability is assumed.

TEMP_DIR=/tmp/impalaservice
TARBALL=https://github.com/slyons/ambari-impala-service/tarball/0.1
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
SERVICEDIR=/var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/IMPALA
SERVICECACHE=/var/lib/ambari-agent/cache/stacks/HDP/$VERSION/services/IMPALA

if [ -e $TEMP_DIR ]; then
    rm -rf $TEMP_DIR
fi

mkdir $TEMP_DIR

curl -L https://github.com/slyons/ambari-impala-service/tarball/0.1 > $TEMP_DIR/impalaservice.tar
tar xvf $TEMP_DIR/impalaservice.tar -C $TEMP_DIR --strip-components=1

if [ -e $SERVICEDIR ]; then
    echo "Removing existing service directory"
    rm -rf $SERVICEDIR
fi
cp -R $TEMP_DIR $SERVICEDIR

if [ -e $SERVICECACHE ]; then
    echo "Removing existing service directory cache"
    rm -r $SERVICECACHE
fi
cp -R $TEMP_DIR $SERVICECACHE

echo "Done, ready to install through Ambari UI"
