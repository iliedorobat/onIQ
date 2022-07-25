from ro.webdata.oniq.endpoint.namespace import NAMESPACE

DBP_ENDPOINT = "https://dbpedia.org/sparql/"
DBP_LIMIT = 5000
DBP_OFFSET = 5000


DBO_CATEGORIES_QUERY = f"""
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX skos: <{NAMESPACE.SKOS}>

    SELECT *
    WHERE {{
        SELECT DISTINCT ?class ("" as ?label)
        WHERE {{
            ?class rdf:type skos:Concept .
            # OPTIONAL {{
            #     ?class rdfs:label ?label .
            #     FILTER(langMatches(lang(?label), "en"))
            # }}
        }}
        ORDER BY ?class
    }}
    LIMIT {DBP_LIMIT}
    OFFSET %d
"""
"""
SPARQL query for getting categories
DBpedia restricts up to 5000 items (DBP_LIMIT) from a single query.

# https://stackoverflow.com/questions/50526921/10000-row-dbpedia-query-result-set-size-limit
# https://stackoverflow.com/questions/20937556/how-to-get-all-companies-from-dbpedia
"""


DBO_CATEGORIES_COUNTER_QUERY = f"""
    PREFIX skos: <{NAMESPACE.SKOS}>

    SELECT DISTINCT count(?class) as ?counter
    WHERE {{
        ?class ?p skos:Concept
    }}
"""
"""
SPARQL query for getting the number of categories in the repository.
"""


# TODO: remove "?namespace" as it is extracted from the uri
DBO_CLASSES_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX dbo: <{NAMESPACE.DBP_ONTOLOGY}>
    PREFIX owl: <{NAMESPACE.OWL}>
    
    SELECT DISTINCT ?class ?subclassOf ?label ?namespace
    WHERE {{
        {{
            ?class  rdf:type owl:Class ;
                    rdfs:subClassOf ?subclassOf ;
                    rdfs:label ?label .
            FILTER(langMatches(lang(?label), "en"))
            bind(dbo: as ?namespace)
        }} UNION {{
            ?s rdf:type ?class . 
            FILTER (?class = owl:Thing)
            bind(owl:Class as ?subclassOf)
            bind("Thing" as ?label)
            bind(owl: as ?namespace)
        }}
    }}
    ORDER BY ?class
"""
"""
SPARQL query for getting the list of classes.
# TODO: "rdfs:isDefinedBy ?namespace ."
"""


# TODO: remove "?namespace" as it is extracted from the uri
DBO_MAIN_CLASSES_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX dbo: <{NAMESPACE.DBP_ONTOLOGY}>
    PREFIX owl: <{NAMESPACE.OWL}>
    
    SELECT DISTINCT ?class ?label ?subclassOf ?namespace
    WHERE {{
        {{
            ?class  rdf:type owl:Class ;
                    rdfs:subClassOf ?subclassOf ;
                    rdfs:label ?label .
            FILTER(?subclassOf = owl:Thing) .
            FILTER(langMatches(lang(?label), "en"))
            bind(dbo: as ?namespace)
        }} UNION {{
            ?s rdf:type ?class .
            FILTER (?class = owl:Thing)
            bind(owl:Class as ?subclassOf)
            bind("Thing" as ?label)
            bind(owl: as ?namespace)
        }}
    }}
    ORDER BY ?class
"""
"""
SPARQL query for getting the list of main classes.
The "main class" is a class for which "http://www.w3.org/2002/07/owl#Thing" is its parent.
"""


DBO_PROPERTIES_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX dbo: <{NAMESPACE.DBP_ONTOLOGY}>
    
    SELECT DISTINCT ?property ?label ?subclassOf ?domain ?range
    WHERE {{
        ?property   rdf:type ?subclassOf ;
                    rdfs:label ?label .

        OPTIONAL {{ ?property rdfs:domain ?domain }} .
        OPTIONAL {{ ?property rdfs:range ?range }} .

        FILTER(?subclassOf = rdf:Property) .
        FILTER(langMatches(lang(?label), "en")) .
        FILTER(strStarts(str(?property), str(dbo:)))
    }}
    ORDER BY ?property
"""
"""
SPARQL query for getting the list of properties.
"""



DBP_PROPERTIES_OF_RESOURCE_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX dbr: <{NAMESPACE.DBP_RESOURCE}>

    SELECT DISTINCT ?property ?label ?subclassOf ?domain ?range
    WHERE {{
        dbr:%s ?property ?value .

        OPTIONAL {{
            ?property rdfs:label ?label .
            FILTER(langMatches(lang(?label), "en"))
        }}

        OPTIONAL {{
            ?property rdf:type ?subclassOf .
            FILTER(?subclassOf = rdf:Property or !bound(?subclassOf))
        }}

        OPTIONAL {{ ?property rdfs:domain ?domain }}
        OPTIONAL {{ ?property rdfs:range ?range }}

        FILTER(
            ?property NOT IN (rdf:type, rdfs:subPropertyOf, rdfs:subClassOf)
        )
    }}
    ORDER BY ?property
"""
"""
SPARQL query for getting the list of properties for a specific resource.
E.g.: dbr:%s => http://dbpedia.org/resource/Barda_Mausoleum
"""


DBP_ENTITY_TYPE_QUERY = f"""
    PREFIX dbo: <{NAMESPACE.DBP_ONTOLOGY}>
    PREFIX foaf: <{NAMESPACE.FOAF}>
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>

    SELECT *
    WHERE {{
        SELECT DISTINCT ?resource ?label ?name
        WHERE {{
            ?resource   rdf:type dbo:%s ;
                        rdfs:label ?label .
            FILTER(langMatches(lang(?label), "en"))
    
            OPTIONAL {{ ?resource foaf:name ?name }}
        }}
        ORDER BY ?resource
    }}
    LIMIT {DBP_LIMIT}
    OFFSET %d
"""
"""
SPARQL query for getting entities.
E.g.:
    - dbo:%s => http://dbpedia.org/ontology/Place
    - %d => 0; 5000; etc.

DBpedia restricts up to 5000 items (DBP_LIMIT) from a single query.

# https://stackoverflow.com/questions/50526921/10000-row-dbpedia-query-result-set-size-limit
# https://stackoverflow.com/questions/20937556/how-to-get-all-companies-from-dbpedia
"""



DBP_ENTITY_TYPE_COUNTER_QUERY = f"""
    SELECT DISTINCT count(?resource) as ?count
    WHERE {{
        ?resource   rdf:type dbo:%s ;
                    rdfs:label ?label .
        FILTER(langMatches(lang(?label), "en"))

        OPTIONAL {{ ?resource foaf:name ?name }}
    }}
"""
"""
SPARQL query for getting the number of entities in the repository.
E.g.: dbo:%s => http://dbpedia.org/ontology/Place
"""



DBP_ONTOLOGY_RESOURCE_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX dbr: <{NAMESPACE.DBP_RESOURCE}>
    
    SELECT DISTINCT ?class ?label ?subclassOf
    WHERE {{
        ?class  rdf:type ?type ;
                rdfs:label ?label ;
                rdfs:subClassOf ?subclassOf .
        FILTER(?class = dbo:%s)
        FILTER(langMatches(lang(?label), "en"))
    }}
    ORDER BY ?subclassOf
"""
"""
SPARQL query for getting main key-value pairs related to a particular class
E.g.: dbo:%s => http://dbpedia.org/ontology/Museum
"""


DBP_RESOURCE_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX dbr: <{NAMESPACE.DBP_RESOURCE}>
    
    SELECT DISTINCT ?class ?label ?subclassOf
    WHERE {{
        ?class  ?p ?o ;
                rdf:type ?subclassOf ;
                rdfs:label ?label .
        FILTER(langMatches(lang(?label), "en")) .
        FILTER(?class = dbr:%s)
    }}
    ORDER BY ?subclassOf
"""
"""
SPARQL query for getting main key-value pairs related to a particular resource
E.g.: dbr:%s => http://dbpedia.org/resource/Barda_Mausoleum
"""
