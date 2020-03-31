#!/bin/bash

QUERY="$1"
LIMIT="$2"

curl -G "http://cord19.aksw.org/nli" --data-urlencode "query=$QUERY" --data-urlencode "limit=$LIMIT" | jq -r '.results[].id[]'

