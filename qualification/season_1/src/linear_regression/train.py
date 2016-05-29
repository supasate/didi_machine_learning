import sys
sys.path.append('../tools/')

from time import time
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from feature_format import load_and_split_data
from model_helper import save_model
from mape import mape_score

# Ratio to split cross validation test set
TEST_SIZE = 0.5

# Seed number for random splitting of cross validation test set
RANDOM_STATE = 42

# Change prediction model and parameters here
def create_model():
    model = LinearRegression()

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

    # Save model for later use
    save_model(model, './model', 'linear_regression')
