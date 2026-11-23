#!/usr/bin/env python3
"""Build dist/<skill>.zip with SKILL.md at the root, for uploads to Microsoft Copilot,
Claude.ai, ChatGPT and Grok. The check compares file names and contents, so a different zlib
or file mode on another machine does not count as a change.

    python3 tools/build_zip.py          # build
    python3 tools/build_zip.py --check  # fail if dist/<skill>.zip is out of date
"""
import io, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"__pycache__", ".DS_Store"}


def build():
    skills = os.path.join(ROOT, "skills")
    (name,) = [d for d in os.listdir(skills) if os.path.isdir(os.path.join(skills, d))]
    src = os.path.join(skills, name)
    files = []
    for base, dirs, names in os.walk(src):
        dirs[:] = sorted(d for d in dirs if d not in SKIP)
        files += [os.path.join(base, n) for n in sorted(names) if n not in SKIP and not n.endswith(".pyc")]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):
            info = zipfile.ZipInfo(os.path.relpath(f, src).replace(os.sep, "/"), date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = (0o755 if os.access(f, os.X_OK) else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, open(f, "rb").read())
    return name, buf.getvalue()


def main():
    name, data = build()
    out = os.path.join(ROOT, "dist", name + ".zip")
    if "--check" in sys.argv:
        def contents(b):
            with zipfile.ZipFile(io.BytesIO(b)) as z:
                return {i.filename: z.read(i) for i in z.infolist()}
        if not os.path.exists(out) or contents(open(out, "rb").read()) != contents(data):
            print(f"dist/{name}.zip is out of date: run python3 tools/build_zip.py")
            sys.exit(1)
        print(f"dist/{name}.zip is up to date")
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "wb").write(data)
    print(f"wrote dist/{name}.zip ({len(data)} bytes)")


if __name__ == "__main__":
    main()
