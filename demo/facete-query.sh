
QUERY=$1
LIMIT=${2:-10}

BASE=`curl "http://cord19.aksw.org/nli?query=$QUERY&limit=$LIMIT" | jq -r '.results[].id' | awk '{ print "( <"$0"> )" }' | paste -sd " " - | awk '{ print "SELECT ?s { VALUES (?s) { " $0 " } }"  }'`

echo "Created base concept: $BASE"

facete3 -c "$BASE" http://cord19.aksw.org/sparql
