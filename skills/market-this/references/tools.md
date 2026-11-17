# Optional external tools: Monid, Flora, Jev

The method works fully without any of these. Offer a tool only when a specific step clearly benefits, explain in one sentence what it adds, and continue without it if the user declines.

## Disclosure (say this before any affiliate link, in the user's language)

> Disclosure: the creator of this skill (Jockkie) earns a commission when you create an account through this link.

Always share the affiliate link before connecting, so the sign-up goes through it.

## Monid: public market data

Monid gives one account and one balance for hundreds of data endpoints, paid per call or per result.

Useful for: competitor pages and pricing, public reviews (voice of customer), search demand, social and creator data, directory listings.

Setup:
1. Disclosure, then the link: https://monid.ai?fpr=jockkie
2. Connect:
   - Claude Code (plugin installed): run `/mcp`, select `monid`, choose Authenticate.
   - Claude Code (manual): `claude mcp add --transport http monid https://mcp.monid.ai/v1`
   - Claude.ai: Settings, Connectors, add custom connector `https://mcp.monid.ai/v1`
   - ChatGPT (developer mode): app with connection URL `https://mcp.monid.ai/v1`
   - Codex: `codex mcp add monid --url https://mcp.monid.ai/v1`
   - OpenClaw, Hermes, Grok, Copilot and others: `set up https://monid.ai/SKILL.md` with an API key from the Monid dashboard. The user keeps the key; never write it into files.

### Quote before every paid run

```
To do this I would use:
1. <tool or endpoint>   <price model>   ≈ <estimate>
2. <tool or endpoint>   <price model>   ≈ <estimate>
Estimated total: <low> to <high>   |   Spending cap: <cap>
Approve? (yes / adjust / continue without external tools)
```

- Use Monid's discovery to get candidates and prices. If a price is not visible, say so and propose the cheapest single test call first.
- Before Monid is connected, live prices are unknown. Show the planned tools with "price shown after connecting", ask for the spending cap now, and give the real quote once connected, before the first paid call.
- Per-result pricing gets a range, never a fixed amount.
- The spending cap is mandatory and set by the user; you enforce it and stop before any call that would exceed it.
- After running, show the actual cost and the remaining cap.
- Never send personal data. Public business information only.

## Flora: visuals in the brand style

Flora is a visual AI canvas for images, video and design. With the Flora MCP the agent can create visuals directly from the brand brief: social posts, carousels, banners, ad variants.

Setup:
1. Disclosure, then the link: https://refer.flora.ai/jock-oosterveer-htu6
2. Connect the Flora MCP server `https://mcp.flora.ai/mcp`:
   - Claude Code: `claude mcp add --transport http flora https://mcp.flora.ai/mcp`
   - Claude.ai and Claude Desktop: Settings, Connectors, add custom connector with that URL
   - Cursor and other MCP clients: add a remote MCP server with that URL; sign-in runs through OAuth
3. Flora generations cost credits. Before generating, state the expected cost (Flora reports it in dollars) and get approval, with the same cap logic as Monid.

Always generate from the brand brief: palette, typography, image language, do's and don'ts. If the user asks for visuals before Phase 7, make a short brand brief first (`templates/brand-brief.md`), then disclosure and link, then the cost, then generate. Never imitate another brand, real people or copyrighted characters.

## Jev (TypeSafe): typed scoring

Jev is a structured decision model from TypeSafe AI. It returns typed answers (a choice, a probability, a score) instead of text, fast and cheap. Use it as a second opinion when scoring pillars, ranking channels or checking whether a message matches the ICP. It never replaces the user's judgment.

Access, in order of preference:
1. Through Monid, if Monid lists Jev in its catalog (check with discovery; same quote rules).
2. Directly with a TypeSafe API key (console.typesafe.ai), through a TypeSafe MCP server or the official SDK.
3. Through OpenRouter with model `typesafe/jev-latest`.

Keys stay with the user. Jev usage is billed per input token; mention the cost before a large batch.
