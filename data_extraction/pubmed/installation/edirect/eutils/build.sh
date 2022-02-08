#!/bin/sh

if [ ! -f "go.mod" ]
then
  go mod init eutils
fi
if [ ! -f "go.sum" ]
then
  go mod tidy
fi

go build
