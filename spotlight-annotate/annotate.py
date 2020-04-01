import requests
import json
import os
import rdflib
#import rdfextras
import hashlib
from rdflib import Graph, Dataset, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD

dictionary = dict(
    cord19_Doc='http://cord19.aksw.org/resource/document-',
    cord19_Tit='http://cord19.aksw.org/resource/title',
    cord19_Ab='http://cord19.aksw.org/resource/abstract',
    nif='http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#',
    its='http://www.w3.org/2005/11/its/rdf#',
    dct='http://purl.org/dc/terms/',
    res='http://cord19.aksw.org/resource/',
    dul='http://www.loa-cnr.it/ontologies/DUL.owl#',
    wd='http://www.wikidata.org/entity/',
    schema='http://schema.org/',
    dbo='http://dbpedia.org/ontology/'
    )

ds=Dataset()

def main():
    counter=0
    collection='biorxiv_medrxiv'
    targetDir='../target'
    fileDir=targetDir+'/'+collection
    for file in os.listdir(fileDir):
        counter=counter+1
        print(counter)
        with open(fileDir+'/'+file) as json_file:
            data=json.load(json_file)
            paperGraph=Graph(identifier=URIRef('http://cord19.aksw.org/resource/document-'+data['paper_id']))
            setNS(paperGraph)
            # Go through title and abstract
            for x in range(0, 2):
                if x == 1:
                    search=data['metadata']['title']
                    searchType='title'
                    searchPref='cord19_Tit'
                else:
                    if len(data['abstract']) > 0:
                        search=data['abstract'][0]['text']
                        searchType='abstract'
                        searchPref='cord19_Ab'
                body={'text': search,'confidence':'0.8'}
                headers={'Accept': 'application/json'}
                url='http://api.dbpedia-spotlight.org/de/annotate'
                response=requests.get(url,params=body,headers=headers)
                if response.status_code == 200:
                    jsonObj=json.dumps(response.json())
                    loaded=json.loads(jsonObj)
                    addData(loaded,search,searchType,searchPref,paperGraph)
            ds.serialize(destination=targetDir+'/'+collection+'-title_abstract', format='trig')

def addData(json,search,searchType,searchPref,paperGraph):
    hash=hashlib.sha256(str(search).encode('utf-8'))
    hashStr=hash.hexdigest()
    if 'Resources' in json:
        for obj in json['Resources']:
            dbpediaURL=obj['@URI']
            surfaceForm=obj['@surfaceForm']
            beginIndex=search.find(str(surfaceForm))
            endIndex=beginIndex+len(surfaceForm)
            annotationURI=URIRef(getURI(paperGraph, 'res')+searchType+'-'+hashStr+'#char'+str(beginIndex)+','+str(endIndex))
            paperGraph.add((annotationURI, RDF.type, URIRef(getURI(paperGraph,'nif')+'EntityOccurrence')))
            paperGraph.add((annotationURI, RDF.type, URIRef(getURI(paperGraph,'nif')+'Phrase')))
            paperGraph.add((annotationURI, RDFS.label,Literal(surfaceForm, lang='en')))
            paperGraph.add((annotationURI, URIRef(getURI(paperGraph,'nif')+'anchorOf'), Literal(surfaceForm, lang='en')))
            paperGraph.add((annotationURI, URIRef(getURI(paperGraph,'nif')+'beginIndex'), Literal(beginIndex, datatype=XSD.nonNegativeInteger)))
            paperGraph.add((annotationURI, URIRef(getURI(paperGraph,'nif')+'endIndex'), Literal(endIndex, datatype=XSD.nonNegativeInteger)))
            paperGraph.add((annotationURI, URIRef(getURI(paperGraph,'nif')+'referenceContext'), URIRef(getURI(paperGraph,searchPref)+'-'+hashStr)))
            paperGraph.add((annotationURI, URIRef(getURI(paperGraph,'its')+'taIdentRef'), URIRef(dbpediaURL)))
            types=obj['@types'].split(',')
            if types[0] != '':
                for type in types:
                    splittedType=type.split(':')
                    switchStr=splittedType[0]
                    typePart=splittedType[1]
                    ns=None
                    if switchStr == 'DBpedia':
                        ns=getURI(paperGraph,'dbo')
                    elif switchStr == 'Schema':
                        ns=getURI(paperGraph,'schema')
                    elif switchStr == 'Wikidata':
                        ns=getURI(paperGraph,'wd')
                    if ns is not None:
                        paperGraph.add((annotationURI, URIRef(getURI(paperGraph,'its')+'taClassRef'), URIRef(ns+typePart)))
        ds.graph(paperGraph)

def setNS(graph):
    for k, v in dictionary.items():
        graph.namespace_manager.bind(k, URIRef(v),override=False)

def getURI(graph, prefixStr):
    for prefix, URI in graph.namespace_manager.namespaces():
        if prefix == prefixStr:
            return URI

main()
