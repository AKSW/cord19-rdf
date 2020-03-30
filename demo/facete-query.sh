#!/bin/bash

QUERY=$1
LIMIT=${2:-10}

mkdir -p target
wget -O target/facete3.jar -c 'https://github.com/hobbit-project/facete3/releases/download/facete3-bundle-1.2.0-SNAPSHOT/facete3-bundle-1.2.0-SNAPSHOT-jar-with-dependencies.jar'

BASE=`curl "http://cord19.aksw.org/nli?query=$QUERY&limit=$LIMIT" | jq -r '.results[].id' | awk '{ print "( <"$0"> )" }' | paste -sd " " - | awk '{ print "SELECT ?s { VALUES (?s) { " $0 " } }"  }'`

echo "Created base concept: $BASE"

java -cp target/facete3.jar facete3 -c "$BASE" http://cord19.aksw.org/sparql

