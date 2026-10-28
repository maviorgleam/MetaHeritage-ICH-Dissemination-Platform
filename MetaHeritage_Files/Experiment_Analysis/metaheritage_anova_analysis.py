import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def welch_anova(*args):
    """Welch's ANOVA (robust to unequal variances), returns F, df1, df2, p."""
    k = len(args)
    n_i = np.array([len(a) for a in args], dtype=float)
    mean_i = np.array([np.mean(a) for a in args], dtype=float)
    var_i = np.array([np.var(a, ddof=1) for a in args], dtype=float)
    w_i = n_i / var_i
    W = np.sum(w_i)
    grand = np.sum(w_i * mean_i) / W
    numerator = np.sum(w_i * (mean_i - grand) ** 2) / (k - 1)
    denominator = 1 + (2 * (k - 2) / (k ** 2 - 1)) * np.sum((1 - w_i / W) ** 2 / (n_i - 1))
    F = numerator / denominator
    df1 = k - 1
    df2 = 1 / ((3 / (k ** 2 - 1)) * np.sum((1 - w_i / W) ** 2 / (n_i - 1)))
    p = stats.f.sf(F, df1, df2)
    return F, df1, df2, p

DATA_FILE = "MetaHeritage_Dataset_Template.csv"
df = pd.read_csv(DATA_FILE)

MEASURES = {
    "Exploration_Interest": "Exploration Interest",
    "Knowledge_Instant":    "Immediate Knowledge Retention",
    "Knowledge_24h":        "24-hour Knowledge Retention",
    "Cultural_Identity":    "Cultural Identity",
}

GROUP_NAMES = {"A": "Text & Image", "B": "Pure 3D", "C": "3D + Digital Human"}

print("=" * 70)
print("MetaHeritage Formal Analysis (One-way ANOVA + Tukey HSD)")
print("=" * 70)
print(f"Total participants: {len(df)}  |  Per group: {df.groupby('Group').size().to_dict()}\n")

print("-" * 70)
print("Descriptive Statistics (Mean % \u00b1 SD)")
print("-" * 70)
header = f"{'Measure':<28}" + "".join(f"{GROUP_NAMES[g]:>22}" for g in ["A", "B", "C"])
print(header)
for col, label in MEASURES.items():
    line = f"{label:<28}"
    for g in ["A", "B", "C"]:
        vals = df.loc[df["Group"] == g, col]
        line += f"{vals.mean():>13.1f} \u00b1 {vals.std(ddof=1):>4.1f}  "
    print(line)

print("\n" + "-" * 70)
print("Assumption Check: Levene's test for homogeneity of variances (p > 0.05 \u2192 OK)")
print("-" * 70)
for col, label in MEASURES.items():
    groups = [df.loc[df["Group"] == g, col].values for g in ["A", "B", "C"]]
    stat, p = stats.levene(*groups)
    verdict = "OK (homogeneous)" if p > 0.05 else "WARNING (heterogeneous)"
    print(f"{label:<28} Levene W={stat:6.3f}, p={p:.4f}  {verdict}")

print("\n" + "-" * 70)
print("One-way ANOVA (significance level \u03b1 = 0.05)")
print("-" * 70)
anova_results = {}
for col, label in MEASURES.items():
    groups = [df.loc[df["Group"] == g, col].values for g in ["A", "B", "C"]]
    F, p = stats.f_oneway(*groups)
    anova_results[col] = (F, p)
    sig = "significant" if p < 0.05 else "not significant"
    print(f"{label:<28} F={F:6.3f}, p={p:.4f}  {sig}")

# 稳健性检验
print("\n" + "-" * 70)
print("Robustness Checks: Welch ANOVA & Kruskal-Wallis")
print("-" * 70)
robust_results = {}
for col, label in MEASURES.items():
    groups = [df.loc[df["Group"] == g, col].values for g in ["A", "B", "C"]]
    Fw, df1w, df2w, pw = welch_anova(*groups)
    H, pk = stats.kruskal(*groups)
    robust_results[col] = (pw, pk)
    sw = "significant" if pw < 0.05 else "not significant"
    sk = "significant" if pk < 0.05 else "not significant"
    print(f"{label:<28} Welch F={Fw:6.3f}, p={pw:.4f}  {sw}")
    print(f"{'':<28} Kruskal H={H:6.3f}, p={pk:.4f}  {sk}")

print("\n" + "-" * 70)
print("Post-hoc: Tukey HSD pairwise comparisons (family-wise \u03b1 = 0.05)")
print("-" * 70)
for col, label in MEASURES.items():
    F, p_anova = anova_results[col]
    print(f"\n--- {label} ---")
    if p_anova >= 0.05:
        print("ANOVA not significant; pairwise comparisons skipped.")
        continue
    tukey = pairwise_tukeyhsd(endog=df[col], groups=df["Group"], alpha=0.05)
    for row in tukey.summary().data[1:]:  # 跳过表头行
        g1, g2, meandiff, p_adj, lower, upper, reject = row
        if reject:
            print(f"  {GROUP_NAMES[g1]} vs {GROUP_NAMES[g2]}: "
                  f"mean diff = {float(meandiff):+.1f}, p = {float(p_adj):.4f}  (significant)")

print("\n" + "-" * 70)
print("Summary: Group ranking by mean score (1 = highest)")
print("-" * 70)
for col, label in MEASURES.items():
    means = {g: df.loc[df["Group"] == g, col].mean() for g in ["A", "B", "C"]}
    ranking = sorted(means, key=lambda g: -means[g])
    rank_str = " > ".join(f"{GROUP_NAMES[g]} ({means[g]:.1f}%)" for g in ranking)
    print(f"{label:<28} {rank_str}")

print("\n" + "-" * 70)
print("Robustness Verdict: consistency between ANOVA and robust checks")
print("-" * 70)
for col, label in MEASURES.items():
    p_anova = anova_results[col][1]
    p_welch, p_kw = robust_results[col]
    all_sig = (p_anova < 0.05) and (p_welch < 0.05) and (p_kw < 0.05)
    verdict = "Robust (all significant)" if all_sig else "Inconsistent - review"
    print(f"{label:<28} ANOVA p={p_anova:.4f}, Welch p={p_welch:.4f}, "
          f"Kruskal p={p_kw:.4f}  {verdict}")

print("\n" + "=" * 70)
print("Analysis complete.")
print("=" * 70)
