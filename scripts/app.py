import streamlit as st
from pathlib import Path
import holmes_extractor as holmes
import os
import sys
from helper_functions import Helper

#This scripts builds the streamlit app for the Holmes demo

# Configuration
en_literature_dir = Path("data/en_literature")
en_ontology_path = Path("data/en_literature/example_search_EN_literature_ontology.owl")
model_name = "en_core_web_trf"
color_map = {
    "relation":"#607EC9",
    "overlapping_relation":"#BF1E7F",
    "single":"#35C2C2"
}
predefined_queries_en = ["What did Harry see in the mirror?", "Where did Harry meet Hermione?","When did Harry meet Hermione?","How can someone be killed?"]

if __name__ == '__main__':
    # CSS
    with open("scripts/style.css") as f:
        st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)

    # Helper & JS
    helper = Helper()

    with open("scripts/script.js") as f:
        helper.add_javascript(f.read())

    # Logo
    empty_col, img_col, empty2_col = st.columns([0.4,0.8,0.4])
    img_col.image("data/img/lunar.png")

    # Header
    st.title("Welcome to Holmes")

    try:

        # Initialization
        data_load_state = st.subheader("Setting up Holmes...")
        # Save holmes manager in session state
        if "holmes" not in st.session_state:
            holmes_manager = helper.setup_en_literature(en_ontology_path, model_name, en_literature_dir)
            st.session_state["holmes"] = holmes_manager
        data_load_state.subheader("⚙️ Intelligent Information Extraction")

        # Intro
        st.markdown(
            """
            Holmes ([version 3.0](https://github.com/msg-systems/holmes-extractor)) is a Python 3 library running on top of spaCy that supports a number of use cases involving information extraction
            . In all use cases, the information extraction is based on analysing the semantic relationships expressed by the component parts of each sentence.
            """
        )

        st.write("""Holmes works by understanding each query and reading through the loaded documents to look for places
            that look as though they deal with the same topic. Unlike other search engines,
            Holmes analyses the logical relationships between the words in a query and prioritises hits that share these relationships.
            This means it is important to use full, grammatical expressions and to take care with spelling.
        """
        )

        st.write("This app demonstrates usecases of the Holmes library.")

        # Usecases
        ## Topic
        topic_card_col, topic_text_col = st.columns([0.3,0.8])
        topic_card_col.markdown(helper.card("🔮 Topic Matching",""), unsafe_allow_html=True)
        topic_text_col.markdown("""
        > The topic matching use case matches a query document,
        or alternatively a query phrase entered ad-hoc by the user,
        against a set of documents pre-loaded into memory.
        The aim is to find the passages in the documents whose topic most closely corresponds to the topic of the query document;
        the output is a ordered list of passages scored according to topic similarity.
        Additionally, if a query phrase contains an initial question word, the output will contain potential answers to the question.
        """)

        st.markdown("Both questions and phrases are acceptable queries; answers to questions are displayed in a separate column. The loaded search documents are the seven Harry Potter books.")

        # User Input
        check = st.checkbox("Use predefined queries")

        if not check:
            search = st.text_input(label="Enter your query", value="What did Harry see in the mirror?")
        else:
            search = st.selectbox("Predefined queries", predefined_queries_en)

        n = st.slider("Show top n results", min_value=1, max_value=50, value=10)

        # Legend
        st.markdown(f"<p class ='answer' style='background-color:{color_map['single']}'>single words</p><p class ='answer' style='background-color:{color_map['relation']}'>relations involving two words</p><p class ='answer' style='background-color:{color_map['overlapping_relation']}'>relations involving three or more words</p>", unsafe_allow_html=True)
        st.markdown("""---""")

        # Processing
        if "query" not in st.session_state:
            st.session_state["query"] = search
            holmes_results = st.session_state["holmes"].topic_match_documents_against(search,only_one_result_per_document=True)
            results = helper.format_topic_query_output(holmes_results,color_map)
            st.session_state["results"] = results

        elif st.session_state["query"] != search:
            st.session_state["query"] = search
            holmes_results = st.session_state["holmes"].topic_match_documents_against(search,only_one_result_per_document=True)
            results = helper.format_topic_query_output(holmes_results,color_map)
            st.session_state["results"] = results

        if n > len(st.session_state["results"]):
            n = len(st.session_state["results"])

        _results = st.session_state["results"][:n]

        # Printing
        for result in _results:
            st.markdown(helper.topic_query_output(result["label"],result["rank"],result["text"],result["answers"]), unsafe_allow_html=True)
            st.markdown("""---""")

    except KeyboardInterrupt:
        try:
            holmes_manager.close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
