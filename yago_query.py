def yago_collab_artworks_query():
    query = """
    PREFIX schema: <http://schema.org/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?artwork ?artworkLabel ?creatorCount ?date ?creatorLabel ?creator ?nationality ?nationalityLabel ?genderLabel
    WHERE
    {
    { SELECT ?artwork (COUNT(DISTINCT ?creator) as ?creatorCount)  WHERE
    {
    ?artwork rdf:type schema:VisualArtwork .
    ?artwork  schema:creator ?creator .
    }
    GROUP BY ?artwork ?creatorCount
    }
    ?artwork  schema:creator ?creator .
    ?creator rdfs:label ?creatorLabel FILTER (lang(?creatorLabel) = 'en')
    OPTIONAL {?creator schema:nationality ?nationality . ?nationality rdfs:label ?nationalityLabel FILTER (lang(?nationalityLabel) = 'en') . }
    OPTIONAL { ?creator schema:gender ?gender . ?gender rdfs:label ?genderLabel FILTER (lang(?genderLabel) = 'en') .}
    OPTIONAL { ?artwork rdfs:label ?artworkLabel FILTER (lang(?artworkLabel) = 'en') }
    OPTIONAL { ?artwork schema:dateCreated ?date . }
    FILTER (?creatorCount > 1)
    }
    GROUP BY ?artwork ?creatorCount ?date ?artworkLabel ?creatorLabel ?creator ?nationalityLabel ?nationality ?genderLabel
    ORDER BY DESC(?creatorCount)
    LIMIT 20
    """
    return query
