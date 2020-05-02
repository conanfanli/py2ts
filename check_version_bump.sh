#!/bin/bash

PYPI_VERSION=`pip search py2ts| grep '\d+\.\d+.\d+' -E -o`
LOCAL_VERSION=`cat py2ts/__init__.py | grep '\d+\.\d+.\d+' -E -o`

if [[ "$PYPI_VERSION" != "$LOCAL_VERSION" ]]
then
    echo Version is bumped \($LOCAL_VERSION != $PYPI_VERSION\)
    exit 0
else
    echo Version is NOT bumped \($LOCAL_VERSION == $PYPI_VERSION\)
    exit 1
fi
