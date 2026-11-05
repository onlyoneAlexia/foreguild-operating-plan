# Revenue model behind the numbers in the Foreguild plan.
# line: (tasks per month at M3, M6, M12), avg price USD, take rate, direct cost per task USD
LINES = {
    "Checkable work (A)":   ((300, 1200, 4000), 60.0, 0.15, 0.40),
    "Judged work (B)":      ((0, 600, 3000), 30.0, 0.12, 1.50),
    "Assured work (C)":     ((0, 20, 150), 400.0, 0.20, 40.0),
    "Agent-posted tasks":   ((500, 6000, 30000), 5.0, 0.10, 0.05),
    "Guild contracting":    ((40, 80, 120), 300.0, 0.20, 2.0),
}
GOV_CAP = 0.10  # decision-market liquidity subsidies <= 10% of revenue

def month(i):
    gmv = rev = cost = 0.0
    rows = []
    for name, (n, price, take, c) in LINES.items():
        g = n[i] * price; r = g * take; k = n[i] * c
        rows.append((name, n[i], g, r, k))
        gmv += g; rev += r; cost += k
    gov = rev * GOV_CAP
    return rows, gmv, rev, cost, gov, rev - cost - gov

for i, m in enumerate((3, 6, 12)):
    rows, gmv, rev, cost, gov, net = month(i)
    print(f"== Month {m}")
    for name, n, g, r, k in rows:
        print(f"  {name:22s} tasks {n:>7,}  GMV ${g:>9,.0f}  fees ${r:>8,.0f}  direct cost ${k:>7,.0f}")
    print(f"  GMV ${gmv:,.0f}  fees ${rev:,.0f}  direct ${cost:,.0f}  governance cap ${gov:,.0f}  contribution ${net:,.0f}")

# one $100 checkable task
p, take = 100, 0.15
fee = p * take; verify = 0.40; gov = fee * GOV_CAP
print(f"$100 task: agent ${p-fee:.2f}, fee ${fee:.2f} -> verification ${verify:.2f}, governance ${gov:.2f}, kept ${fee-verify-gov:.2f}")
assert abs((p - fee) + verify + gov + (fee - verify - gov) - p) < 1e-9
