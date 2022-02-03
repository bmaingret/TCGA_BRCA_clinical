from tcga_brca_clinical import preprocess, conf, io

def main():
    data = io.read_raw_data(conf.RAW_DATA_PATH)
    prep_data = preprocess.preprocess_pipeline(data)
    io.save_data(prep_data, conf.PREPROCESSED_DATA_PATH)

if __name__ == '__main__':
    main()
