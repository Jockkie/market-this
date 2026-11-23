<img src=".claude-plugin/icon.png" alt="" width="96" height="96">

# Market This

*Part of [Jockkie Studio's](https://www.jockkie.com) open-source skills. I do the geeking. You get the easy part.*

> **Version 0.1.0, beta.** Tested in Claude; built to the specification of the other platforms but not yet tested there. See [Platform status](#platform-status), and please [report what you find](https://github.com/Jockkie/market-this/issues/new/choose).

A go-to-market skill for owners and makers who want more customers without hiring an agency. It runs a structured interview, scores the go-to-market on ten pillars, finds the weakest one and fixes that first, then builds the positioning, the channel and distribution strategy, a 90-day plan with a content calendar, a brand brief and a one-file dashboard.

Start by asking something like "nobody buys my product, help me sell it".

Optional tools, always with your consent, a quote and a spending cap: see [Optional tools](#optional-tools).

## Install

The skill folder is `skills/market-this`.

**Claude Code (plugin)**
```
/plugin marketplace add Jockkie/market-this
/plugin install market-this@market-this
```

**Claude.ai**
Zip the `skills/market-this` folder and upload it in Claude's skills settings.

**Hermes Agent (plugin)**
This repository is also a portable [Agent Plugins](https://vercel.com/kb/guide/agent-plugins) package (`plugin.json`, `skills/`, `mcp.json`), which Hermes loads natively. Copy the repository into `~/.hermes/plugins/market-this`, then `hermes plugins enable market-this`. Skill only: copy `skills/market-this` into `~/.hermes/skills/`.

**ChatGPT (Business, Enterprise, Edu)**
Zip the `skills/market-this` folder and upload it under Skills, Create, Upload.

**OpenClaw**
Copy `skills/market-this` into `~/.openclaw/skills/` (or your workspace `skills/` folder) and start a new session.

**Grok**
Import the zipped `skills/market-this` folder under Skills. For Grok Build, copy the folder into `~/.grok/skills/`.

**GitHub Copilot (VS Code, Visual Studio, Copilot CLI, cloud agent)**
Copy `skills/market-this` into `~/.copilot/skills/` for all your projects, or into `.github/skills/` in one repository.

**Codex, Cursor, Gemini CLI and other Agent Skills clients**
Copy `skills/market-this` into the client's skills directory (for example `.agents/skills/`, `.cursor/skills/`, `~/.claude/skills/`).

## Platform status

| Platform | Status | What that means |
|----------|--------|-----------------|
| Claude Code | Validated | The marketplace, manifest and hook pass `claude plugin validate`; the skill was tested in evaluation rounds with Claude models |
| Claude.ai | Skill tested | The same `SKILL.md` as in the evaluations; the zip upload itself is not yet tested |
| Hermes Agent | Untested | Built to the Agent Plugins specification |
| ChatGPT, OpenClaw, Grok, GitHub Copilot | Untested | Built to the Agent Skills format |
| Codex, Cursor, Gemini CLI and others | Untested | Built to the Agent Skills format |

The guard hook only runs in Claude Code. On other platforms, the visible self-check in the skill does that job. Tried it on an untested platform? [Tell us how it went](https://github.com/Jockkie/market-this/issues/new/choose), whether it worked or not.

## Optional tools

Everything works without paid tools. Where they help, always with your consent, a quote and a spending cap you set:

- **[Monid](https://monid.ai?fpr=jockkie)**: public market data (competitors, reviews, search demand). MCP: `https://mcp.monid.ai/v1`
- **[Flora](https://refer.flora.ai/jock-oosterveer-htu6)**: visuals in your brand style, from the brand brief the skill makes. MCP: `https://mcp.flora.ai/mcp`
- **MiroFish**: simulate how a market reacts to a launch, price or message
- **Jev** (TypeSafe): fast typed scoring as a second opinion

The Monid and Flora MCP servers are registered but do nothing until you authenticate them with `/mcp`.

**Disclosure:** the Flora and Monid links are affiliate links. Jockkie earns a commission when you create an account through them. The skill says so before it shares a link.

## How this skill keeps you from trusting a guess

AI tools sound sure of themselves, even when they are guessing. This skill is built to show you the difference:

1. **What you told me and what I assumed.** Every summary and every delivery separates what you said (with your own words), what the skill estimated (with its basis) and what is still unknown.
2. **A check before every step that matters.** Where the skill can run code, `check_dossier.py` or the skill's own script blocks the next step while a fact is labelled as yours without your words or a number has no label.
3. **A visible self-check** before every delivery: sources, invented numbers, one question at a time, files that really exist.
4. **In Claude Code, a guard.** A small hook sends a reply back for a fix when it asks several questions at once, contains an internal note, or claims a file was saved when none was written. It only acts in sessions where this skill is used.

A good habit with any AI advice: before you act on it, ask "Which of this did I tell you, and which did you assume?"

## Privacy

What you share stays with you. Personal data is never sent to external tools, and the files the skill makes are yours to keep. The skill asks for counts and roles, not names, and anonymizes exports first.

## Quality

Every change runs the script tests and checks on GitHub (`.github/workflows/tests.yml`). The skill itself is tested with written evaluation cases (`evals/evals.json`) and full simulated conversations, graded by a separate model; results are in `evals/results`.

What changed per version is in the [changelog](CHANGELOG.md). Want to help? Read [CONTRIBUTING](CONTRIBUTING.md). Found a security problem? Report it privately through the Security tab ([how](SECURITY.md)), not in a public issue.

## Credits

April Dunford's positioning, jobs to be done, the Bullseye method (Gabriel Weinberg and Justin Mares), Rob Fitzpatrick's *The Mom Test*, Peter van Westendorp's price sensitivity meter, AARRR.

## The other skills

| Skill | For |
|-------|-----|
| [Consult Anything](https://github.com/Jockkie/consult-anything) | Owners and managers whose business is stuck |
| [Copywrite Me](https://github.com/Jockkie/copywrite-me) | Anyone who needs a text that sells |
| [Find My Ikigai](https://github.com/Jockkie/find-my-ikigai) | Anyone looking for what makes life worth living |
| [Align My Astro](https://github.com/Jockkie/align-my-astro) | Anyone who likes a daily reflection |

## Need a human?

The skill refers you to the right type of professional when a problem needs one. Jockkie Studio is one of the options: helicopter view, project management and workflows, process improvement, change and innovation, go-to-market, AI implementation.

## Contact and support

- Website: https://www.jockkie.com
- Email: info@jockkie.com
- The skill is free. If it helped you: https://buymeacoffee.com/jockkie

## License

MIT
