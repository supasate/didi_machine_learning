import sys
sys.path.append('../tools/')

from time import time
from sklearn.cross_validation import train_test_split
from feature_format import load_and_split_data
from model_helper import save_model
from mape import mape_score
from sklearn.grid_search import GridSearchCV

# Import learning algo
from sklearn.ensemble import RandomForestRegressor

# Ratio to split cross validation test set
TEST_SIZE = 0.8

# Seed number for random splitting of cross validation test set
RANDOM_STATE = 42

# Model name to be saved
MODEL_NAME = 'random_forest'

# best n_est=1000, 2000, max_feat='sqrt', max_depth=Non

## Change prediction model and parameters here
def create_model():
    model = RandomForestRegressor(n_jobs = 3)
    return model

def get_model_params():
    return {
        'n_estimators': [10, 50, 100, 250, 500, 1000, 2000],
        'max_features': ['auto', 'sqrt', 'log2', None],
        'max_depth': [None, 1000, 500, 250, 100, 50, 20, 10],
        'min_samples_split': [2, 3, 4],
        'min_samples_leaf': [1, 2, 3],
        'oob_score': [True, False]
    }
if __name__ == "__main__":
    # Load and split training data into metadata, features, target
    data_file = '../../processed_data/features_data/training_data/features_ready'
    metadata_list, features_list, target_list = load_and_split_data(data_file)

    # Split data into training set and cross validation set
    feature_train, feature_test, target_train, target_test = train_test_split(features_list, target_list, test_size = TEST_SIZE, random_state = RANDOM_STATE)

    # Select importance features
    from sklearn.feature_selection import SelectPercentile
    from sklearn.feature_selection import f_regression
    feature_selection = SelectPercentile(score_func=f_regression, percentile=80)
    feature_selection.fit(feature_train, target_train)
    feature_train = feature_selection.transform(feature_train)
    feature_test = feature_selection.transform(feature_test)

    # Start training
    start_time = time()
    pre_tuned_model = create_model()
    parameters = get_model_params()

    model = GridSearchCV(pre_tuned_model, parameters)
    model.fit(feature_train, target_train)
    print("best params", model.best_params_)
    print("training time", round(time() - start_time, 3), "s")

    # Clean outliers
    pred = model.predict(feature_train)

    cleaned = []
    for i in range(len(pred)):
        mape = abs(pred[i] - target_train[i]) / target_train[i]
        cleaned.append((feature_train[i], target_train[i], pred[i], mape))
    cleaned.sort(key = lambda x: x[3])
    cleaned = cleaned[: int(len(pred) * 0.80)]
    feature_train, target_train, pred, mape = zip(* cleaned)
    start_time = time()
    model.fit(feature_train, target_train)
    print("re-training time after cleaning outliers", round(time() - start_time, 3), "s")

    # Start prediction using cross validation set
    start_time = time()
    pred = model.predict(feature_test)
    print("predition time", round(time() - start_time, 3), "s")

    # Show MAPE score of trained model with cross validation set
    score = mape_score(pred, target_test)
    print('MAPE score ', score)

    # Save model for later use
    save_model(model, './model', MODEL_NAME)





    from result_helper import save_result

    data_file = '../../processed_data/prediction_data/to_predict_features'
    test_metadata_list, test_features_list, test_target_list = load_and_split_data(data_file)
    test_features_list = feature_selection.transform(test_features_list)

    test_predictions = model.predict(test_features_list)

    OUTPUT_FOLDER = './output'

    save_result(OUTPUT_FOLDER, MODEL_NAME, test_metadata_list, test_predictions)
