import numpy as np
import pandas as pd
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

print("Loading and preprocessing data...")

# Load data
df1 = pd.read_csv("Bengaluru_House_Data.csv")

# Data cleaning and preprocessing
df2 = df1.drop(['area_type','availability','society'], axis='columns')
df3 = df2.dropna()
df3['bhk'] = df3['size'].apply(lambda x: int(x.split()[0]))

# Convert sqft to numeric
def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return ((float(tokens[0])+float(tokens[1]))/2)
    try:
        return float(x)
    except:
        return None

df4 = df3.copy()
df4['total_sqft'] = df4['total_sqft'].apply(convert_sqft_to_num)

# Create price per sqft
df5 = df4.copy()
df5['price_per_sqft'] = df5['price']*100000/df5['total_sqft']

# Reduce locations
df5.location = df5.location.apply(lambda x: x.strip())
location_stats = df5.groupby('location')['location'].agg('count').sort_values(ascending=False)
location_stats_less_than_10 = location_stats[location_stats<=10]
df5.location = df5.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

# Remove outliers
df6 = df5[~((df5.total_sqft/df5.bhk)<300)]

def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key,subdf in df.groupby('location'):
        m = np.mean(subdf.price_per_sqft)
        st = np.std(subdf.price_per_sqft)
        reduced_df = subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<=(m+st))]
        df_out = pd.concat([df_out,reduced_df], ignore_index=True)
    return df_out

df7 = remove_pps_outliers(df6)

def remove_bhk_outliers(df):
    exclude_indices = np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats = {}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk] = {
                'mean': np.mean(bhk_df.price_per_sqft),
                'std': np.std(bhk_df.price_per_sqft),
                'count': bhk_df.shape[0]
            }
        for bhk, bhk_df in location_df.groupby('bhk'):
            stats = bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices = np.append(exclude_indices, bhk_df[bhk_df.price_per_sqft<(stats['mean'])].index.values)
    return df.drop(exclude_indices, axis='index')

df8 = remove_bhk_outliers(df7)
df9 = df8[df8.bath < df8.bhk+2]

# Drop unnecessary columns
df10 = df9.drop(['size','price_per_sqft'], axis='columns')

# Create dummy variables
dummies = pd.get_dummies(df10.location)
df11 = pd.concat([df10, dummies.drop('other', axis='columns')], axis='columns')
df12 = df11.drop('location', axis='columns')

# Prepare X and y
X = df12.drop('price', axis='columns')
y = df12.price

print(f"Training model with {X.shape[0]} samples and {X.shape[1]} features...")

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
lr_clf = LinearRegression()
lr_clf.fit(X_train, y_train)
score = lr_clf.score(X_test, y_test)

print(f"Model R² score: {score:.4f}")

# Save model
print("Saving model to artifacts folder...")
with open('./artifacts/bangalore_home_prices_model.pickle', 'wb') as f:
    pickle.dump(lr_clf, f)

# Save columns
columns = {
    'data_columns': [col.lower() for col in X.columns]
}
with open('./artifacts/columns.json', 'w') as f:
    f.write(json.dumps(columns))

print("Model and columns saved successfully!")
print(f"Total locations: {len([col for col in X.columns if col not in ['total_sqft', 'bath', 'balcony', 'bhk']])}")
