<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Holmes Demo

This repository builds a streamlit application for demonstrating Topic Extraction with [Holmes](https://github.com/msg-systems/holmes-extractor). It is inspired by the original demo hosted on https://holmes-demo.xt.msg.team/

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `requirements` | Install dependencies and requirements |
| `download_en` | Download data for the english literature example |
| `download_de` | Download data for the german literature example |
| `app` | Start the Holmes demo |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `install` | `requirements` |
| `download` | `download_en` &rarr; `download_de` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`spacy project assets`](https://spacy.io/api/cli#project-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `data/example_search_EN_literature_ontology.owl` | Local | Ontology for the english literature example |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->