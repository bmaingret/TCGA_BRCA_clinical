# TCGA_BRCA_clinical

Analysis of clinical data from the Breast Invasive Carcinoma (TCGA-BRCA) dataset 

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
    pip install -r requirements.txt
```
> `requirements.txt` was create using `poetry export -f requirements.txt -o requirements.txt --without-hashes --dev`.

The package `scikit-survival`has some specifics. Please check the [install guide](https://scikit-survival.readthedocs.io/en/stable/install.html)

## Usage

To create the preprocessed data:

``console
    python -m tcga_brca_clinical.make_dataset
```
