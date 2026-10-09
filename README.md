# B2B Account Targeting & Outbound Funnel Engine (Talent-Readiness Platform)

**Goal:** Prioritise which corporates to pitch a "validated sprint -> PPO" talent platform to, test outreach messaging, and measure the funnel.

**Stack:** Python (pandas, matplotlib), CSV/Google Sheets

## Run
```
pip install pandas matplotlib
python make_sample_data.py     # SAMPLE data. Replace data/accounts.csv with your real research
python icp_scoring.py          # scores + tiers accounts -> outputs/scored_accounts.csv
python make_outreach_log.py    # SAMPLE log. Replace data/outreach_log.csv with your real sends
python outreach_analysis.py    # funnel + A/B test -> outputs/*.csv, *.png, ab_test_result.txt
```
Skip the two `make_*` sample generators once you have real data.

## accounts.csv columns
account_id, company, industry, city, employee_band, freshers_hired_last_year, open_fresher_roles, does_campus_hiring (0/1), has_dedicated_campus_recruiter (0/1)

## outreach_log.csv columns
account_id, tier, persona, channel, variant (A_pain_led / B_proof_led), replied (0/1), meeting_booked (0/1)

## ICP scoring (100 pts)
Industry fit 20 | Company size 20 | Fresher hiring volume 25 | Open fresher roles 15 | Screening-process gap 20 (campus hiring without a dedicated recruiter). Tier 1 >= 70, Tier 2 50-69, Tier 3 < 50.

## Resume entry (fill brackets with YOUR real numbers)
**B2B Account Targeting & Outbound Funnel Engine | Python, Pandas, Google Sheets**
- Built a prospect database of **[N]** target corporate accounts and designed a 100-point ICP scoring model (industry, size, fresher-hiring volume, screening-process gap) to rank them into Tier 1/2/3.
- Designed a 4-touch LinkedIn + email outreach sequence with 2 message variants (pain-led vs proof-led) for HR heads, campus-hiring leads and founders; sent to **[N]** prospects.
- Built a funnel analysis (contacted -> replied -> meeting) with a two-proportion A/B test; found Tier 1 accounts converted at **[X%]** reply rate vs **[Y%]** for Tier 3, identifying the best segment and message to scale.
