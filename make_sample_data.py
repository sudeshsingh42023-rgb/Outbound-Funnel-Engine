"""Generates SAMPLE (synthetic) data so the pipeline runs end-to-end.
REPLACE data/accounts.csv and data/outreach_log.csv with your REAL research/outreach
before putting any numbers on your resume."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
N = 320
industries = ["IT Services","Startup/SaaS","BFSI","EdTech","E-commerce","Manufacturing","Consulting"]
cities = ["Bengaluru","Hyderabad","Pune","Bhubaneswar","Gurugram","Chennai","Kolkata","Remote-first"]
bands = ["1-50","51-200","201-1000","1000+"]
df = pd.DataFrame({
    "account_id": [f"ACC{i:03d}" for i in range(1, N+1)],
    "company": [f"SampleCo-{i:03d}" for i in range(1, N+1)],
    "industry": rng.choice(industries, N, p=[.25,.2,.12,.1,.12,.08,.13]),
    "city": rng.choice(cities, N),
    "employee_band": rng.choice(bands, N, p=[.25,.35,.25,.15]),
    "freshers_hired_last_year": rng.poisson(14, N),
    "open_fresher_roles": rng.poisson(3, N),
    "does_campus_hiring": rng.choice([0,1], N, p=[.4,.6]),
    "has_dedicated_campus_recruiter": rng.choice([0,1], N, p=[.65,.35]),
})
df.to_csv("data/accounts.csv", index=False)

# outreach log for scored accounts (created after scoring so tiers exist)
