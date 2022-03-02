def yago_work_data_query():
    query = """
    PREFIX schema: <http://schema.org/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX yago: <http://yago-knowledge.org/resource/>

    SELECT ?artwork ?artworkLabel ?creatorCount ?creatorLabel ?creator (SAMPLE(?workImage) as ?sampleWorkImage)
    WHERE
    {

    { SELECT ?artwork (COUNT(DISTINCT ?creator) as ?creatorCount)  WHERE
    {
    ?artwork rdf:type schema:Painting .
    ?artwork  schema:creator ?creator .
    }
    GROUP BY ?artwork ?creatorCount
    }

    ?artwork  schema:creator ?creator .
    ?creator rdfs:label ?creatorLabel FILTER (lang(?creatorLabel) = 'en')
    ?artwork rdfs:label ?artworkLabel FILTER (lang(?artworkLabel) = 'en')
    ?artwork schema:image ?workImage .
    FILTER (?creatorCount > 1 && (?creator = yago:Titian  || ?creator = yago:Giorgione))
    }

    GROUP BY ?artwork ?creatorCount ?artworkLabel ?creatorLabel ?creator
    ORDER BY DESC(?creatorLabel)
    """
    return query
