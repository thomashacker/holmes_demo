# Welcome to Holmes

This repository builds a streamlit application for demonstrating Topic Extraction with [Holmes](https://github.com/msg-systems/holmes-extractor). 

> The project is wrapped in a spacy project.

---

## Requirements

All requirements can be install via
`pip install -r requirements.txt`

```
spacy>=3.1.4
streamlit>=1.2.0
holmes-extractor>=3.0.0
coreferee>=1.1.1
```


## ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `requirements` | Install dependencies and requirements |
| `download_en_literature` | Download data for the english literature example |
| `app` | Start the Holmes demo |

## 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `data/example_search_EN_literature_ontology.owl` | Local | Ontology for the english literature example |
