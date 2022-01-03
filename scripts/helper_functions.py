from pathlib import Path
from typing import Tuple
import holmes_extractor as holmes
import os
import streamlit.components.v1 as components

class Helper:
    """This class handles serialization, initialization, formatting and various HTML snippets"""

    # Setup
    def setup_en_literature(self,ontology_path:Path,model_name:str, en_literature_dir:Path):
        ontology = holmes.Ontology(ontology_path)
        holmes_manager = holmes.Manager(model=model_name, ontology=ontology, number_of_workers=1, verbose=True)

        serialized_documents = {}
        for file in os.listdir(str(en_literature_dir)):
            if file.endswith("hdc"):
                label = file[:-4]
                long_filename = os.sep.join((str(en_literature_dir), file))
                with open(long_filename, "rb") as file:
                    contents = file.read()
                serialized_documents[label] = contents
        holmes_manager.register_serialized_documents(serialized_documents)

        return holmes_manager

    # Processing
    def format_topic_query_output(self, results, color_map):
        """Format results of the Topic Extraction"""

        output_list = []

        for result in results:
            og_text = result["text"]
            output_dict = {"label":result["document_label"], "rank":result["rank"], "answers":result["text_to_match"], "text":""}

            if len(result["answers"]) > 0:
                for answer in result["answers"]:
                    output_dict["answers"] += f"<p class='answer'>{og_text[answer[0]:answer[1]]}</p>"
            else:
                output_dict["answers"] = ""

            indices_list = self.group_indices(result["word_infos"], result["answers"], color_map)
            offset = 0
            for index in indices_list:
                start_index = index[0]+offset
                start_snippet = og_text[:start_index] 
                end_snippet = og_text[start_index:]
                og_text = start_snippet + index[1] + end_snippet
                offset += index[2]

            output_dict["text"] = og_text
            output_list.append(output_dict)
        
        return output_list


    def group_indices(self, word_infos, answers, color_map):
        indices_list = []

        for answer in answers:
            first_tag = f" <span class='answer_mark'>"
            last_tag = f" </span> "
            indices_list.append((answer[0], first_tag, len(first_tag)))
            indices_list.append((answer[1], last_tag, len(last_tag)))           

        for word_info in word_infos:
            background_color = f"style='background-color:{color_map[word_info[2]]}'"
            first_tag = f" <p class='text_mark' data-text='{word_info[4]}' {background_color}> "
            last_tag = f" </p> "
            indices_list.append((word_info[0], first_tag, len(first_tag)))
            indices_list.append((word_info[1], last_tag, len(last_tag)))
          
        indices_list = sorted(indices_list, key=lambda tup: tup[0])
        return indices_list

    # HTML
    def card(self, n, text):
        """HTML Card"""

        html = f"""
        <div class='card'>
            <h4 class='card_text' id='test'->{n}<h4>
            <span>{text}</span>
        </div>
        """
        return html

    def topic_query_output(self, label, rank, text, answer):
        """HTML for Topic Extraction entries"""

        html = f"""
        <span class='rank'>{rank}</span> <span class='label'>{label}</span>
        <div class='text'>{text}</div>
        <p class='answer_container'>{answer}</p>
        """
        return html

    def add_javascript(self,code):
        components.html(f"""<script>{code}</script>""")
