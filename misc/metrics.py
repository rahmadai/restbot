import pandas as pd
import json
data = {
  "lokasi_resto": {
    "precision": 1.0,
    "recall": 1.0,
    "f1-score": 1.0,
    "support": 1,
    "confused_with": {}
  },
  "restaurant_name": {
    "precision": 0.8333333333333334,
    "recall": 0.5555555555555556,
    "f1-score": 0.6666666666666667,
    "support": 9,
    "confused_with": {}
  },
  "working_hours": {
    "precision": 0.6666666666666666,
    "recall": 0.6666666666666666,
    "f1-score": 0.6666666666666666,
    "support": 3,
    "confused_with": {}
  },
  "micro avg": {
    "precision": 0.8,
    "recall": 0.6153846153846154,
    "f1-score": 0.6956521739130435,
    "support": 13
  },
  "macro avg": {
    "precision": 0.8333333333333334,
    "recall": 0.7407407407407408,
    "f1-score": 0.7777777777777778,
    "support": 13
  },
  "weighted avg": {
    "precision": 0.8076923076923077,
    "recall": 0.6153846153846154,
    "f1-score": 0.6923076923076923,
    "support": 13
  }
}
# Create a list of dictionaries to flatten the nested JSON structure
flat_data = []
try:
    for intent, values in data.items():
        flat_intent = {"Intent": intent}
        for key, value in values.items():
            if key != "confused_with":
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        flat_intent[f"{key}_{sub_key}"] = sub_value
                else:
                    flat_intent[key] = value
        flat_data.append(flat_intent)
except Exception as e:
    print(e)
    print(intent)
    print(values)
    print(key)
    print(value)
    print(sub_key)
    print(sub_value)
# Create a DataFrame from the flattened data
df = pd.DataFrame(flat_data)

# Save the DataFrame to a CSV file
df.to_csv("entity_metrics.csv", index=False)