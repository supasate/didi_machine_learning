import sys
sys.path.append('../tools/')

from feature_format import load_and_split_data
from model_helper import load_latest_model
from result_helper import save_result

if __name__ == "__main__":
    # Load and split data into metadata, features, target
    data_file = '../../processed_data/prediction_data/to_predict_features'
    metadata_list, features_list, target_list = load_and_split_data(data_file)

    # Load saved model
    model = load_latest_model('./model', 'linear_regression')

    predictions = model.predict(features_list)

    OUTPUT_FOLDER = './output'

    save_result(OUTPUT_FOLDER, 'linear_regression', metadata_list, predictions)
