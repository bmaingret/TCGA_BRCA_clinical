import pathlib


DATA_DIR = pathlib.Path("./data")

RAW_FILENAME = "brca_tcga_clinical.tsv"
PREPROCESSED_FILENAME = "brca_tcga_clinical.preprocess.pkl"

RAW_DATA_PATH = DATA_DIR.joinpath(RAW_FILENAME)
PREPROCESSED_DATA_PATH = DATA_DIR.joinpath(PREPROCESSED_FILENAME)

RANDOM_STATE = 0
