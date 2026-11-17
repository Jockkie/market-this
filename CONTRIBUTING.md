# Contributing

Thank you for helping. Market This is for people who want to make progress without hiring a professional first, so every change is judged by one question: does it help that person get a better, more honest result?

## The easiest way to help: report a mistake

Did the skill invent a number, ask three questions at once, give advice that did not fit, or break on your platform? [Report it](https://github.com/Jockkie/market-this/issues/new/choose) with the "The skill made a mistake" template.

- **Remove personal data first.** No names, customer details, birth data or dreams. The template asks you to confirm this.
- Say which platform and which model you used.
- Paste the smallest part of the conversation that shows the problem.

Every confirmed report becomes an evaluation case, so the mistake cannot quietly come back.

Reports from platforms other than Claude are especially welcome. They are the least tested (see "Platform status" in the README).

## Ideas

Use the "Idea or improvement" template. An idea for a new skill is welcome too, as long as it fits the principle above and can be built with the same trust layer: facts labelled as seen, inferred or unknown, one question at a time, and a visible self-check.

## Changing the skill or a script

1. Fork the repository and create a branch.
2. Make one change per pull request.
3. Run the checks:
   ```
   python tests/check_skills.py
   python -m unittest discover -s tests -v
   ```
   If you have Claude Code, also run `claude plugin validate .`.
4. If you change a script, add or update a test in `tests/test_scripts.py`.
5. If you change skill behaviour, add or update a case in `evals/evals.json` that shows the old mistake and the expected behaviour.
6. Describe in the pull request what went wrong before and how you checked that it is fixed.

## House rules for skill text

- **One question per message** to the user.
- **No invented facts.** A number or claim is either the user's (with their words), an estimate (with its basis) or unknown.
- **Sources for anything about the world as it is now:** platform rules, prices, laws. Check them live and give the date.
- **Plain language.** The reader is an owner or a manager, not a consultant.
- **No em-dashes.** `tests/check_skills.py` fails on them.
- **English in the repository.** The skills answer in the user's own language.
- **Scripts use the Python standard library**, write only to paths passed on the command line, and make no network calls. Optional dependencies must stay optional.
- **Affiliate links** (Monid, Flora) are always disclosed before they are shared.

## Licence

By contributing you agree that your contribution is released under the MIT licence of this repository.

## Questions

Email info@jockkie.com or open an issue with the "Idea or improvement" template.
