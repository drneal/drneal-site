#!/usr/bin/env python3
"""Five-year financial model for the Kenya Institute for Clinical AI.

Every figure in the business case is computed here, not typed into a table by
hand. Change an assumption and re-run; the document tables are regenerated from
this output.

Currency: USD. Planning rate KES 130 = USD 1 (Aug 2026).
"""

FX = 130                      # KES per USD, planning rate
ON_COSTS = 0.26               # employer statutory + pension + medical, on top of gross
INFLATION = 0.05              # annual uplift on pay and non-pay from Y2

# ── establishment: (unit, post, count, gross USD each) ───────────────────────
ESTABLISHMENT = [
    ("Executive",              "Director / Chief Executive",            1,  96_000),

    ("Quality & Evaluation",   "Head of Quality and Evaluation",        1,  60_000),
    ("Quality & Evaluation",   "Evaluation officers",                   2,  30_000),
    ("Quality & Evaluation",   "Data analyst",                          1,  28_000),
    ("Quality & Evaluation",   "Observation and audit officers",        2,  26_000),

    ("Ethics & Data Gov.",     "Ethics and governance lead",            1,  48_000),
    ("Ethics & Data Gov.",     "Data protection officer",               1,  38_000),
    ("Ethics & Data Gov.",     "Research ethics coordinator",           1,  24_000),

    ("Curriculum & Pedagogy",  "Director of Curriculum and Pedagogy",   1,  72_000),
    ("Curriculum & Pedagogy",  "Instructional designers",               4,  32_000),
    ("Curriculum & Pedagogy",  "Clinical content leads",                6,  54_000),
    ("Curriculum & Pedagogy",  "Assessment psychometrician",            1,  60_000),
    ("Curriculum & Pedagogy",  "Medical editors and translators",       3,  22_000),

    ("Faculty & Delivery",     "Track leads",                           5,  50_000),
    ("Faculty & Delivery",     "Certified instructors",                10,  34_000),
    ("Faculty & Delivery",     "Simulation faculty",                    2,  38_000),
    ("Faculty & Delivery",     "Programme manager",                     1,  34_000),

    ("Engineering & Platform", "Head of engineering",                   1,  68_000),
    ("Engineering & Platform", "Full-stack developers",                 5,  36_000),
    ("Engineering & Platform", "ML and evaluation engineers",           3,  44_000),
    ("Engineering & Platform", "Data engineers",                        2,  36_000),
    ("Engineering & Platform", "DevSecOps engineer",                    1,  42_000),
    ("Engineering & Platform", "QA engineer",                           1,  28_000),

    ("Simulation & Labs",      "Simulation centre director",            1,  52_000),
    ("Simulation & Labs",      "Simulation technicians",                3,  20_000),
    ("Simulation & Labs",      "Standardised-patient programme lead",   1,  24_000),
    ("Simulation & Labs",      "Clinical skills tutors",                2,  30_000),

    ("Operations & Registry",  "Registrar and records",                 2,  20_000),
    ("Operations & Registry",  "Finance and procurement",               2,  26_000),
    ("Operations & Registry",  "Partnerships",                          1,  34_000),
    ("Operations & Registry",  "Communications",                        1,  26_000),
    ("Operations & Registry",  "Monitoring and evaluation officer",     1,  28_000),
    ("Operations & Registry",  "Administration",                        1,  14_000),
]

# average FTE in post during each year (ramp from the blueprint's four phases)
FTE_BY_YEAR = {1: 16, 2: 34, 3: 60, 4: 71, 5: 71}

# ── capital, one-off ─────────────────────────────────────────────────────────
CAPEX = [
    ("Simulation centre fit-out (2 consult rooms, ward bay, theatre, debrief)", 480_000, 1),
    ("Sandbox, platform build and de-identified case corpus",                   350_000, 1),
    ("Assessment hall, 30 invigilated stations",                                120_000, 2),
    ("Mobile delivery unit (vehicle, generator, satellite uplink, kit)",        140_000, 2),
    ("Laptop, AV and recording fleet",                                            90_000, 1),
    ("Headquarters office fit-out",                                              110_000, 1),
]

# ── recurrent non-pay at steady state, USD/yr ────────────────────────────────
NONPAY_STEADY = {
    "Cloud, compute and model API access":        120_000,
    "Standardised patients (sessional)":           60_000,
    "Clinical champions (sessional, 0.2 FTE)":     72_000,
    "Travel and mobile-unit running costs":        80_000,
    "External examiner and triennial peer review": 30_000,
    "Accreditation, legal, audit and insurance":   45_000,
    "Utilities, maintenance and premises":         90_000,
    "Fellowship stipends (8 fellows)":            192_000,
}
# proportion of steady-state non-pay incurred each year
NONPAY_RAMP = {1: 0.30, 2: 0.55, 3: 0.85, 4: 1.00, 5: 1.00}
# fellowship only runs from Y4 (first cohort, month 22 onward)
FELLOWSHIP_FROM = 4

# ── throughput and fees ──────────────────────────────────────────────────────
FEES = {"L1": 45, "L2": 220, "L3": 480, "L4": 650, "L5": 6_000}
THROUGHPUT = {
    1: {"L1": 120,   "L2": 0,     "L3": 0,   "L4": 0,  "L5": 0},   # pilot, unpriced
    2: {"L1": 1_200, "L2": 150,   "L3": 0,   "L4": 40, "L5": 0},
    3: {"L1": 3_500, "L2": 600,   "L3": 120, "L4": 60, "L5": 0},
    4: {"L1": 5_500, "L2": 1_100, "L3": 240, "L4": 60, "L5": 8},
    5: {"L1": 7_000, "L2": 1_600, "L3": 360, "L4": 80, "L5": 8},
}
PILOT_YEAR = 1                       # Y1 cohort is free at the point of use

# institutional contracts: hospitals buying cohorts + evaluation/advisory work
CONTRACTS = {1: 0, 2: 180_000, 3: 520_000, 4: 900_000, 5: 1_250_000}


def infl(year):
    return (1 + INFLATION) ** (year - 1)


def payroll_full():
    base = sum(n * s for _, _, n, s in ESTABLISHMENT)
    return base, base * (1 + ON_COSTS)


def main():
    base, loaded = payroll_full()
    posts = sum(n for _, _, n, _ in ESTABLISHMENT)

    print("=" * 78)
    print("ESTABLISHMENT")
    print("=" * 78)
    units = {}
    for unit, post, n, s in ESTABLISHMENT:
        units.setdefault(unit, [0, 0])
        units[unit][0] += n
        units[unit][1] += n * s
    for unit, (n, cost) in units.items():
        print(f"  {unit:24} {n:3} posts   ${cost:>9,.0f} gross")
    print(f"  {'TOTAL':24} {posts:3} posts   ${base:>9,.0f} gross")
    print(f"  {'incl. on-costs @26%':24} {'':9}   ${loaded:>9,.0f} fully loaded")
    print(f"  {'per post average':24} {'':9}   ${loaded/posts:>9,.0f}")
    assert posts == 71, f"establishment is {posts}, blueprint says 71"

    print()
    print("=" * 78)
    print("FIVE-YEAR OPERATING MODEL (USD)")
    print("=" * 78)
    hdr = f"  {'':34}" + "".join(f"{'Y'+str(y):>12}" for y in range(1, 6))
    print(hdr)

    rows, totals = {}, {}
    pay, nonpay, capex, fees, contracts = {}, {}, {}, {}, {}
    for y in range(1, 6):
        pay[y] = loaded * (FTE_BY_YEAR[y] / posts) * infl(y)

        np_steady = sum(v for k, v in NONPAY_STEADY.items()
                        if not (k.startswith("Fellowship") and y < FELLOWSHIP_FROM))
        nonpay[y] = np_steady * NONPAY_RAMP[y] * infl(y)

        capex[y] = sum(c for _, c, yr in CAPEX if yr == y)

        fees[y] = 0 if y == PILOT_YEAR else sum(
            THROUGHPUT[y][k] * FEES[k] * infl(y) for k in FEES)
        contracts[y] = CONTRACTS[y]

    def line(label, d, money=True):
        print(f"  {label:34}" + "".join(f"{d[y]:>12,.0f}" for y in range(1, 6)))

    print("\n  EXPENDITURE")
    line("Payroll (incl. on-costs)", pay)
    line("Recurrent non-pay", nonpay)
    line("Capital", capex)
    tot_exp = {y: pay[y] + nonpay[y] + capex[y] for y in range(1, 6)}
    line("Total expenditure", tot_exp)

    print("\n  INCOME")
    line("Course fees", fees)
    line("Institutional contracts and advisory", contracts)
    tot_inc = {y: fees[y] + contracts[y] for y in range(1, 6)}
    line("Total earned income", tot_inc)

    print("\n  POSITION")
    gap = {y: tot_exp[y] - tot_inc[y] for y in range(1, 6)}
    line("Subsidy required (grant/endowment)", gap)
    cover = {y: 100 * tot_inc[y] / tot_exp[y] for y in range(1, 6)}
    print(f"  {'Earned-income cover %':34}" + "".join(f"{cover[y]:>11.0f}%" for y in range(1, 6)))

    print()
    print("=" * 78)
    print("UNIT COSTS AND TOTALS")
    print("=" * 78)
    learners = {y: sum(THROUGHPUT[y][k] for k in ("L1", "L2", "L3", "L4", "L5"))
                for y in range(1, 6)}
    line("Learners certificated", learners)
    ucost = {y: tot_exp[y] / learners[y] if learners[y] else 0 for y in range(1, 6)}
    print(f"  {'Cost per learner (all-in, USD)':34}"
          + "".join(f"{ucost[y]:>12,.0f}" for y in range(1, 6)))

    five_exp = sum(tot_exp.values())
    five_inc = sum(tot_inc.values())
    five_gap = five_exp - five_inc
    five_learners = sum(learners.values())
    print()
    print(f"  Five-year expenditure          USD {five_exp:>12,.0f}   "
          f"(KES {five_exp*FX/1e6:>7,.0f} m)")
    print(f"  Five-year earned income        USD {five_inc:>12,.0f}   "
          f"(KES {five_inc*FX/1e6:>7,.0f} m)")
    print(f"  Five-year subsidy required     USD {five_gap:>12,.0f}   "
          f"(KES {five_gap*FX/1e6:>7,.0f} m)")
    print(f"  Learners certificated          {five_learners:>16,}")
    print(f"  Blended cost per learner       USD {five_exp/five_learners:>12,.0f}")
    print(f"  Subsidy per learner            USD {five_gap/five_learners:>12,.0f}")
    print(f"  Y5 earned-income cover         {cover[5]:>15.0f}%")

    print()
    print("=" * 78)
    print("SENSITIVITY — Y5 subsidy requirement (USD)")
    print("=" * 78)
    base_y5 = gap[5]
    print(f"  {'Base case':44} {base_y5:>12,.0f}")
    for label, adj in [
        ("Payroll bands 20% higher than assumed", lambda: pay[5] * 0.20),
        ("Payroll bands 20% lower than assumed",  lambda: -pay[5] * 0.20),
        ("Throughput 30% below plan",             lambda: fees[5] * 0.30),
        ("Throughput 30% above plan",             lambda: -fees[5] * 0.30),
        ("Contracts fail to materialise",         lambda: contracts[5]),
        ("Fees held at half the assumed rate",    lambda: fees[5] * 0.50),
    ]:
        print(f"  {label:44} {base_y5 + adj():>12,.0f}")

    print()
    print(f"  Break-even on earned income requires Y5 income of USD {tot_exp[5]:,.0f}")
    print(f"  — i.e. {tot_exp[5]/tot_inc[5]:.1f}x the modelled Y5 earned income.")


if __name__ == "__main__":
    main()
