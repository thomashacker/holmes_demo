from pathlib import Path
import holmes_extractor as holmes
import os

# Setup
def setup_en_literature(ontology_path:Path, model_name:str, en_literature_dir:Path):
    """Initialize Holmes Manager for the english literature"""
    ontology = holmes.Ontology(ontology_path)
    holmes_manager = holmes.Manager(model=model_name, ontology=ontology, number_of_workers=1, verbose=True)
    return serialize_documents(en_literature_dir, holmes_manager)

def setup_de_literature(model_name:str, de_literature_dir:Path) -> holmes.Manager:
    """Initialize Holmes Manager for the german literature"""
    holmes_manager = holmes.Manager(model=model_name, number_of_workers=1, verbose=True)
    return serialize_documents(de_literature_dir, holmes_manager)

def serialize_documents(literature_dir: Path, holmes_manager: holmes.Manager) -> holmes.Manager:
    """Serialize a set of documents to the Holmes Manager"""
    serialized_documents = {}
    for file in os.listdir(str(literature_dir)):
        if file.endswith("hdc"):
            label = file[:-4]
            long_filename = os.sep.join((str(literature_dir), file))
            with open(long_filename, "rb") as file:
                contents = file.read()
            serialized_documents[label] = contents
    holmes_manager.register_serialized_documents(serialized_documents)

    return holmes_manager

# Processing
def process_holmes_output(holmes_results: list[dict], color_map: dict) -> list[dict]:
    """Format results of the Holmes Topic Extraction to a list of dicts"""

    output_list = []

    for result in holmes_results:
        text = result["text"]
        output_dict = {"label":result["document_label"], "rank":result["rank"], "answers":"", "text":"", "score":result["score"]}

        # If results contains answers
        if len(result["answers"]) > 0:
            output_dict["answers"] = result["text_to_match"]
            for answer in result["answers"]:
                output_dict["answers"] += f"<p class='answer'>{text[answer[0]:answer[1]]}</p>"

        # Create indices list for HTML marks
        indices_list = group_indices(result["word_infos"], result["answers"], color_map)
        offset = 0
        for index in indices_list:
            start_index = index[0]+offset
            start_snippet = text[:start_index] 
            end_snippet = text[start_index:]
            text = start_snippet + index[1] + end_snippet
            offset += index[2]

        output_dict["text"] = text
        output_list.append(output_dict)
    
    return output_list

def group_indices(word_infos: list[dict], answers: list[str], color_map: dict) -> list[tuple]:
    """Sort word_info and answers indices in text and create a list of tuples with start and end index"""
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
def card(n : int, text: str) -> str:
    """Create a HTML Card"""

    html = f"""
    <div class='card'>
        <h4 class='card_text' id='test'->{n}<h4>
        <span>{text}</span>
    </div>
    """
    return html

def format_results_HTML(label:str, rank: str, score: float, text:str, answer:str) -> str:
    """Format results to HTML for Topic Extraction"""

    formatted_score = round(score*100,0)/100

    html = f"""
    <div class='header'> <span class='rank'>{rank}</span> <span class='rank'>Score {formatted_score}</span> <span class='label'>{label}</span> </div>
    <div class='text'>{text}</div>
    <p class='answer_container'>{answer}</p>
    """
    return html

