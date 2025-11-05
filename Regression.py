import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

prs = pd.read_csv("output_data/cleaned-pr-labels.csv")
reviews = pd.read_csv("output_data/backloggd_reviews_with_sentiment.csv")

sentimentSummary = reviews.groupby("Title")["prob_positive"].mean().reset_index()
sentimentSummary.rename(columns={"prob_positive": "Avg_Positive_Sentiment"}, inplace=True)

merged = pd.merge(prs, sentimentSummary, left_on="Game Title", right_on="Title")

merged["Bug_Ratio"] = merged["Bug Fix"] / merged["Total PRs"]
merged["Refinement_Ratio"] = merged["Refinements"] / merged["Total PRs"]
merged["Feature_Ratio"] = merged["Feature Addition"] / merged["Total PRs"]
merged["Update_Frequency"] = np.log1p(merged["Total Releases"])

x = merged[["Bug_Ratio", "Refinement_Ratio", "Feature_Ratio", "Update_Frequency"]]
y = merged["Avg_Positive_Sentiment"]

scaler = StandardScaler()
xScaled = scaler.fit_transform(x)

model = LinearRegression()
model.fit(xScaled, y)
yPred = model.predict(xScaled)

r2 = model.score(xScaled, y)
print("R2:", r2)
print("Independent Var:")
for feature, coef in zip(x.columns, model.coef_):
    print(f"  {feature}: {coef:.4f}")

plt.figure(figsize=(8,6))
plt.scatter(y, yPred, color="blue", alpha=0.7, s=100, edgecolor="k")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", linewidth=2)

for i, title in enumerate(merged["Game Title"]):
    plt.text(y.iloc[i]+0.002, yPred[i]+0.002, title, fontsize=9)

plt.xlabel("Actual Avg Sentiment")
plt.ylabel("Predicted Avg Sentiment")
plt.title("Actual vs Predicted Game Quality (Sentiment)")
plt.grid(True)
plt.tight_layout()
plt.savefig("tables/scatter_plot.png")

features = ["Bug_Ratio", "Refinement_Ratio", "Feature_Ratio", "Update_Frequency"]
for f in features:
    plt.figure(figsize=(6,4))
    plt.scatter(merged[f], merged["Avg_Positive_Sentiment"], color="blue", alpha=0.7, s=100, edgecolor="k")
    plt.xlabel(f)
    plt.ylabel("Avg Positive Sentiment")
    plt.title(f"{f} vs Avg Positive Sentiment")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("./tables/" + f + "_Trends.png")
