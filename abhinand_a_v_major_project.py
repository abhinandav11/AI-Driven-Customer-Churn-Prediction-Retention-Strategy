# -*- coding: utf-8 -*-
"""Abhinand A V Major Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gObZ9wrkGiip7nxNqb4-2QigTl91SjDF
"""

import pandas as pd
import os

# Define file path
file_path = "/content/Telco_customer_churn.xlsx"

# Check if the file exists
if not os.path.exists(file_path):
    print("❌ File NOT Found! Please re-upload the dataset.")
else:
    print("✅ File Found! Loading Data...")

    # Load dataset
    df = pd.read_excel("Telco_customer_churn.xlsx")

    # Display dataset overview
    print("\n📌 Dataset Overview:")
    print(df.info())

    # Handle missing values by dropping rows with nulls
    df = df.dropna()

    # Convert 'Total Charges' to numeric if it exists
    if "Total Charges" in df.columns:
        df["Total Charges"] = pd.to_numeric(df["Total Charges"], errors="coerce")
        df = df.dropna()

    # Standardize the Churn column name (renaming it to 'Churn' if necessary)
    churn_columns = ["Churn Label", "Churn Value", "Exited", "Churn Reason"]
    for col in churn_columns:
        if col in df.columns:
            df.rename(columns={col: "Churn"}, inplace=True)
            break  # Stop after renaming the first matching column

    # Drop unnecessary columns
    unnecessary_cols = ["CustomerID", "Count", "Country", "State", "City", "Zip Code",
                        "Lat Long", "Latitude", "Longitude", "Churn Score", "CLTV"]
    df.drop(columns=[col for col in unnecessary_cols if col in df.columns], inplace=True)

    # Save cleaned dataset
    cleaned_file_path = "/content/cleaned_churn.csv"
    df.to_csv(cleaned_file_path, index=False)

    print(f"\n✅ Data Cleaning Completed! Cleaned Data Shape: {df.shape}")
    print("\n🛠️ Remaining Columns:", df.columns.tolist())



import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load cleaned dataset
cleaned_file_path = "/content/cleaned_churn.csv"
df = pd.read_csv(cleaned_file_path)

# Ensure 'Churn' column is numeric (0/1)
if df["Churn"].dtype == "object":
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})  # Convert 'Yes' -> 1, 'No' -> 0

# ✅ Churn Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x=df["Churn"])
plt.title("Customer Churn Distribution")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.show()

# ✅ Correlation Heatmap (for all numerical features)
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.show()

# ✅ Tenure vs Churn
plt.figure(figsize=(8, 5))
sns.boxplot(x=df["Churn"], y=df["Tenure Months"])
plt.title("Tenure vs Churn")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Tenure (Months)")
plt.show()

# ✅ Monthly Charges vs Churn
plt.figure(figsize=(8, 5))
sns.boxplot(x=df["Churn"], y=df["Monthly Charges"])
plt.title("Monthly Charges vs Churn")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Monthly Charges ($)")
plt.show()

print("\n📌 EDA Completed! Insights Generated.")

# expand EDA by adding:

# Advanced Feature Analysis – Identifying multicollinearity, feature importance using models like XGBoost

# Segmentation Analysis – Clustering techniques (like K-Means) for deeper customer insights

# Anomaly Detection – Identifying unusual customer behaviors that may indicate fraud or churn

# Check for Multicollinearity (Using VIF)
# 1. Advanced Feature Analysis
# Check Multicollinearity Using a Correlation Heatmap
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load dataset
df = pd.read_csv("/content/cleaned_churn.csv")  # Replace with actual dataset

# Selecting numerical columns for VIF calculation
numeric_features = df.select_dtypes(include=[np.number]).dropna()

# Compute VIF for each feature
vif_data = pd.DataFrame()
vif_data["Feature"] = numeric_features.columns
vif_data["VIF"] = [variance_inflation_factor(numeric_features.values, i) for i in range(len(numeric_features.columns))]

print(vif_data)
# Interpreting the Output:
# VIF < 5 → Low multicollinearity (Good to keep)

# VIF between 5-10 → Moderate multicollinearity (Consider removing or transforming)

# VIF > 10 → High multicollinearity (Should be removed or combined with other variables)

# Solutions to Handle Multicollinearity
# Drop one of the highly correlated variables (e.g., drop "Total Charges" since it's derived from "Tenure Months" and "Monthly Charges").

# Use Principal Component Analysis (PCA) to transform features while reducing dimensionality.

# Solution 1: Drop Highly Correlated Features
# Dropping 'Total Charges' to reduce multicollinearity
df.drop(columns=['Total Charges'], inplace=True)

# Recalculate VIF after dropping the feature
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np

numerical_features = df.select_dtypes(include=[np.number]).drop(columns=['Churn'], errors='ignore')

vif_data = pd.DataFrame()
vif_data["Feature"] = numerical_features.columns
vif_data["VIF"] = [variance_inflation_factor(numerical_features.values, i) for i in range(numerical_features.shape[1])]

print(vif_data)

#Handling "Churn Value" Multicollinearity
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import LabelEncoder

# Sample dataset (Replace this with your actual dataframe)
# df = pd.read_csv("your_data.csv")

# Step 1: Drop non-numeric columns
df_numeric = df.select_dtypes(include=[np.number])

# Step 2: Encode categorical variables if needed (One-Hot Encoding & Label Encoding)
categorical_cols = df.select_dtypes(include=['object']).columns

for col in categorical_cols:
    if df[col].nunique() <= 2:
        # Binary columns -> Label Encoding
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
    else:
        # Non-binary categorical columns -> One-Hot Encoding
        df = pd.get_dummies(df, columns=[col], drop_first=True)

# Step 3: Recompute VIF
df_numeric = df.select_dtypes(include=[np.number])  # Ensure only numeric columns remain

vif_data = pd.DataFrame()
vif_data["Feature"] = df_numeric.columns
vif_data["VIF"] = [variance_inflation_factor(df_numeric.values, i) for i in range(df_numeric.shape[1])]

# Display VIF values
print(vif_data)
# Removes non-numeric columns
# Encodes categorical variables (if needed)
# Calculates VIF

#  Removes non-numeric columns to avoid "string to float" errors
#  Encodes categorical variables using Label Encoding (for binary) & One-Hot Encoding (for multi-category)
#  Recalculates VIF to check for multicollinearity

# "inf" (Infinite) VIF Values

# This happens when a column is highly correlated with other features, causing perfect multicollinearity.

# Columns like "Tenure Months", "Monthly Charges", and "PC1/PC2" might be highly dependent on each other.

# "NaN" in Churn

# This occurs if "Churn" has constant values or missing data.

#  Cause: Highly Correlated Variables
# "Tenure Months" and "Monthly Charges" might be strongly correlated.

# Solution: Check correlations and drop one of them.

#  Cause: Principal Component Features (PC1, PC2, etc.)
# The presence of multiple PC1 & PC2 columns suggests an issue with feature engineering.

# Solution: Ensure that PCA components are stored correctly and avoid duplicate features.

# Cause: Perfect Collinearity in Data
# If a feature is a linear combination of other features, VIF becomes infinite.

# Solution: Drop highly correlated columns based on correlation analysis.


import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Drop columns with infinite VIF values
columns_to_remove = ["PC1", "PC2", "Tenure Months", "Monthly Charges"]  # Modify based on correlation analysis
df_reduced = df.drop(columns=columns_to_remove, errors='ignore')

# Ensure numeric data
df_numeric = df_reduced.select_dtypes(include=[np.number])

# Recompute VIF
vif_data = pd.DataFrame()
vif_data["Feature"] = df_numeric.columns
vif_data["VIF"] = [variance_inflation_factor(df_numeric.values, i) for i in range(df_numeric.shape[1])]

# Display VIF values after removing collinear variables
print(vif_data)

# Churn" has NaN VIF

# This suggests that "Churn" might be a categorical variable or has constant values.

# Solution: Drop "Churn" before calculating VIF.



import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Ensure only numerical columns are used for VIF
df_numeric = df.select_dtypes(include=[np.number])

# Step 1: Check for correlation and drop highly correlated features
corr_matrix = df_numeric.corr().abs()  # Get absolute correlation values
upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

# Find features with correlation > 0.9 (high multicollinearity)
high_corr_features = [column for column in upper_triangle.columns if any(upper_triangle[column] > 0.9)]

# Drop one of the highly correlated features
df_vif = df_numeric.drop(columns=high_corr_features, errors="ignore")

# Step 2: Remove duplicate PCA columns (if they exist)
df_vif = df_vif.loc[:, ~df_vif.columns.duplicated()]

# Step 3: Compute VIF
vif_data = pd.DataFrame()
vif_data["Feature"] = df_vif.columns
vif_data["VIF"] = [variance_inflation_factor(df_vif.values, i) for i in range(df_vif.shape[1])]

# Display correlation heatmap (optional)
plt.figure(figsize=(10, 6))
sns.heatmap(df_vif.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Updated Feature Correlation Heatmap")
plt.show()

# Display VIF values
print(vif_data)

# Drop the feature with the highest VIF
df_vif = df_vif.drop(columns=["Monthly Charges"], errors="ignore")

# Recalculate VIF
vif_data = pd.DataFrame()
vif_data["Feature"] = df_vif.columns
vif_data["VIF"] = [variance_inflation_factor(df_vif.values, i) for i in range(df_vif.shape[1])]

# Display updated VIF values
print(vif_data)
# Display correlation heatmap (optional)
plt.figure(figsize=(10, 6))
sns.heatmap(df_vif.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Updated Feature Correlation Heatmap")
plt.show()

# 3. Customer Segmentation (K-Means Clustering)
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Selecting relevant features
features = df[['Total Charges', 'Tenure', 'Monthly Charges']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(scaled_features)

# Visualizing clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x=df['Tenure'], y=df['Monthly Charges'], hue=df['Cluster'], palette="viridis")
plt.title("Customer Segmentation Based on Tenure & Monthly Charges")
plt.show()

print(df.columns)  # Display all available column names

# Your dataset does not contain Total Charges and Tenure, but it does have Tenure Months and Monthly Charges.

# Solution
# Replace Total Charges with Monthly Charges and Tenure with Tenure Months in your K-Means Clustering code.


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Select the correct columns
X = df[['Monthly Charges', 'Tenure Months']]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Display cluster assignments
print(df[['Monthly Charges', 'Tenure Months', 'Cluster']].head())

# 4. Anomaly Detection (Identify Unusual Customer Behaviors)
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Selecting numerical features for anomaly detection
features = ['Monthly Charges', 'Tenure Months']  # Adjust if needed

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[features])

# Apply Isolation Forest for anomaly detection
iso_forest = IsolationForest(contamination=0.05, random_state=42)
df['Anomaly'] = iso_forest.fit_predict(scaled_features)

# Convert Anomaly labels: 1 → Normal, -1 → Anomaly
df['Anomaly'] = df['Anomaly'].map({1: 'Normal', -1: 'Anomaly'})

# Display anomaly results
print(df[['Monthly Charges', 'Tenure Months', 'Anomaly']].head())
#  Key Fixes
# Defined scaled_features using StandardScaler().

# Selected only numerical columns (Monthly Charges, Tenure Months) since categorical features should not be included directly.

# Applied Isolation Forest for anomaly detection.

# Mapped anomaly results so that 1 → Normal and -1 → Anomaly.

from sklearn.cluster import KMeans

# Selecting relevant features for clustering
cluster_features = df[["Tenure Months", "Monthly Charges", "Total Charges"]]

# Standardizing features
cluster_features = scaler.fit_transform(cluster_features)

# Finding optimal number of clusters using Elbow Method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans.fit(cluster_features)
    wcss.append(kmeans.inertia_)

# Plot Elbow Method
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker='o')
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.title("Elbow Method for Optimal Clusters")
plt.show()

# Training K-Means with 3 clusters (assume optimal)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Customer Segment"] = kmeans.fit_predict(cluster_features)

print("\n✅ Customer Segmentation Done! Assigned clusters:\n", df["Customer Segment"].value_counts())

# KAFKA

!pip install confluent_kafka

from confluent_kafka import Producer

# Set up Kafka Producer for Local Tunnel
conf = {
    'bootstrap.servers': 'mykafka.loca.lt:9092',  # Replace with your local tunnel URL
    'client.id': 'colab-producer'
}

producer = Producer(conf)

# Send a test message
producer.produce('churn-data', key='customer1', value='Test Churn Message')
producer.flush()
print("Message Sent!")

from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'mykafka.loca.lt:9092',  # Replace with your local tunnel URL
    'group.id': 'colab-consumer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['churn-data'])

while True:
    msg = consumer.poll(1.0)  # Wait for a message
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print(f"Received message: {msg.value().decode('utf-8')}")

import pandas as pd

df = pd.read_csv("/content/churn.csv")  # or your actual filename
# print(df['Churn'].value_counts())
print(df.columns)