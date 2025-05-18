import pandas as pd
import numpy as np
from faker import Faker
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

# Config
NUM_CUSTOMERS = 1000
fake = Faker()
np.random.seed(42)

# Generate synthetic customer churn data
def generate_customer_data(n):
    data = []
    for _ in range(n):
        gender = np.random.choice(['Male', 'Female'])
        age = np.random.randint(18, 70)
        tenure = np.random.randint(1, 72)
        monthly_charge = round(np.random.uniform(20, 150), 2)
        total_charge = round(monthly_charge * tenure, 2)
        support_calls = np.random.poisson(2)
        churn = np.random.choice([0, 1], p=[0.8, 0.2])

        data.append({
            'customer_id': fake.uuid4(),
            'gender': gender,
            'age': age,
            'tenure': tenure,
            'monthly_charge': monthly_charge,
            'total_charge': total_charge,
            'support_calls': support_calls,
            'churn': churn
        })
    return pd.DataFrame(data)

# Train ML model
def train_model(df):
    X = df[['age', 'tenure', 'monthly_charge', 'total_charge', 'support_calls']]
    y = df['churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("✅ Model Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    df['churn_prediction'] = clf.predict(X)
    return df

# Run pipeline
if __name__ == "__main__":
    df = generate_customer_data(NUM_CUSTOMERS)
    result_df = train_model(df)

    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    result_df.to_csv(f"{output_dir}/churn_predictions.csv", index=False)
    print(f"✅ Churn predictions saved to {output_dir}/churn_predictions.csv")
