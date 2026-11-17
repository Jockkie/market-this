# Self-check (visible to the user)

Run this before every gate summary and every delivery, and show the result to the user as a short block titled "Self-check". If an item fails, fix it first and say what you fixed. Never claim a check passed that you did not do.

## Checklist
1. **Sources:** `seen` only for what the user said or showed in this conversation, with their words as `quote`. Pages, pitches or accounts you have not seen are `unknown`. If you can run code: `python3 scripts/check_dossier.py dossier.json --gate <1|2|deliver>` must pass.
2. **No invented numbers:** every derived figure (conversion rate, DMs per reel, expected sales from a group, hours per test, thresholds you set) appears under "I estimated" with its basis, or is labelled "my proposal". Never write "pass" for a check that has not run.
3. **Live sources:** every platform rule or number you give has a source, a date and a confidence; nothing you did not read.
4. **One question:** your message ends with exactly one question.
5. **Gate confirmed:** the user confirmed Gate 1 and the weakest pillar themselves.
6. **Funnel arithmetic:** the plan shows what the goal takes at the current conversion and whether the hours fit.
7. **Honest marketing:** no fake reviews, scarcity or claims without proof; consent rules checked before email or outreach.
8. **Tools:** affiliate disclosure before any link; quote and cap before any paid call.
9. **Files:** you name only files that exist; the content calendar and business context are printed in full.

Write values you do not know as `unknown` (or with label `unknown`), never leave them out; list choices you made yourself (a scope, a time window, a conversion rate) in the dossier's `assumptions` list. The assumptions block may only say "none" when that is true.

## Assumptions block (in every gate summary and delivery)
Show "What you told me and what I assumed". With code: `python3 scripts/check_dossier.py dossier.json --assumptions`.
