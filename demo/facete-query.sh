#!/bin/bash

QUERY="$1"
LIMIT="${2:-100}"

JAR="target/facete3.jar"
FOLDER=`dirname "$JAR"`

mkdir -p "$FOLDER"
[ -f "$JAR" ] || wget -O target/facete3.jar -c 'https://github.com/hobbit-project/facete3/releases/download/facete3-bundle-1.2.0-SNAPSHOT/facete3-bundle-1.2.0-SNAPSHOT-jar-with-dependencies.jar'

# Approach using FILTER
BASE=`curl -G "http://cord19.aksw.org/nli" --data-urlencode "query=$QUERY" --data-urlencode "limit=$LIMIT" |\
  jq -r '.results[].id[]' |\
  awk '{ print "<"$0">" }' |\
  paste -sd "," - |\
  awk '{ print "SELECT ?s { ?s a <http://purl.org/dc/terms/BibliographicResource> . FILTER(?s IN (" $0 ")) }"  }'`

# Note: Using filter alone throws an exception due to invalid algebra
#  awk '{ print "SELECT ?s { ?s ?x ?y FILTER(?s IN (" $0 ")) }"  }'`

# Approach usinge VALUES
#BASE=`curl -G "http://cord19.aksw.org/nli" --data-urlencode "query=$QUERY" --data-urlencode "limit=$LIMIT" |\
#  jq -r '.results[].id[]' |\
#  awk '{ print "( <"$0"> )" }' |\
#  paste -sd " " - |\
#  awk '{ print "SELECT ?s { VALUES (?s) { " $0 " } }"  }'`

echo "Created base concept: $BASE"

# echo "$BASE" > /tmp/tmp.sparql

java -cp target/facete3.jar facete3 -c "$BASE" http://cord19.aksw.org/sparql

