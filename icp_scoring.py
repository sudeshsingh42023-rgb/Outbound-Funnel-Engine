"""Step 1: Score and tier target accounts against the Ideal Customer Profile (ICP).
ICP hypothesis: companies that hire freshers repeatedly and lack a mature campus-screening
process are the best buyers of a 'validated sprint' talent pipeline."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

W = {"industry":20, "size":20, "fresher_volume":25, "open_roles":15, "process_gap":20}  # = 100
INDUSTRY_FIT = {"IT Services":1.0, "Startup/SaaS":0.9, "BFSI":0.8, "EdTech":0.7,
                "E-commerce":0.7, "Consulting":0.6, "Manufacturing":0.4}
SIZE_FIT = {"1-50":0.4, "51-200":0.8, "201-1000":1.0, "1000+":0.7}  # mid-size = sweet spot

def score(r):
    s  = W["industry"] * INDUSTRY_FIT.get(r.industry, 0.3)
    s += W["size"] * SIZE_FIT.get(r.employee_band, 0.3)
    s += W["fresher_volume"] * min(r.freshers_hired_last_year / 25, 1)
    s += W["open_roles"] * min(r.open_fresher_roles / 6, 1)
    # pain signal: hires from campuses but has NO dedicated recruiter -> screening gap
    gap = 1.0 if (r.does_campus_hiring and not r.has_dedicated_campus_recruiter) else (0.4 if r.does_campus_hiring else 0.2)
    s += W["process_gap"] * gap
    return round(s, 1)

def tier(s): return "Tier 1" if s >= 70 else ("Tier 2" if s >= 50 else "Tier 3")

if __name__ == "__main__":
    df = pd.read_csv("data/accounts.csv")
    df["icp_score"] = df.apply(score, axis=1)
    df["tier"] = df.icp_score.apply(tier)
    df = df.sort_values("icp_score", ascending=False)
    df.to_csv("outputs/scored_accounts.csv", index=False)
    print(df.tier.value_counts().sort_index().to_string())
    print("\nTop 10 accounts:\n", df.head(10)[["company","industry","employee_band","icp_score","tier"]].to_string(index=False))
    print("\nAvg score by industry:\n", df.groupby("industry").icp_score.mean().round(1).sort_values(ascending=False).to_string())
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    df.tier.value_counts().sort_index().plot.bar(ax=ax[0], color=["#2a6f97","#61a5c2","#a9d6e5"]); ax[0].set_title("Accounts per tier"); ax[0].set_xlabel("")
    df.groupby("industry").icp_score.mean().sort_values().plot.barh(ax=ax[1], color="#2a6f97"); ax[1].set_title("Avg ICP score by industry")
    plt.tight_layout(); plt.savefig("outputs/icp_overview.png", dpi=150)
