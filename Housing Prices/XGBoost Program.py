import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

# Read the data
X = pd.read_csv('train.csv', index_col='Id')
X_test_full = pd.read_csv('test.csv', index_col='Id')

# Remove rows with missing target, separate target from predictors
X.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = X.SalePrice              
X.drop(['SalePrice'], axis=1, inplace=True)

# Break off validation set from training data
X_train_full, X_valid_full, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# "Cardinality" means the number of unique values in a column
# Select categorical columns with relatively low cardinality (convenient but arbitrary)
low_cardinality_cols = [cname for cname in X_train_full.columns if X_train_full[cname].nunique() < 10 and X_train_full[cname].dtype == "object"]

# Select numeric columns
numeric_cols = [cname for cname in X_train_full.columns if X_train_full[cname].dtype in ['int64', 'float64']]

# Keep selected columns only
my_cols = low_cardinality_cols + numeric_cols
X_train = X_train_full[my_cols].copy()
X_valid = X_valid_full[my_cols].copy()
X_test = X_test_full[my_cols].copy()

# One-hot encode the data (to shorten the code, we use pandas)
X_train = pd.get_dummies(X_train)
X_valid = pd.get_dummies(X_valid)
X_test = pd.get_dummies(X_test)
X_train, X_valid = X_train.align(X_valid, join='left', axis=1)
X_train, X_test = X_train.align(X_test, join='left', axis=1)

# Define the model
my_model_1 = XGBRegressor(random_state = 0)
# Fit the model
my_model_1.fit(X_train, y_train) 
# Get predictions
predictions_1 = my_model_1.predict(X_valid)
# Calculate MAE
mae_1 = mean_absolute_error(predictions_1, y_valid) 

#Better Model
my_model_2 = XGBRegressor(n_estimators = 400, learning_rate = 0.05) 
my_model_2.fit(X_train, y_train, early_stopping_rounds = 10, eval_set = [(X_valid, y_valid)], verbose = False) 
predictions_2 = my_model_2.predict(X_valid) 
mae_2 = mean_absolute_error(predictions_2, y_valid) 

print("Mean Absolute Error:" , mae_1)
print("Mean Absolute Error:" , mae_2)