import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

COLS = [
    "Bug Fix", "Feature Addition", "Refinements",
    "Other", "Total PRs", "Total Releases",
    "Average Prob. Positive", "Review Count"
]

pr_df = pd.read_csv("output_data/cleaned-pr-labels.csv")
sentiment_df = pd.read_csv("output_data/backloggd_reviews_with_sentiment.csv")

agg_sentiment_df = sentiment_df.groupby("Title").agg({
    "prob_positive": "mean",
    "Review": "count"
}).rename(columns={
    "prob_positive": "Average Prob. Positive",
    "Review": "Review Count",

})

merged = pd.merge(pr_df, agg_sentiment_df, left_on="Game Title", right_on="Title", how="inner")
data = merged[COLS]

spearman = data.corr(method="spearman")
kendall = data.corr(method="kendall")

plt.figure(figsize=(18,14))
sns.heatmap(spearman, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Spearman Correlation Heatmap")
plt.savefig("./tables/spearman_heatmap.png")

plt.figure(figsize=(18,14))
sns.heatmap(kendall, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Kendall Tau Correlation Heatmap")
plt.savefig("./tables/kendall_heatmap.png")