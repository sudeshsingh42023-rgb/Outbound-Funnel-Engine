"""SAMPLE outreach log (synthetic). Replace data/outreach_log.csv with your real sends."""
import numpy as np, pandas as pd
rng = np.random.default_rng(7)
acc = pd.read_csv("outputs/scored_accounts.csv")
pick = pd.concat([acc[acc.tier=="Tier 1"].head(60), acc[acc.tier=="Tier 2"].head(60), acc[acc.tier=="Tier 3"].head(30)])
rows = []
base = {"Tier 1":0.20, "Tier 2":0.12, "Tier 3":0.06}
for _, a in pick.iterrows():
    variant = rng.choice(["A_pain_led","B_proof_led"])
    persona = rng.choice(["HR Head","Campus Hiring Lead","Founder/CXO"], p=[.4,.4,.2])
    channel = rng.choice(["LinkedIn","Email"], p=[.6,.4])
    p_reply = base[a.tier] * (1.35 if variant=="B_proof_led" else 1.0) * (1.15 if channel=="LinkedIn" else 1.0)
    replied = rng.random() < min(p_reply, .9)
    meeting = replied and rng.random() < 0.45
    rows.append(dict(account_id=a.account_id, tier=a.tier, persona=persona, channel=channel,
                     variant=variant, replied=int(replied), meeting_booked=int(meeting)))
pd.DataFrame(rows).to_csv("data/outreach_log.csv", index=False)
