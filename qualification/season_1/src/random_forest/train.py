import sys
sys.path.append('../tools/')

from time import time
from sklearn.cross_validation import train_test_split
from feature_format import load_and_split_data
from model_helper import save_model
from mape import mape_score

# Import learning algo
from sklearn.ensemble import RandomForestRegressor

# Ratio to split cross validation test set
TEST_SIZE = 0.2

# Seed number for random splitting of cross validation test set
RANDOM_STATE = 42

# Model name to be saved
MODEL_NAME = 'random_forest'

# best n_est=1000, 2000, max_feat='sqrt', max_depth=Non

# Change prediction model and parameters here
def create_model():
    model = RandomForestRegressor(n_estimators=2000, max_features='sqrt', max_depth=None, n_jobs=3)

    return model

if __name__ == "__main__":
    # Load and split training data into metadata, features, target
    data_file = '../../processed_data/features_data/training_data/features_ready'
    metadata_list, features_list, target_list = load_and_split_data(data_file)

    # Split data into training set and cross validation set
    feature_train, feature_test, target_train, target_test = train_test_split(features_list, target_list, test_size = TEST_SIZE, random_state = RANDOM_STATE)

    # Start training
    start_time = time()
    model = create_model()
    model.fit(feature_train, target_train)
    print("training time", round(time() - start_time, 3), "s")

    # Start prediction using cross validation set
    start_time = time()
    pred = model.predict(feature_test)
    print("predition time", round(time() - start_time, 3), "s")

    # Show MAPE score of trained model with cross validation set
    score = mape_score(pred, target_test)
    print('MAPE score ', score)

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

    start_time = time()
    pred = model.predict(feature_test)
    print("prediction time after cleaning outliers", round(time() - start_time, 3), "s")
    score = mape_score(pred, target_test)
    print("MAPE score after cleaning outliers", score)

    # Save model for later use
    save_model(model, './model', MODEL_NAME)
