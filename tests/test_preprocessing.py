import pandas as pd
from tcga_brca_clinical import preprocess, conf, io


def test_data_export(tmp_path):
    tmp_filepath = tmp_path.joinpath(conf.PREPROCESSED_FILENAME)
    data = io.read_raw_data(conf.RAW_DATA_PATH)
    prep_data = preprocess.preprocess_pipeline(data)
    io.save_data(data, tmp_filepath)
    saved_data = io.read_data(tmp_filepath)
    pd.testing.assert_frame_equal(saved_data, data)
