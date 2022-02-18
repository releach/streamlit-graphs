import requests
import streamlit as st
from streamlit_agraph import Config, TripleStore, agraph
from wikidata_query import wikidata_companies_query
from yago_query import yago_collab_artworks_query


@st.cache
def get_yago_graph():
    url = "https://yago-knowledge.org/sparql/query"
    query = yago_collab_artworks_query()
    r = requests.get(url, params={"format": "json", "query": query})
    results = r.json()
    store = TripleStore()
    for result in results["results"]["bindings"]:
        subject = result["artwork"]["value"]
        predicate = "creator"
        object = (
            result["creator"]["value"]
            if "creator" in result
            else "Unknown Creator"
        )
        subject2 = result["creator"]["value"]
        predicate2 = "nationality"
        object2 = (
            result["nationality"]["value"]
            if "nationality" in result
            else "Unknown Nationality"
        )
        store.add_triple(subject, predicate, object)
        store.add_triple(subject2, predicate2, object2)
    return store


@st.cache
def get_wikidata_graph():
    url = "https://query.wikidata.org/sparql"
    query = wikidata_companies_query()
    r = requests.get(url, params={"format": "json", "query": query})
    results = r.json()
    store = TripleStore()
    for result in results["results"]["bindings"]:
        subject1 = result["company"]["value"]
        predicate1 = "industry"
        object1 = (
            (result["industries"]["value"].split(", ")[0])
            if "industries" in result
            else "Unknown"
        )
        store.add_triple(subject1, predicate1, object1)
    return store


def app():
    st.title("LOD Graphs with SPARQL, Python, and Streamlit")
    st.sidebar.title("Select a graph")
    query_type = st.sidebar.selectbox(
        "Query Type: ", ["Artist Collaborations", "Companies and industries"]
    )
    configwikidata = Config(
        height=900,
        width=900,
        nodeHighlightBehavior=True,
        highlightColor="#AF90A9",
        directed=True,
        collapsible=True,
    )
    configyago = Config(
        height=900,
        width=900,
        nodeHighlightBehavior=True,
        highlightColor="#85FF9E",
        directed=True,
        collapsible=True,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": True},
    )

    if query_type == "Artist Collaborations":
        st.subheader("Artist Collaborations")
        with st.spinner("Loading data"):
            store = get_yago_graph()
            st.write("Nodes loaded: " + str(len(store.getNodes())))
        st.success("Done")
        agraph(list(store.getNodes()), (store.getEdges()), configyago)

    if query_type == "Companies":
        st.subheader("Companies")
        with st.spinner("Loading data"):
            store = get_wikidata_graph()
            st.write("Nodes loaded: " + str(len(store.getNodes())))
        st.success("Done")
        agraph(list(store.getNodes()), (store.getEdges()), configwikidata)


if __name__ == "__main__":
    app()
