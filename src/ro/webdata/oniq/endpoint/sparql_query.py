from ro.webdata.oniq.endpoint.namespace import NAMESPACE

CATEGORIES_QUERY = f"""
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX skos: <{NAMESPACE.SKOS}>
    PREFIX odr: <{NAMESPACE.OPEN_DATA_R}>
    
    SELECT DISTINCT ?class ?label
    WHERE {{
        ?class skos:prefLabel ?label .
        FILTER EXISTS {{
            SELECT DISTINCT ?class
            WHERE {{
                ?class ?p skos:Concept .
            }}
        }}
    }}
    ORDER BY ?class
    OFFSET %d
"""

CATEGORIES_COUNTER_QUERY = f"""
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    PREFIX skos: <{NAMESPACE.SKOS}>
    PREFIX odr: <{NAMESPACE.OPEN_DATA_R}>
    
    SELECT DISTINCT count(?class) as ?counter
    WHERE {{
        ?class skos:prefLabel ?label .
        FILTER EXISTS {{
            SELECT DISTINCT ?class
            WHERE {{
                ?class ?p skos:Concept .
            }}
        }}
    }}
"""

# TODO: add more exceptions to the filter (e.g.: owl:FunctionalProperty)
CLASSES_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX owl: <{NAMESPACE.OWL}>
        
    SELECT DISTINCT ?class ?subclassOf ?label ?namespace
    WHERE {{
        ?s rdf:type ?class .
        FILTER(
            ?class != rdf:Property &&
            ?class != owl:SymmetricProperty &&
            ?class != owl:TransitiveProperty
        )
        bind("" as ?subclassOf)
        bind("" as ?label)
        bind("" as ?namespace)
    }}
    ORDER BY ?class
"""

PROPERTIES_QUERY = f"""
    PREFIX rdf: <{NAMESPACE.RDF}>
    PREFIX rdfs: <{NAMESPACE.RDFS}>
    
    SELECT DISTINCT ?property ?label ?subclassOf ?domain ?range
    WHERE {{
        ?property rdf:type ?subclassOf .

        OPTIONAL {{ ?property rdfs:domain ?domain }} .
        OPTIONAL {{ ?property rdfs:range ?range }} .

        FILTER(
            ?property NOT IN (rdf:type, rdfs:subPropertyOf, rdfs:subClassOf) &&
            ?subclassOf = rdf:Property
        )
        
        bind("" as ?label)
    }}
    ORDER BY ?property
"""


# TODO: check the query
PROPERTIES_OF_RESOURCE_QUERY = f"""
    SELECT DISTINCT ?property ?subclassOf ?domain ?range
    WHERE {{
        ?class ?property ?value .

        OPTIONAL {{ ?property rdfs:domain ?domain }}
        OPTIONAL {{ ?property rdfs:range ?range }}
        OPTIONAL {{ ?property rdf:type ?subclassOf }}

        FILTER(
            ?class = <{NAMESPACE.OPEN_DATA_R}%s>
        )
        FILTER(
            ?property NOT IN (rdf:type, rdfs:subPropertyOf, rdfs:subClassOf)
        )
        FILTER(
            ?subclassOf = rdf:Property or !bound(?subclassOf)
        )
    }}
    ORDER BY ?property
"""

# TODO: check the query
RESOURCE_QUERY = f"""
    SELECT DISTINCT ?class
    WHERE {{
        ?class rdf:type ?type .
        FILTER(
            ?class = <{NAMESPACE.OPEN_DATA_R}%s>
        )
    }}
"""
