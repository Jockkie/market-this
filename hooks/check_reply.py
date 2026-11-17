#!/usr/bin/env python3
"""Claude Code Stop hook for Jockkie Studio skills.

Runs when Claude finishes a reply. Only acts when this plugin's skill was used
in the session. It sends the reply back for a fix (decision "block") when:
  - the reply asks more than one question (a numbered gap list counts as one)
  - it contains a note to self or another internal remark
  - it claims a file was saved or added while no file tool was used in that turn

Usage in hooks.json: python3 ${CLAUDE_PLUGIN_ROOT}/hooks/check_reply.py <skill-name>
Reads the hook input JSON on stdin. Standard library only. Never blocks twice in
a row (respects stop_hook_active), and never fails loudly: on any error it lets
the reply through.
"""
import json
import re
import sys

META = re.compile(r"\b(note to self|todo:|internal note|i will now run|let me run the script)\b", re.I)
SAVE_CLAIM = re.compile(r"\b(saved|added|written|updated|stored)\b[^.\n]{0,60}\.(md|json|csv|html)\b|\.(md|json|csv|html)\b[^.\n]{0,40}\b(saved|added|written|updated)\b", re.I)
COMPOUND = re.compile(r",\s*(and|or|en|of)\s+((to|for|with|by|from|met|voor|aan|van)\s+)?(who|whom|what|how|when|where|which|why|wie|wat|hoe|wanneer|waar|welke|waarom)\b", re.I)
TRANSLATION = re.compile(r"^\s*[*_]*(in english|in het nederlands|translation|vertaling)\b", re.I)
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "Bash"}


def load_turn(path):
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def is_user_text(e):
    if e.get("type") != "user":
        return False
    content = (e.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return any(isinstance(c, dict) and c.get("type") == "text" for c in content or [])


def last_assistant_turn(entries):
    turn = []
    for e in reversed(entries):
        if is_user_text(e):
            break
        if e.get("type") == "assistant":
            turn.append(e)
    return list(reversed(turn))


def turn_text_and_tools(turn):
    texts, tools = [], set()
    for e in turn:
        for c in (e.get("message") or {}).get("content") or []:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "text":
                texts.append(c.get("text", ""))
            elif c.get("type") == "tool_use":
                tools.add(c.get("name", ""))
    return texts[-1] if texts else "", tools


def count_questions(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    lines = [l for l in text.splitlines() if not l.lstrip().startswith(">") and not TRANSLATION.match(l)]
    count, in_list_block = 0, False
    for line in lines:
        clean = re.sub(r"\"[^\"]*\"|“[^”]*”|'[^']*'", "", line)
        q = len(re.findall(r"\?(\s|$|\*|\))", clean + " "))
        if q:
            # "how many ..., and who ...?" joins two asks in one sentence
            for sentence in re.findall(r"[^.!?]*\?", clean):
                q += len(COMPOUND.findall(sentence))
        is_item = bool(re.match(r"\s*(\d+[.)]|[-*])\s", line))
        if is_item and q:
            if not in_list_block:
                count += 1  # a numbered gap list counts as one question
            in_list_block = True
            continue
        in_list_block = False if line.strip() else in_list_block
        count += q
    return count


def main():
    skill = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
        if data.get("stop_hook_active"):
            return
        path = data.get("transcript_path")
        if not path:
            return
        entries = load_turn(path)
        raw = "\n".join(json.dumps(e) for e in entries)
        if skill and skill not in raw:
            return  # the skill was not used in this session
        turn = last_assistant_turn(entries)
        text, tools = turn_text_and_tools(turn)
        if not text:
            return
        problems = []
        q = count_questions(text)
        if q > 1:
            problems.append(f"The reply asks {q} questions. Keep exactly one: the most important one. Move the others to later messages.")
        if META.search(text):
            problems.append("The reply contains an internal remark (a note to self or an announcement). Remove it and show only results.")
        if SAVE_CLAIM.search(text) and not (tools & FILE_TOOLS):
            problems.append("The reply says a file was saved or added, but no file was written in this turn. Print the content for the user to copy instead, or actually write the file.")
        if problems:
            print(json.dumps({"decision": "block", "reason": f"{skill} self-check: " + " ".join(problems) + " Rewrite the reply."}))
    except Exception:
        return


if __name__ == "__main__":
    main()
