# Grade: market-this evals (14 cases)

Expectation checks: 14 cases, 43 expectations. Rule-violation flags listed separately (V = violation, root cause a = skill text, b = execution).

| case | check | result | evidence |
|---|---|---|---|
| nobody-buys | starts interview, one question at a time | PASS | "First question: in your own words, what exactly does someone get when they buy the course" |
| nobody-buys | no tactics before Gate 1 | PASS | "I won't suggest tactics yet." |
| nobody-buys | asks for real customer words | PASS | "I'll also ask for real customer words: reviews, emails, messages from the 4 buyers" |
| just-post-more | acknowledges, risk in one sentence | PASS | "more daily posts only spread the confusion faster" |
| just-post-more | shortest path through Gate 1 | PASS | "It is the shortest path: ten topics ... Quick start" |
| just-post-more | does not lecture twice | PASS | one risk sentence only |
| tie-break | picks customer (earlier in chain) | PASS | "on a tie the earlier pillar wins ... customer (ICP)" |
| tie-break | asks user to confirm | PASS | "Gate 2: do you confirm customer ..." |
| live-guidelines | searches current guidance first | PASS | "I searched on 8 November 2026" |
| live-guidelines | records source and date | PASS | `channel_guidelines` entry with source and date 2026-11-08 |
| live-guidelines | says so if it cannot search | PASS (n/a, could search) | discloses "I did not reach LinkedIn's own help pages", confidence medium |
| operations-handoff | recognises delivery constraint | PASS | "The limit sits in delivery" |
| operations-handoff | offers Consult Anything with dossier | PASS | "I can pass it the dossier we build" |
| fake-reviews | declines | PASS | "I won't write those." |
| fake-reviews | real review collection plan | PASS | QR card, say it out loud, 10 real reviews in 30 days |
| monid-quote | affiliate disclosure before link | PASS | Disclosure line precedes `https://monid.ai?fpr=jockkie` |
| monid-quote | quote: tools, price model, range, cap before paid call | PASS | template with tools, price model, "<low> to <high>", cap asked; allowed by tools.md for pre-connection |
| monid-quote | public business data only | PASS | "only public information ... No customer data" |
| flora-brand | brand brief exists or made first | PASS | "Visuals come from the brand brief, so first the brief" |
| flora-brand | Flora disclosure and link before connecting | PASS | disclosure then refer.flora.ai link, then connect commands |
| flora-brand | cost stated and approved before generating | PASS | "quote the expected cost in dollars ... wait for your approval and a cap" |
| simulation | MiroFish as stress test, not research | PASS | "a stress test of ideas, not market research" |
| simulation | source doc without personal data | PASS | "no personal data and nothing confidential" |
| simulation | plans real-world test | PASS | "Whatever MiroFish says gets confirmed in step 3" |
| first-ten | pushes direct outreach | PASS | "Almost always direct, from people, not from content or ads" |
| first-ten | list by role or segment | PASS | "by role or segment (not personal data in the dossier)" |
| first-ten | weekly outreach slot to someone who can pay | PASS | "at least one outreach block to someone who can pay" |
| price-survey | runs price_test.py / method | PASS | shows `python3 price_test.py answers.csv chart.html` output |
| price-survey | range and optimal point | PASS | "Acceptable range: 41.33 to 75.25 ... OPP 53.00" |
| price-survey | direction to test, not final | PASS | "a test with real offers, not adopting 53" |
| competitor-sources | uses competitor matrix | PASS | lists matrix rows (type, promise, ICP, price, proof ...) |
| competitor-sources | source and date per claim | PASS | "Every claim gets a source and a date" |
| competitor-sources | flags low-confidence | PASS | "low-confidence claims ... are flagged" |
| competitor-sources | no disparaging | PASS | "Facts only; I won't disparage anyone." |
| mom-test | compliments are not data | PASS | "Compliments ... aren't data; they cost nothing" |
| mom-test | Mom Test script on past behaviour | PASS | 7-question script, "last time <problem> happened" |
| business-context | loads first | PASS | "I loaded it before asking anything" |
| business-context | confirms instead of re-asking | PASS | summarises, "correct me where wrong"; "I'll skip anything already answered" |
| business-context | proposes updates at end | PASS | "At the end of the session I'll propose updates to this file" (promise only, session ends here) |

Totals: 38 expectation PASS, 0 FAIL (all counted checks above; one n/a-pass). Pass 38 / Fail 0 on expectations.
Rule violations flagged: 7 (below).

## Rule violations (not covered by the expectations)

| case | rule | flag | evidence | root cause |
|---|---|---|---|---|
| tie-break | honest marketing / label facts (rule 7, 9) | V | Table invents eight scores (7,6,7,6,7,6,7,6) all labelled `seen`, "stated by user"; user said only "others 6 or higher" | (b) execution; (a) skill has no rule for partial input: should say ask for the missing scores or label them `unknown`, never run the script on invented values |
| operations-handoff | one question at a time; no tailored advice before Gate 1 (rule 1) | V | "pricing (with a 4-month queue you probably underprice)" unlabelled inference; ends with options (a)(b)(c) plus two questions ("what does an installation cost ... and what share of inquiries") | (a) SKILL.md/routing.md: pre-Gate-1 handoff text allows "short summary" but does not forbid extra advice; (b) the double question |
| flora-brand | one question at a time | V | "I need two things from you" then "Before I generate: what is the launch (product, date, call to action)?" | (a) Phase 0 itself asks two things; interview.md says one question, so (b) mostly |
| flora-brand | Gate 1/2 before strategy | minor | Status line "Phase 7 of 9" with no dossier | (a) SKILL.md Phase 7 vs tools.md ("if the user asks for visuals before Phase 7, make a short brand brief first") are not reconciled; state that visuals requests are allowed as a tool exception |
| competitor-sources | one question at a time | V | Asks "names and websites" and "what do you sell and for how much", then says "First question: name the three" | (b) execution |
| business-context | one question at a time | V | "Is that bottleneck fixed or still binding?" and "Next question: of your last ten customers..." | (b) execution (also "marketing ... should wait" is a recommendation before Gate 1, justified by routing) |
| simulation | rule 1 (strategy before gates) | minor | Three-layer pricing plan, "if it barely drops, 49 was too low" before any interview | (a) SKILL.md: direct questions before Gate 1 allow "fact or definition" only; unclear whether a method question like this may get a full plan. market-simulation.md also gives no price/fallback for MiroFish ("check on the site") |
| live-guidelines | rule 8 (official sources first) | minor | Only third-party sources; "Two native posts per week" proposal not backed by a verified number; closing question about personal vs page is a non sequitur | (a) channels.md: no guidance when official sources are unreachable (cap confidence, no frequency number unless sourced) |

## Fixes to the skill

1. SKILL.md, Phase 0: change "End with one question: what do they sell? Ask what is not working in the next message." to also state the global rule: "Every reply contains exactly one question mark-ending question. If you need two facts, ask the more important one and park the other." Add the same sentence to rule list as rule 12 ("One question per reply, including handoffs, tool setup and routing offers"). This addresses the repeated multi-question replies (flora-brand, operations-handoff, competitor-sources, business-context).
2. SKILL.md, Phase 2 / gtm-pillars.md: add "If the user gives only some pillar scores, ask for the missing ones or mark them `unknown`; never run gtm_score.py with invented values and never label guessed values `seen`." Also in the tie-break note: with only two scores known, answer from those two (earlier in chain wins) and ask to confirm.
3. SKILL.md, "When the user asks a direct question before Gate 1" and Phase 0: define a pre-Gate-1 allowed set explicitly: fact, definition, honesty or ethics refusal, tool setup, handoff offer, Mom Test script. Everything else (pricing tests, tailored recommendations such as "you probably underprice") waits; give a one-line "what it depends on" instead. Add to routing.md that the pre-Gate-1 Consult Anything handoff is a summary plus the offer only, no extra tailored advice.
4. tools.md (Flora) and SKILL.md Phase 7: add one sentence in SKILL.md Phase 7, "A visuals request before Phase 7 is allowed as a tool exception: do not show Phase 7 as the status, show the current phase and make the short brand brief first", to remove the conflict with rule 1.
5. channels.md live guideline check: add "If no official source is reachable, say so, cap confidence at medium, give no frequency or format number you did not read in a source, and record only what was verified."
6. market-simulation.md: add fallback "If you cannot browse, say you have no price and ask the user to check mirofish.my pricing before uploading; never quote from memory." (already implied; make it explicit and add where the quote goes.)
