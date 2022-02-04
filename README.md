# TCGA_BRCA_clinical

Analysis of clinical data from the Breast Invasive Carcinoma (TCGA-BRCA) dataset 

## Content

    .
    ├── data                   # raw and processed data
    ├── notebooks                    # Jupyter notebooks
    ├── tcga_brca_clinical                     # Source files 
    └── tests                    # Automated tests 


## Installation

Using `pyenv` to install Python version.

```console
    pyenv install 3.10.0
    pyenv local 3.10.0
```

If using `poetry`

```console
    poetry install
```

If using `pip`

```console
    python3 -m venv .venv
    source .venv/bin/activate
    pip install cmake
    pip install .
```
The package `scikit-survival`has some specifics and thus requires `cmake` to be installed.
Please check the [install guide](https://scikit-survival.readthedocs.io/en/stable/install.html).

## Usage

To create the preprocessed data:

``console
    python -m tcga_brca_clinical.make_dataset
```
