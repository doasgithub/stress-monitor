import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load data
data = pd.read_csv("data.csv")

X = data[["gsr", "hr", "temp"]]
y = data["stress"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained and saved as model.pkl")