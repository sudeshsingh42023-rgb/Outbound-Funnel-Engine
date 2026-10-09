"""Step 2: Funnel + A/B test on outreach (contacted -> replied -> meeting)."""
import math, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def two_prop_z(x1, n1, x2, n2):
    p1, p2, p = x1/n1, x2/n2, (x1+x2)/(n1+n2)
    se = math.sqrt(p*(1-p)*(1/n1+1/n2))
    z = (p1-p2)/se if se else 0.0
    pval = math.erfc(abs(z)/math.sqrt(2))      # two-sided
    return p1, p2, z, pval

df = pd.read_csv("data/outreach_log.csv")
def funnel(g): 
    return pd.Series({"contacted":len(g), "replied":g.replied.sum(), "meetings":g.meeting_booked.sum(),
                      "reply_rate_%":round(100*g.replied.mean(),1),
                      "meeting_rate_%":round(100*g.meeting_booked.mean(),1)})
out = {}
for col in ["tier","variant","persona","channel"]:
    out[col] = df.groupby(col).apply(funnel, include_groups=False)
    print(f"\n== By {col} ==\n", out[col].to_string())
    out[col].to_csv(f"outputs/funnel_by_{col}.csv")

a, b = df[df.variant=="A_pain_led"], df[df.variant=="B_proof_led"]
pa, pb, z, p = two_prop_z(a.replied.sum(), len(a), b.replied.sum(), len(b))
msg = (f"A/B reply rate: A(pain-led)={pa:.1%} (n={len(a)}) vs B(proof-led)={pb:.1%} (n={len(b)}) | z={z:.2f}, p={p:.3f} "
       f"-> {'significant' if p<0.05 else 'not significant at 5% (need more sends)'}")
print("\n"+msg); open("outputs/ab_test_result.txt","w").write(msg+"\n")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
out["tier"][["reply_rate_%","meeting_rate_%"]].plot.bar(ax=ax[0], color=["#2a6f97","#e07a5f"]); ax[0].set_title("Reply & meeting rate by ICP tier"); ax[0].set_xlabel("")
out["variant"][["reply_rate_%","meeting_rate_%"]].plot.bar(ax=ax[1], color=["#2a6f97","#e07a5f"]); ax[1].set_title("A/B message variants"); ax[1].set_xlabel("")
plt.tight_layout(); plt.savefig("outputs/outreach_funnel.png", dpi=150)
