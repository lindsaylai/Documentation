from pathlib import Path

p = Path("docs/persistent-ais/muse.md")
text = p.read_text(encoding="utf-8")
marker = '??? note "Expand the tutor text"'
start = text.find(marker)
end = text.find("\nDo not upload files from your personal computer", start)
if start < 0 or end < 0:
    raise SystemExit(f"markers not found start={start} end={end}")
head = text[:start]
block = text[start:end]
tail = text[end:]
lines = block.splitlines(True)
out = [lines[0]]
i = 1
if i < len(lines) and lines[i].strip() == "":
    out.append(lines[i])
    i += 1
for line in lines[i:]:
    if line.startswith("    "):
        out.append(line)
    elif line.strip() == "":
        out.append("    \n" if line.endswith("\n") else "    ")
    else:
        out.append("    " + line)
p.write_text(head + "".join(out) + tail, encoding="utf-8")
print("indented", len(lines) - 1, "lines")
