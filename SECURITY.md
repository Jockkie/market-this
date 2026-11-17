# Security

Skills tell an AI agent what to do, and this one also runs scripts on your machine. Read this before you install, and review any skill before you enable it, from this repository or anywhere else.

## What runs, and what it can reach

| Part | What it does | Network | Writes files |
|------|--------------|---------|--------------|
| `skills/market-this/SKILL.md` and `references/` | Instructions and reference text for the agent | No | No |
| `skills/market-this/scripts/*.py` | Calculations, checks and HTML pages (Python standard library) | No | Only to the output path you or the agent pass on the command line |
| `hooks/check_reply.py` (Claude Code only) | Reads the current session transcript after each reply and can send the reply back for a fix | No | No |
| `.mcp.json` / `mcp.json` | Registers the Monid and Flora MCP servers | Only after you authenticate them with `/mcp` | No |

- No script makes a network call. You can check this yourself: none of them imports a network library.
- The hook reads the transcript Claude Code hands it, prints a decision and exits. It does not store or send anything.
- Paid tools are never used without your consent, a quote and a spending cap you set. Personal data is never sent to them.

## Supported versions

Only the latest release receives fixes.

| Version | Supported |
|---------|-----------|
| 0.1.x | Yes |

## Reporting a vulnerability

Please do not open a public issue for a security problem: it shows everyone how to use the weakness before it is fixed.

Report it privately in this repository instead: go to the **Security** tab and choose **Report a vulnerability** ([direct link](https://github.com/Jockkie/market-this/security/advisories/new)). Only the maintainer and you can see the report. Describe:

- which script, hook or instruction is affected;
- how to reproduce it;
- what an attacker could do with it.

You will get a reply within seven days. Once a fix is released, the advisory is published and you are credited in it and in the changelog, unless you prefer not to be.

No GitHub account? Email **info@jockkie.com** with "Security" in the subject line.

Prompt-injection weaknesses count as security problems too: for example, a web page or document that makes the skill ignore its own rules, spend money without consent or send data to a tool.
