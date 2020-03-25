# cord19-rdf

[alt text](screenshot.png "Logo Title Text 1")

```
cd target
Download data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/download
unzip in the target folder (which is in .gitignore)
```

Schema at https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-13/json_schema.txt


```bash
sparql-integrate map-to-graph.sparql | ngs map --sparql extract-bodies.sparql > cord19.trig
```

