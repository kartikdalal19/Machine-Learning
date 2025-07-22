# 🚕 NYC Taxi Trip Duration Prediction

This project predicts **taxi trip durations** in New York City using machine learning models. It uses real-world trip data with timestamps, coordinates, and passenger info to estimate how long each ride will take. This can help in fleet optimization, dynamic pricing, and better customer service.

---

## 🎯 Objective

- Predict the duration of a taxi trip (in seconds) using regression models.
- Engineer features based on time and location.
- Compare multiple models and evaluate their performance.

---

## 📦 Technologies Used

- Python 3.x
- Pandas, NumPy
- Scikit-learn
- XGBoost
- Gradient Boosting Regressor
- Matplotlib, Seaborn
- Jupyter Notebook

---

## 🗂 Dataset

Dataset: **NYC Taxi Trip Duration** from Kaggle  
Includes:

- `id`, `pickup_datetime`, `dropoff_datetime`
- `pickup_longitude`, `pickup_latitude`
- `dropoff_longitude`, `dropoff_latitude`
- `passenger_count`, `store_and_fwd_flag`
- `trip_duration` (target variable)

---

## 🔧 Feature Engineering

- Extracted time-based features: `hour`, `weekday`, `month`, etc.
- Calculated geospatial distances: **Haversine**, **Manhattan**, and **bearing**
- Removed outliers and duplicates
-
---

## 🤖 Machine Learning Models Used

| Model                    | Description                              |
|-------------------------|------------------------------------------|
| 🔵 **Linear Regression**         | Baseline regression model             |
| 🌲 **Random Forest Regressor**   | Bagging ensemble of decision trees    |
| 🔶 **XGBoost Regressor**         | Boosted trees, highly efficient       |
| 🟢 **Gradient Boosting Regressor** | Gradient-boosted regression trees     |
| 🔵 **Polynomial Regression**     | Linear model with non-linear features |

---

## 📊 Model Evaluation

### ✅ Final Model: **XGBoost Regressor**

#### 🏋️ Training Metrics:

| Metric       | Value          |
|--------------|----------------|
| R²           | 0.9659         |
| Adjusted R²  | 0.9659         |
| MAE          | 64.59 sec      |
| MSE          | 9533.24        |
| RMSE         | 97.64 sec      |
| MAPE         | 18.98%         |

#### 🧪 Test Metrics:

| Metric       | Value          |
|--------------|----------------|
| R²           | 0.9647         |
| Adjusted R²  | 0.9647         |
| MAE          | 65.60 sec      |
| MSE          | 9926.40        |
| RMSE         | 99.63 sec      |
| MAPE         | 19.11%         |

> ✅ The XGBoost model achieved **high accuracy** with **low error rates**, generalizing well on unseen data.

---

## 📈 Visualizations

- 📊 **Feature Importance** (from XGBoost)
- 🧭 **Trip Duration Distribution**
- 🔥 **Correlation Heatmap**
- 📍 **Scatter Plots** of Distance vs Duration
