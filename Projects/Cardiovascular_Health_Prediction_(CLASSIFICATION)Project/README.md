# 🫀 Cardiovascular Health Prediction Classification Project

This project aims to predict the likelihood of cardiovascular disease (CVD) in patients using machine learning classification techniques. The dataset includes key medical and demographic indicators. A major focus was placed on optimizing threshold selection and evaluating model performance using various classification metrics.

---

## 🧠 Problem Statement

Cardiovascular diseases are the leading cause of death globally. Early identification of individuals at high risk can significantly improve patient outcomes. This project focuses on building a classification model that accurately predicts the presence of cardiovascular disease using patient medical records.

---

## 📁 Dataset Description

The dataset contains clinical information for each individual:

- **Features include:**
  - Age
  - Gender
  - Blood pressure (systolic/diastolic)
  - Cholesterol & Glucose levels
  - BMI (calculated from height and weight)
  - Lifestyle factors (smoking, alcohol, physical activity)
- **Target:** `1` - Has CVD, `0` - No CVD

---

## ⚙️ Preprocessing Steps

- Outlier handling and data cleaning
- Feature scaling using `StandardScaler`
- Encoding categorical variables
- Train-Test split (stratified)
- Addressed class imbalance using techniques like SMOTE

---

## ✅ Model Training & Threshold Optimization

Multiple classification models were tested, and performance was evaluated using metrics such as:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC Score



### 🧮 Threshold Optimization:

Youden’s J statistic was used to find the optimal threshold:

## 📊 Evaluation Metrics at Optimal Threshold

### Train Set Evaluation:

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0     | 0.9722    | 0.9781 | 0.9752   | 1647    |
| 1     | 0.9780    | 0.9721 | 0.9750   | 1647    |


### 🔹 Test Set Evaluation:

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0     | 0.9228    | 0.9253 | 0.9240   | 411     |
| 1     | 0.9249    | 0.9223 | 0.9236   | 411     |

- **Macro Avg F1:** 0.9238  
- **ROC-AUC Score (Test):** Maintains strong generalization performance

---

## 🔍 Key Observations

- The model performs consistently across both train and test sets, indicating low overfitting.
- Threshold tuning via Youden’s J improves sensitivity-specificity trade-off.
- High precision and recall for both classes make the model reliable for deployment in clinical risk settings.

---

## 📌 Conclusion

- A highly reliable classification model for detecting cardiovascular disease was successfully developed.
- Custom threshold selection significantly improved the performance balance.
- The model generalizes well and is suitable for integration into health-monitoring tools.

---

