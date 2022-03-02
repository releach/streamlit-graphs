import graphviz as graphviz
import requests
import streamlit as st
from streamlit_agraph import Config, Edge, Node, TripleStore, agraph
from yago_query import yago_collab_artworks_query
from yago_work_data import yago_work_data_query


@st.cache(suppress_st_warning=True)
def get_yago_graph_nats():
    url = "https://yago-knowledge.org/sparql/query"
    query = yago_collab_artworks_query()
    r = requests.get(url, params={"format": "json", "query": query})
    results = r.json()

    store = TripleStore()
    for result in results["results"]["bindings"]:
        subject = (
            result["artworkLabel"]["value"]
            if "artworkLabel" in result
            else "Unknown Work"
        )
        predicate = "creator"

        object = (
            result["creatorLabel"]["value"]
            if "creator" in result
            else "Unknown Creator"
        )
        subject2 = result["creatorLabel"]["value"]
        predicate2 = "nationality"
        object2 = (
            result["nationalityLabel"]["value"]
            if "nationality" in result
            else "Unknown Nationality"
        )
        store.add_triple(subject, predicate, object)
        store.add_triple(subject2, predicate2, object2)
    return store


def get_yago_work_graph():
    url = "https://yago-knowledge.org/sparql/query"
    query = yago_work_data_query()
    r = requests.get(url, params={"format": "json", "query": query})
    results = r.json()
    nodes = []
    edges = []
    for result in results["results"]["bindings"]:

        artworkURI = result["artwork"]["value"]
        artworkLabel = result["artworkLabel"]["value"]
        creatorURI = result["creator"]["value"]
        creatorLabel = result["creatorLabel"]["value"]
        artworkImage = result["sampleWorkImage"]["value"]
        creatorImage = "https://riverlegacy.org/wp-content/uploads/2021/07/blank-profile-photo.jpeg"
        nodes.append(
            Node(id=artworkURI, label=artworkLabel, size=700, svg=artworkImage)
        )
        nodes.append(
            Node(id=creatorURI, label=creatorLabel, size=500, svg=creatorImage)
        )
        edges.append(
            Edge(
                source=artworkURI,
                label="creator",
                target=creatorURI,
                type="CURVE_FULL",
            )
        )

    config = Config(
        width=900,
        height=900,
        directed=True,
        nodeHighlightBehavior=True,
        highlightColor="#800080",
        collapsible=True,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": True},
        initialZoom=2
    )
    agraph(nodes=nodes, edges=edges, config=config)

def load_graph():
    graph = graphviz.Digraph()
    graph.edge("David Hockney", "'A Bigger Splash'")
    graph.edge("David Hockney", "'A Lawn Being Sprinkled'")
    graph.edge("'A Bigger Splash'", "1967")
    graph.edge("'A Lawn Being Sprinkled'", "1967")
    graph.edge("'A Bigger Splash'", "Pop art")
    graph.edge("Pop art", "'Whaam!''")
    graph.edge("'Whaam!''", "Roy Lichtenstein")
    graph.edge("Pop art", "'Monogram'")
    graph.edge("'Monogram'", "Robert Rauschenberg")
    graph.edge("'Monogram'", "1959")
    return graph



def app():
    st.set_page_config(page_title="LOD graphs")
    st.title("LOD Graphs in Streamlit")
    st.sidebar.title("Graphs")
    query_type = st.sidebar.selectbox(
        "Select a graph: ",
        [
            "Collaborative artists and their home countries",
            "Collaborations between Titian and Giorgione",
            "Artist networks in GraphViz"
        ],
    )

    configyago = Config(
        height=900,
        width=900,
        nodeHighlightBehavior=True,
        highlightColor="#800080",
        directed=True,
        collapsible=True,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": True},
    )

    if query_type == "Collaborative artists and their home countries":
        st.subheader("Collaborative artists and their home countries")
        st.write(
            "The data was generated via a query to the [Yago](https://yago-knowledge.org/) knowledge base. The graph was created using [streamlit_agraph](https://github.com/ChrisDelClea/streamlit-agraph)."
        )
        with st.spinner("Loading data"):
            store = get_yago_graph_nats()
            agraph(list(store.getNodes()), (store.getEdges()), configyago)


    if query_type == "Collaborations between Titian and Giorgione":
        st.subheader("Collaborations between Titian and Giorgione")
        st.write(
            "The data was generated via a query to the [Yago](https://yago-knowledge.org/) knowledge base. The graph was created using [streamlit_agraph](https://github.com/ChrisDelClea/streamlit-agraph)."
        )
        with st.spinner("Loading data"):
            store = get_yago_work_graph()


    if query_type == "Artist networks in GraphViz":
        st.subheader("Artist networks in GraphViz")
        st.write(
            "This graph was created using [GraphViz](https://graphviz.org/), an open source graph visualization library."
            )
        graph = load_graph()
        st.graphviz_chart(graph)

if __name__ == "__main__":
    app()
