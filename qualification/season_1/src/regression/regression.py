import sys
sys.path.append('../tools/')
from time import time
from feature_format import load_data, target_feature_split

t0 = time()
data_file = '../../processed_data/features_data/training_data/features_ready'
data = load_data(data_file)

target, features = target_feature_split(data)

from sklearn.cross_validation import train_test_split
feature_train, feature_test, target_train, target_test = train_test_split(features, target, test_size=0.5, random_state=42)

print("data preparation time", round(time() - t0, 3), "s")

from sklearn.linear_model import LinearRegression

t1 = time()
clf = LinearRegression().fit(feature_train, target_train)
print("training time", round(time() - t1, 3), "s")

t2 = time()
pred = clf.predict(feature_test)
print("predition time", round(time() - t2, 3), "s")

from mape import mape_score

score = mape_score(pred, target_test)
print('MAPE score ', score)
