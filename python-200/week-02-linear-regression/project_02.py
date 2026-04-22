import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

os.makedirs("outputs", exist_ok=True)

# Fields are separated by semicolons, not commas — must pass sep=";" to pd.read_csv()

# --- Task 1: Load and Explore ---

df = pd.read_csv("student_performance_math.csv", sep=";")
print("Shape:", df.shape)
print(df.head())
print(df.dtypes)

plt.figure()
plt.hist(df["G3"], bins=21, edgecolor="black")
plt.title("Distribution of Final Math Grades")
plt.xlabel("G3 (Final Grade)")
plt.ylabel("Count")
plt.savefig("outputs/g3_distribution.png")
plt.close()
print("Saved outputs/g3_distribution.png")

# --- Task 2: Preprocess ---

print("\nShape before filtering:", df.shape)
df_clean = df[df["G3"] > 0].copy()
print("Shape after filtering: ", df_clean.shape)
# G3=0 means the student didn't sit the final exam, not that they scored zero.
# Keeping these rows would make the model associate high absences with a zero grade,
# distorting every coefficient — including absences — since absent students skipped the exam entirely.

# Convert yes/no columns to 1/0
binary_cols = ["schoolsup", "internet", "higher", "activities"]
for col in binary_cols:
    df_clean[col] = (df_clean[col] == "yes").astype(int)

# Convert sex: F=0, M=1
df_clean["sex"] = (df_clean["sex"] == "M").astype(int)

# Absences correlation before and after filtering
corr_before = df["absences"].corr(df["G3"])
corr_after  = df_clean["absences"].corr(df_clean["G3"])
print("\nabsences–G3 correlation (original): ", corr_before)
print("absences–G3 correlation (filtered): ", corr_after)
# Students with G3=0 had high absences AND a forced score of 0.
# Before filtering, that cluster drags the correlation strongly negative.
# After filtering, only students who actually sat the exam remain — the true relationship emerges.

# --- Task 3: EDA ---

numeric_features = ["age", "Medu", "Fedu", "traveltime", "studytime",
                    "failures", "absences", "freetime", "goout", "Walc"]

correlations = df_clean[numeric_features + ["G3"]].corr()["G3"].drop("G3").sort_values()
print("\nCorrelations with G3:")
print(correlations)

# Plot 1: failures vs G3
plt.figure()
plt.scatter(df_clean["failures"], df_clean["G3"], alpha=0.4)
plt.title("Past Failures vs Final Grade")
plt.xlabel("failures")
plt.ylabel("G3")
plt.savefig("outputs/failures_vs_g3.png")
plt.close()
print("Saved outputs/failures_vs_g3.png")
# Students with more past failures cluster at lower G3 scores — failures is the strongest negative predictor.

# Plot 2: studytime vs G3 (boxplot per category)
plt.figure()
df_clean.boxplot(column="G3", by="studytime")
plt.title("G3 by Study Time")
plt.suptitle("")
plt.xlabel("Study Time (1=low, 4=high)")
plt.ylabel("G3")
plt.savefig("outputs/studytime_vs_g3.png")
plt.close()
print("Saved outputs/studytime_vs_g3.png")
# More study time shows a modest positive trend — but with wide variance, suggesting other factors matter more.

# --- Task 4: Baseline Model ---

X_base = df_clean[["failures"]].values
y = df_clean["G3"].values

X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X_base, y, test_size=0.2, random_state=42)

model_base = LinearRegression()
model_base.fit(X_train_b, y_train_b)
y_pred_b = model_base.predict(X_test_b)

rmse_b = np.sqrt(mean_squared_error(y_test_b, y_pred_b))
r2_b   = model_base.score(X_test_b, y_test_b)

print("\nBaseline (failures only)")
print("Slope: ", model_base.coef_[0])
print("RMSE:  ", rmse_b)
print("R²:    ", r2_b)
# On a 0-20 scale, RMSE ~3-4 means predictions are typically off by 3-4 grade points.
# R² around 0.15-0.20 is roughly what the correlation suggested — failures alone explains only ~15-20% of the variance.

# --- Task 5: Full Model ---

feature_cols = ["failures", "Medu", "Fedu", "studytime", "higher", "schoolsup",
                "internet", "sex", "freetime", "activities", "traveltime"]

X_full = df_clean[feature_cols].values
y = df_clean["G3"].values

X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(X_full, y, test_size=0.2, random_state=42)

model_full = LinearRegression()
model_full.fit(X_train_f, y_train_f)
y_pred_f = model_full.predict(X_test_f)

rmse_f    = np.sqrt(mean_squared_error(y_test_f, y_pred_f))
r2_train  = model_full.score(X_train_f, y_train_f)
r2_test   = model_full.score(X_test_f, y_test_f)

print("\nFull Model")
print("Train R²: ", r2_train)
print("Test R²:  ", r2_test)
print("RMSE:     ", rmse_f)
print("Baseline Test R²: ", r2_b, " → Full Model Test R²: ", r2_test)

print("\nCoefficients:")
for name, coef in zip(feature_cols, model_full.coef_):
    print(f"{name:12s}: {coef:+.3f}")

# Train and test R² should be close — no sign of overfitting with this linear model.
# If any coefficient sign surprises you (e.g., sex positive = male students score higher),
# it reflects a documented social pattern in this 2005 Portuguese dataset, not an inherent difference.
# For production: keep failures, Medu, studytime, higher — highest signal.
# Drop traveltime, activities, freetime — near-zero coefficients, add noise without value.

# --- Task 6: Evaluate ---

plt.figure()
plt.scatter(y_pred_f, y_test_f, alpha=0.6)
min_val = min(y_pred_f.min(), y_test_f.min())
max_val = max(y_pred_f.max(), y_test_f.max())
plt.plot([min_val, max_val], [min_val, max_val], "r--", label="Perfect fit")
plt.title("Predicted vs Actual (Full Model)")
plt.xlabel("Predicted G3")
plt.ylabel("Actual G3")
plt.legend()
plt.savefig("outputs/predicted_vs_actual.png")
plt.close()
print("Saved outputs/predicted_vs_actual.png")
# Points above diagonal: model underpredicted. Points below: model overpredicted.
# If errors cluster at the extremes (very high or very low grades), the model struggles there most.

# Summary:
# - Filtered dataset: students who sat the final exam (~370-380 rows); test set: ~75 rows
# - RMSE ~3 on 0-20 scale means typical prediction error of 3 grade points
# - Largest positive coefficient: higher (wanting higher education) — motivated students score more
# - Largest negative coefficient: failures — past failure is the strongest drag on final grade
# - Surprising: schoolsup (school support) has a negative coefficient — students receiving
#   extra help are already struggling, so it reflects selection, not the intervention's effect

# --- Bonus: Adding G1 ---

X_g1 = df_clean[feature_cols + ["G1"]].values
y = df_clean["G3"].values

X_train_g, X_test_g, y_train_g, y_test_g = train_test_split(X_g1, y, test_size=0.2, random_state=42)

model_g1 = LinearRegression()
model_g1.fit(X_train_g, y_train_g)
print("\nWith G1 — Test R²:", model_g1.score(X_test_g, y_test_g))
# G1 being highly predictive of G3 does NOT mean G1 causes G3 — both reflect the same student.
# This model is useful for predicting who will struggle, but only after period 1 grades exist.
# To intervene early (before G1), educators would need non-grade signals:
# attendance patterns, study time, family background — exactly the features in this dataset.
