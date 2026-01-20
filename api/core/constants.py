# Label mapping for obesity levels
LABEL_MAPPING = {
    0: "Insufficient_Weight",
    1: "Normal_Weight",
    2: "Overweight_Level_I",
    3: "Overweight_Level_II",
    4: "Obesity_Type_I",
    5: "Obesity_Type_II",
    6: "Obesity_Type_III"
}

# Features information for API documentation
FEATURES_INFO = {
    "Gender": {"type": "string", "values": ["Male", "Female"]},
    "Age": {"type": "float", "range": [10, 120], "unit": "years"},
    "Height": {"type": "float", "range": [1.0, 2.5], "unit": "meters"},
    "Weight": {"type": "float", "range": [20, 300], "unit": "kg"},
    "family_history_with_overweight": {"type": "string", "values": ["yes", "no"]},
    "FAVC": {"type": "string", "values": ["yes", "no"], "description": "High caloric food consumption"},
    "FCVC": {"type": "float", "range": [1, 3], "description": "Vegetable consumption frequency"},
    "NCP": {"type": "float", "range": [1, 4], "description": "Number of main meals"},
    "CAEC": {"type": "string", "values": ["no", "Sometimes", "Frequently", "Always"], "description": "Food between meals"},
    "SMOKE": {"type": "string", "values": ["yes", "no"]},
    "CH2O": {"type": "float", "range": [1, 3], "unit": "liters", "description": "Daily water intake"},
    "SCC": {"type": "string", "values": ["yes", "no"], "description": "Calorie monitoring"},
    "FAF": {"type": "float", "range": [0, 3], "description": "Physical activity frequency (days/week)"},
    "TUE": {"type": "float", "range": [0, 2], "unit": "hours", "description": "Technology usage time"},
    "CALC": {"type": "string", "values": ["no", "Sometimes", "Frequently", "Always"], "description": "Alcohol consumption"},
    "MTRANS": {"type": "string", "values": ["Automobile", "Motorbike", "Bike", "Public_Transportation", "Walking"], "description": "Transportation"}
}
