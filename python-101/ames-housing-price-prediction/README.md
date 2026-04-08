# 🏡 Ames Housing Price Prediction

## Project Overview

For this project, I built a regression model to predict house sale prices using the Ames Housing Dataset. This was part of a Kaggle competition challenge where I got to apply machine learning concepts I'd been learning. What started as a simple baseline model evolved into a more sophisticated approach through iterative experimentation and kaggle submissions.

**Real-World Context:** Accurate house price prediction is crucial in real estate. When homes are overpriced, they sit on the market longer, costing sellers time and money. When underpriced, sellers lose potential revenue. I wanted to build a model that could help inform these pricing decisions using actual property features.

---

## 📁 Project Structure

```
project-2/
│
├── code/
│   ├── data_reprocessing.ipynb          # Data cleaning, EDA, and visualization
│   ├── model_tuning_cleaned_data.ipynb  # Model training and evaluation
│   ├── kaggle_submissions.ipynb         # Iterative Kaggle submissions
│   └── model_insights.ipynb             # Advanced preprocessing techniques
│
├── data/
│   ├── train.csv                        # Original training data with SalePrice
│   ├── test.csv                         # Original test data (no SalePrice)
│   ├── cleaned_train.csv                # Preprocessed training data
│   ├── cleaned_test.csv                 # Preprocessed test data
│   ├── v1_submission.csv                # First Kaggle submission (baseline)
│   ├── v2_submission.csv                # Second submission (multi-feature)
│   ├── v4_submission.csv                # Fourth submission iteration
│   └── v5_submission.csv                # Ridge regression submission
│
├── images/
│   ├── Features_heatmap.png
│   ├── Garage_areaVSsale_price.png
│   ├── House_Price_Hist.png
│   ├── House_year_Built.png
│   ├── Overal_Qual_BoxPlot.png
│   ├── Pair_Plots_Feature_relationship.png
│   └── RegressionPl_Ground_Living_SalesPrice.png
│
├── presentation/
│   └── Project_2_AN_GA.pdf              # Project presentation slides
│
└── README.md
```

---

## 🎯 Problem Statement

**Can we predict house sale prices based on property features?**

I approached this as a supervised learning regression problem. The Ames Housing Dataset contains over 70 features describing various aspects of residential homes. My goal was to identify which features matter most and build a model that could accurately predict sale prices for homes in the test set.

---

## 📊 Dataset Information

**Source:** Ames Housing Dataset (Kaggle Competition)

- **Training Set:** 2,051 houses with 81 columns (including target variable `SalePrice`)
- **Test Set:** 878 houses with 80 columns (no `SalePrice` - this is what I needed to predict)

### Key Features I Focused On

After exploring correlations, I identified these as the strongest predictors:

| Feature | Description | Correlation with SalePrice |
|---------|-------------|----------------------------|
| `Overall Qual` | Overall material and finish quality (1-10 scale) | Highest |
| `Gr Liv Area` | Above-grade living area (square feet) | Very High |
| `Garage Cars` | Number of cars that fit in garage | High |
| `Garage Area` | Garage size in square feet | High |
| `Year Built` | Original construction year | Moderate-High |

---

## 🔧 My Workflow

### 1. Data Cleaning & Preprocessing (`data_reprocessing.ipynb`)

I started by getting my hands dirty with the data. Here's what I did:

**Column Standardization:**
- Converted all column names to lowercase
- Replaced spaces and special characters with underscores
- Made everything consistent across train and test sets

**Handling Missing Values:**
- Found that many "missing" values actually meant "absence of feature" (e.g., no garage, no pool)
- Filled these with `0` for numerical columns
- Key columns I addressed: `lot_frontage`, `mas_vnr_area`, `garage_yr_blt`, `garage_area`, `garage_cars`, basement features, and more

**Saved Clean Data:**
```python
train_data.to_csv("../data/cleaned_train.csv", index=False)
test_data.to_csv("../data/cleaned_test.csv", index=False)
```

### 2. Exploratory Data Analysis (EDA)

I created several visualizations to understand the data better:

**Distribution Analysis:**
- Sale prices showed right-skewed distribution (most houses in $100k-$200k range)
- Cheapest house: $12,789 | Most expensive: $755,000
- Mean: $180,796 | Median: $160,000

**Correlation Heatmap:**
- Discovered `Overall Qual` had the strongest correlation with `SalePrice`
- `Gr Liv Area` and garage-related features also showed strong relationships
- This guided my feature selection for modeling

**Key Visualizations:**
- House price distribution histogram
- Box plot showing price vs. overall quality
- Scatter plots for individual features vs. sale price
- Correlation heatmap between top features
- Regression plots showing linear relationships

### 3. Model Training & Evaluation (`model_tuning_cleaned_data.ipynb`)

**Feature Selection:**
I narrowed down to 4 core features based on correlation analysis:
```python
features = ['overall_qual', 'gr_liv_area', 'garage_cars', 'garage_area']
```

**Train/Validation Split:**
```python
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
```

**Model Training:**
```python
model = LinearRegression()
model.fit(X_train, y_train)
```

**Performance Metrics:**
- **R² Score:** 0.7935 (79.35% of variance explained)
- **Mean Absolute Error (MAE):** $25,918
- **Root Mean Squared Error (RMSE):** $35,030

**Feature Coefficients (What I Learned):**
- `overall_qual`: +$27,392 per quality point
- `gr_liv_area`: +$48.59 per square foot
- `garage_cars`: +$7,478 per car space
- `garage_area`: +$55.48 per square foot

**Model Assessment:**
While my R² of 0.79 shows the model explains a good portion of price variance, the high RMSE suggests there's still significant prediction error. This indicates potential underfitting - the model might benefit from additional features or more complex relationships.

### 4. Iterative Kaggle Submissions (`kaggle_submissions.ipynb`)

I took an iterative approach, learning from each submission:

**Submission v1 - Baseline:**
- Started simple with just `Overall Qual` as a single feature
- Wanted to establish a baseline performance

**Submission v2 - Feature Expansion:**
- Added more features: `Overall Qual`, `Gr Liv Area`, `Garage Cars`, `Total Bsmt SF`, `Year Built`
- Linear Regression model
- Saw improvement in predictions

**Submission v5 - Regularization:**
- Tried Ridge Regression (alpha=1.0) to reduce overfitting
- Same feature set as v2
- Added L2 penalty to prevent coefficient inflation

### 5. Advanced Techniques (`model_insights.ipynb`)

In this notebook, I experimented with:
- **One-hot encoding** for categorical variables
- Feature alignment between train/test sets to ensure consistency
- Handling the 42 object-type columns in the dataset

---

## 📈 Results & Key Insights

### What Worked Well:
1. **Data cleaning was crucial** - Properly handling missing values made a big difference
2. **Feature selection from EDA** - Correlation analysis helped me focus on what matters
3. **Iterative approach** - Each submission taught me something new

### What I Learned:
1. **Overall Quality is king** - This single feature has the strongest impact on price
2. **Size matters** - Both living area and garage size are strong predictors
3. **Newer homes command premiums** - Year built shows positive correlation
4. **Simple models can work** - Linear regression with 4 features got me 79% R²

### Challenges Faced:
1. **High dimensionality** - 80+ features meant careful selection was needed
2. **Missing data interpretation** - Had to understand whether "missing" meant "zero" or truly unknown
3. **Feature engineering** - Balancing model complexity vs. interpretability
4. **Underfitting** - High RMSE suggests model could be improved with additional features or non-linear relationships

---

## 🚀 How to Run This Project

### Prerequisites:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Step-by-Step:

1. **Clone this repository**
2. **Start with data preprocessing:**
   ```bash
   jupyter notebook code/data_reprocessing.ipynb
   ```
   This will generate cleaned CSVs in the `data/` folder.

3. **Train the model:**
   ```bash
   jupyter notebook code/model_tuning_cleaned_data.ipynb
   ```
   This will train the model and output performance metrics.

4. **Generate predictions for Kaggle:**
   ```bash
   jupyter notebook code/kaggle_submissions.ipynb
   ```
   This creates submission CSV files ready for Kaggle upload.

---

## 🎓 What I'd Do Differently Next Time

1. **Feature Engineering:** Create interaction terms (e.g., `Overall_Qual * Gr_Liv_Area`)
2. **Try Other Models:** Test Random Forest, XGBoost, or ensemble methods
3. **Handle Outliers:** Remove or transform extreme values
4. **Log Transform:** Apply log transformation to skewed features like `SalePrice`
5. **Cross-Validation:** Use k-fold CV for more robust evaluation
6. **More EDA:** Deeper dive into categorical variables and their impact

---

## 📚 Tools & Technologies

- **Python 3.8**
- **pandas** - Data manipulation
- **NumPy** - Numerical operations
- **scikit-learn** - Machine learning models
- **Matplotlib & Seaborn** - Data visualization
- **Jupyter Notebook** - Interactive development

---

## 📧 Contact

If you have questions about this project or want to discuss machine learning approaches, feel free to reach out!

---

**Note:** This project was completed as part of a data science learning journey. The focus was on understanding the full ML workflow from data cleaning to model evaluation and iterative improvement.
