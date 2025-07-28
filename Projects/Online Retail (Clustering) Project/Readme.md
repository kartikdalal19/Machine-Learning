# 🛍️ Online Retail (Clustering) Project


This project performs customer segmentation using unsupervised machine learning techniques on a real-world retail dataset. The goal is to identify distinct customer groups based on purchasing behavior and product interest to drive data-informed business strategies.

---

## 📌 Problem Statement

In a highly competitive e-commerce environment, understanding customer behavior is crucial. This project aims to segment customers based on purchase frequency, total spend, and product preferences, using clustering techniques. Such segmentation allows businesses to:

- Personalize marketing efforts
- Improve customer retention
- Enhance inventory and pricing strategies

---

## 📊 Dataset Overview

The dataset contains 406,829 transaction records with the following key fields:

- `InvoiceNo`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `UnitPrice`
- `CustomerID`
- `Country`

---

## 🔍 Data Preprocessing

- Removed duplicates and missing `CustomerID` values
- Handled negative quantities (erroneous returns)
- Created new features:
  - `TotalPrice = Quantity × UnitPrice`
  - `OrderFrequency` (number of orders per customer)
- One-hot encoded `Country`
- Grouped `Description` using **TF-IDF** for product-level interest
- Scaled numeric features using `StandardScaler`

---

## 📈 Exploratory Data Analysis (EDA)

- **Box Plot**: Identified outliers in `TotalPrice` and negative `Quantity`
- **Bar Chart**: Top purchased products and countries with the most customers
- **Scatter Plot**: Visualized customer spend vs order frequency

---

## 🤖 Machine Learning Models Used

### 1. Agglomerative Clustering
- Linkage: Ward
- Clusters: 4
- **Silhouette Score**: `0.8286`
- Well-separated and compact clusters

### 2. KMeans Clustering
- Clusters: 4
- **Silhouette Score**: `0.8002`
- Centroid-based, fast but slightly less cohesive

✅ **Final Model Chosen**: **Agglomerative Clustering**  
- Chosen due to higher silhouette score and better interpretability in hierarchical structure.

---

## 🧠 Feature Importance (PCA Insights)

PCA revealed that:
- `TotalPrice` and `OrderFrequency` are the most influential features.
- Product-level TF-IDF words (e.g., "bag", "red", "lunch") have minor contributions.

---

## 📈 Visualizations

- **PCA 2D Plot**: Cluster separation using dimensionality reduction
- **Silhouette Scores**: Evaluation metric for cohesion and separation

---

## 💼 Business Impact

- Identified **high-frequency, high-spending** customers for loyalty programs
- Detected **low-frequency, low-value** buyers to target with offers
- Product-based clustering insights can optimize inventory and marketing

---

## ❗ Key Insights

- Some customers placed unusually large orders (outliers)
- Negative quantities highlight data quality issues (returns or entry errors)
- Clusters reflect varying behavior, helping tailor strategies per group

---

## ✅ Conclusion

This project demonstrates how clustering can uncover hidden patterns in customer behavior, helping businesses optimize marketing, improve customer satisfaction, and boost revenue.

---

## 📁 Project Structure

