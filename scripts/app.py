import streamlit as st
from pathlib import Path
import holmes_extractor as holmes
import os
import sys
import processing as helper

# Configuration
en_literature_dir = Path("data/en_literature")
en_ontology_path = Path("data/en_literature/example_search_EN_literature_ontology.owl")
en_model_name = "en_core_web_trf"

de_literature_dir = Path("data/de_literature")
de_model_name = "de_core_news_lg"

color_map = {
    "relation":"#607EC9",
    "overlapping_relation":"#BF1E7F",
    "single":"#35C2C2"
}

predefined_queries_en = ["What did Harry see in the mirror?", "Where did Harry meet Hermione?","When did Harry meet Hermione?",
"Why was the Decree of Justifiable Confiscation created?","How can someone be killed?","Who waved their wand?","Which boys came in?",
"Which person came in?", "Somebody gives a present to Harry", "Wizards may not do magic outside school", "Hermione would never break a school rule",
"Harry Potter's dead mother","Harry Potter plays Quidditch well","An ENTITYPERSON yawns widely","a silver lion"]

predefined_queries_de = ["Wer schläft in einer Schlafstube ein?", "Wen hat ein Mann gesehen?", "Wem hilft ein Arzt?", "Woher kommt ein König nach Hause?",
"Whin reist ein Kaufmann?", "Wo wird ein Schrei gehört?", "Wieso kauft eine Tochter einen Hasen?", "Wie läuft man im Wald?", "Jemand verschreibt dem Teufel seine Seele für Silberkunst",
"Sie aß von einem goldenen Teller", "Jemand spielt mit einem goldenen Ei", "Jemand setzt sich hinter einen Busch", "Da fielen die Sterne vom Himmel", "Ein Bauer hat drei Pferde",
"Vier Ochsen und sechs Ochsen", "Ein ENTITYPER wacht die ganze Nacht"]

if __name__ == '__main__':

    # Import CSS file
    with open("scripts/style.css") as f:
        st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)

    # Logo
    empty_col, img_col, empty2_col = st.columns([0.4,0.8,0.4])
    img_col.image("data/img/lunar.png")

    # Header
    st.title("Welcome to Holmes")

    try:
        # Initialization
        data_load_state = st.subheader("Setting up Holmes...")

        # Save holmes managers in session state
        if "holmes_en" not in st.session_state:
            holmes_manager_en = helper.setup_en_literature(en_ontology_path, en_model_name, en_literature_dir)
            st.session_state["holmes_en"] = holmes_manager_en
        if "holmes_de" not in st.session_state:
            holmes_manager_de = helper.setup_de_literature(de_model_name, de_literature_dir)
            st.session_state["holmes_de"] = holmes_manager_de

        data_load_state.subheader("⚙️ Intelligent Information Extraction")

        # Intro
        st.markdown(
            """
            Holmes ([version 3.0](https://github.com/msg-systems/holmes-extractor)) is a Python 3 library running on top of spaCy that supports a number of use cases involving information extraction
            . In all use cases, the information extraction is based on analyzing the semantic relationships expressed by the component parts of each sentence.
            """
        )

        st.write("""Holmes works by understanding each query and reading through the loaded documents to look for places
            that look as though they deal with the same topic. Unlike other search engines,
            Holmes analyses the logical relationships between the words in a query and prioritises hits that share these relationships.
            This means it is important to use full, grammatical expressions and to take care with spelling.
        """
        )

        st.write("This app demonstrates one of the possible usecases of the Holmes library.")

        # Topic Extraction
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

        st.markdown("Both questions and phrases are acceptable queries; answers to questions are displayed below. The loaded search documents are the seven Harry Potter books.")

        # User Input
        language = st.selectbox("Language", ["English", "German"])
        check = st.checkbox("Use predefined queries")

        if not check:
            if language == "English":
                search = st.text_input(label="Enter your query", value="What did Harry see in the mirror?")
            else:
                search = st.text_input(label="Enter your query", value="Sie aß von einem goldenen Teller")
        else:
            if language == "English":
                search = st.selectbox("Predefined queries", predefined_queries_en)
            else:
                search = st.selectbox("Predefined queries", predefined_queries_de)

        n = st.slider("Show top n results", min_value=1, max_value=50, value=10)

        # Legend
        st.markdown(f"<p class ='answer' style='background-color:{color_map['single']}'>single words</p><p class ='answer' style='background-color:{color_map['relation']}'>relations involving two words</p><p class ='answer' style='background-color:{color_map['overlapping_relation']}'>relations involving three or more words</p>", unsafe_allow_html=True)
        st.markdown("""---""")

        # Holmes Extraction
        if language == "English":
            if "en_query" not in st.session_state:
                st.session_state["en_query"] = search
                holmes_results = st.session_state["holmes_en"].topic_match_documents_against(search,only_one_result_per_document=True)
                results = helper.process_holmes_output(holmes_results,color_map)
                st.session_state["results_en"] = results

            elif st.session_state["en_query"] != search:
                st.session_state["en_query"] = search
                holmes_results = st.session_state["holmes_en"].topic_match_documents_against(search,only_one_result_per_document=True)
                results = helper.process_holmes_output(holmes_results,color_map)
                st.session_state["results_en"] = results

            if n > len(st.session_state["results_en"]):
                n = len(st.session_state["results_en"])
            _results = st.session_state["results_en"][:n]

        else:
            if "de_query" not in st.session_state:
                st.session_state["de_query"] = search
                holmes_results = st.session_state["holmes_de"].topic_match_documents_against(search,only_one_result_per_document=True)
                results = helper.process_holmes_output(holmes_results,color_map)
                st.session_state["results_de"] = results

            elif st.session_state["de_query"] != search:
                st.session_state["de_query"] = search
                holmes_results = st.session_state["holmes_de"].topic_match_documents_against(search,only_one_result_per_document=True)
                results = helper.process_holmes_output(holmes_results,color_map)
                st.session_state["results_de"] = results

            if n > len(st.session_state["results_de"]):
                n = len(st.session_state["results_de"])
            _results = st.session_state["results_de"][:n]

        # Printing
        for result in _results:
            st.markdown(helper.format_results_HTML(result["label"],result["rank"],result["score"],result["text"],result["answers"]), unsafe_allow_html=True)
            st.markdown("""---""")

    except KeyboardInterrupt:
        try:
            st.session_state["holmes_en"].close()
            st.session_state["holmes_de"].close()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
