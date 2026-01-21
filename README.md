# Obesity Level Prediction API

A Machine Learning-based system (XGBoost) for predicting obesity levels based on eating habits and physical condition.

## Project Description

This project builds a **REST API** to predict a person's obesity level based on 16 features related to:
- Personal information (gender, age, height, weight)
- Eating habits (vegetable consumption frequency, number of main meals, snacking, alcohol consumption)
- Physical activity (exercise frequency, technology device usage time)
- Lifestyle (smoking, transportation mode, calorie monitoring)

### Predicted Obesity Levels

| Code | Level | Description |
|------|-------|-------------|
| 0 | Insufficient_Weight | Underweight |
| 1 | Normal_Weight | Normal weight |
| 2 | Overweight_Level_I | Overweight Level I |
| 3 | Overweight_Level_II | Overweight Level II |
| 4 | Obesity_Type_I | Obesity Type I |
| 5 | Obesity_Type_II | Obesity Type II |
| 6 | Obesity_Type_III | Obesity Type III |

## Project Structure

```
predict_overweight/
├── api/                          # REST API (FastAPI)
│   ├── app.py                    # Entry point của API
│   ├── Dockerfile                # Docker configuration
│   ├── docker-compose.yml        # Docker Compose configuration
│   ├── requirement.txt           # Python dependencies
│   ├── core/                     # Core configurations
│   │   ├── config.py             # Application settings
│   │   ├── constants.py          # Constants & label mapping
│   │   └── logging.py            # Logging configuration
│   ├── routers/                  # API endpoints
│   │   ├── health.py             # Health check endpoint
│   │   ├── info.py               # API info endpoint
│   │   └── prediction.py         # Prediction endpoint
│   ├── schemas/                  # Pydantic models
│   │   ├── request.py            # Request schemas
│   │   ├── response.py           # Response schemas
│   │   └── enums/                # Enum definitions
│   └── services/                 # Business logic
│       └── model_service.py      # ML model service
├── dataset/                      # Datasets
│   ├── train.csv                 # Training data
│   ├── test.csv                  # Test data
│   └── sample_submission.csv     # Sample submission
└── model/                        # ML Model development
    └── predict_overweight.ipynb  # Jupyter notebook for training
```

## Technologies Used

- **Backend Framework:** FastAPI
- **Machine Learning:** XGBoost
- **Data Processing:** Pandas, NumPy, Scikit-learn
- **Containerization:** Docker, Docker Compose
- **Validation:** Pydantic

## Input Features

| Feature | Type | Description |
|---------|------|-------------|
| Gender | string | Gender (Male/Female) |
| Age | float | Age (10-120 years) |
| Height | float | Height (1.0-2.5 meters) |
| Weight | float | Weight (20-300 kg) |
| family_history_with_overweight | string | Family history of overweight (yes/no) |
| FAVC | string | Frequent consumption of high caloric food (yes/no) |
| FCVC | float | Frequency of vegetable consumption (1-3) |
| NCP | float | Number of main meals per day (1-4) |
| CAEC | string | Consumption of food between meals (no/Sometimes/Frequently/Always) |
| SMOKE | string | Smoking (yes/no) |
| CH2O | float | Daily water consumption (1-3 liters) |
| SCC | string | Calorie consumption monitoring (yes/no) |
| FAF | float | Physical activity frequency (0-3 days/week) |
| TUE | float | Time using technology devices (0-2 hours) |
| CALC | string | Alcohol consumption (no/Sometimes/Frequently/Always) |
| MTRANS | string | Transportation used (Automobile/Motorbike/Bike/Public_Transportation/Walking) |

## Installation and Running

### Requirements
- Python 3.11+
- Docker & Docker Compose (optional)

### Option 1: Run directly with Python

```bash
# Clone repository
cd predict_overweight/api

# Install dependencies
pip install -r requirement.txt

# Run API
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Run with Docker

```bash
cd predict_overweight/api

# Build and run container
docker-compose up -d --build

# View logs
docker-compose logs -f
```

## API Endpoints

### Health Check
```
GET /health
```
Check API and model status.

### Prediction
```
POST /predict
```
Predict obesity level based on input information.

**Request Body:**
```json
{
  "Gender": "Male",
  "Age": 25,
  "Height": 1.75,
  "Weight": 70,
  "family_history_with_overweight": "yes",
  "FAVC": "no",
  "FCVC": 2,
  "NCP": 3,
  "CAEC": "Sometimes",
  "SMOKE": "no",
  "CH2O": 2,
  "SCC": "no",
  "FAF": 2,
  "TUE": 1,
  "CALC": "Sometimes",
  "MTRANS": "Public_Transportation"
}
```

**Response:**
```json
{
  "prediction": "Normal_Weight",
  "prediction_code": 1,
  "probabilities": {
    "Insufficient_Weight": 0.05,
    "Normal_Weight": 0.80,
    "Overweight_Level_I": 0.03,
    "Overweight_Level_II": 0.05,
    "Obesity_Type_I": 0.02,
    "Obesity_Type_II": 0.03,
    "Obesity_Type_III": 0.02
  },
  "confidence": 0.80,
  "bmi": 22.86,
  "bmi_category": "Normal"
}
```

## 📖 API Documentation

After running the API, access:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Model Training

The notebook `model/predict_overweight.ipynb` contains the complete workflow:

1. **Data Loading & Exploration** - Load and explore dataset
2. **Data Visualization** - Visualize feature distributions
3. **Data Preprocessing** - Process data (encoding, scaling)
4. **Model Training** - Train XGBoost model
5. **Model Evaluation** - Evaluate model performance
6. **Model Export** - Export model for API usage

## Authentication

The API supports API Key authentication. Set the environment variable:

```bash
export API_KEY=your_secret_api_key
```

Then send requests with the header:
```
X-API-Key: your_secret_api_key
```

## Dataset

Data is stored in the `dataset/` folder:
- `train.csv` - Training data
- `test.csv` - Test data
- `sample_submission.csv` - Sample submission format


## Contributing

All contributions are welcome! Please create a Pull Request or Issue.
