# cord19-rdf

```
cd target
Download data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/download
unzip in the target folder (which is in .gitignore)
```


```bash
sparql-integrate map-to-graph.sparql | ngs map --sparql extract-bodies.sparql > cord19.trig
```

