def wikidata_companies_query():
    query = """
    SELECT
      ?company ?companyLabel
      (GROUP_CONCAT(DISTINCT ?inceptionLabel;separator=", ") AS ?inceptions)
      (GROUP_CONCAT(DISTINCT ?foundedByLabel;separator=", ") AS ?founders)
      (GROUP_CONCAT(DISTINCT ?industryLabel;separator=", ") AS ?industries)
      (MAX (?numEmployees) AS ?maxEmployees)
      (MAX(?revenue) as ?maxRevenue)
    WHERE {
      ?company wdt:P31 wd:Q891723 .
      ?company wdt:P17 wd:Q30 .
      OPTIONAL { ?company wdt:P571 ?inception . }
      OPTIONAL { ?company wdt:P112 ?foundedBy . }
      OPTIONAL { ?company wdt:P452 ?industry . }

      ?company p:P1128 ?statement1 .
      ?statement1 ps:P1128 ?numEmployees .

      ?company p:P2139 ?statement .
      ?statement ps:P2139 ?revenue .

      SERVICE wikibase:label {
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
                  ?foundedBy rdfs:label ?foundedByLabel .
                  ?company rdfs:label ?companyLabel .
                  ?inception rdfs:label ?inceptionLabel .
                  ?industry rdfs:label ?industryLabel .
                  }
    }
    GROUP BY ?company ?companyLabel ?inceptions ?founders ?industries
    ORDER BY DESC(?maxRevenue)
    LIMIT 50
    """
    return query
