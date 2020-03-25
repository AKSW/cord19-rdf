# cord19-rdf


Download data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/download


```bash
sparql-integrate map-to-graph.sparql | ngs map --sparql extract-bodies.sparql > cord19.trig
```

