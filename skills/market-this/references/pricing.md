# Pricing

## Principles

1. **Price the outcome, not the hours.** What is the result worth to the buyer, compared to their real alternative?
2. **The alternative sets the frame.** Show the price next to what they spend now (an agency, an employee, the cost of the problem).
3. **Tiers when buyers differ.** Three options (basic, recommended, premium), with the middle one the one you want to sell. Name tiers by who they are for.
4. **A small first step lowers risk.** A paid pilot, audit or starter package makes a big decision small.
5. **Discounts only with a reason and a limit.** Annual payment, early commitment, a real launch window. Never as a reflex.
6. **Raise in small steps on new prospects first.** Existing customers later, with notice and a reason.

## Four ways to find the price, from cheap to rigorous

**1. Next-five test (fastest).** Quote a higher price to the next five prospects and watch the close rate. If it barely drops, the price was too low.

**2. Value calculation.** Estimate the money the outcome brings or saves per year for the buyer. A price of 10 to 30 percent of that first-year value is a common starting range for B2B; check against alternatives.

**3. Van Westendorp price sensitivity (survey).** Ask at least 30 people who fit the ICP, after a short description of the offer:
1. At what price would it be so cheap that you would doubt the quality?
2. At what price would it be a bargain, a great buy?
3. At what price would it start to feel expensive, but you would still consider it?
4. At what price would it be too expensive to consider?

Run `scripts/price_test.py` on the answers (CSV with columns `too_cheap, cheap, expensive, too_expensive`). It returns the acceptable range (from the point of marginal cheapness to the point of marginal expensiveness) and the optimal price point where "too cheap" and "too expensive" cross. The result is a direction to test, not the final price; it assumes people already understand what the product is and it ignores competitor prices.

**4. Gabor-Granger (survey).** Show one price per respondent group and ask if they would buy. Estimates demand at each price. Useful to choose between two or three candidates.

Optional: a MiroFish simulation to explore reactions to two price points (see `market-simulation.md`). Always confirm with real offers.

## Output

In the dossier under `pricing`: current price, value estimate, method used, result, chosen test, date. Label everything.
