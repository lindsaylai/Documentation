from pathlib import Path

page = Path("docs/persistent-ais/muse.md")
source = Path("docs/assets/persistent-ais/data8-tutor-paste-into-chat.txt")
text = page.read_text(encoding="utf-8")
tutor = source.read_text(encoding="utf-8").rstrip("\n")
preview = "\n".join(tutor.splitlines()[:8])

start = text.find("Paste the entire file as the first message")
end = text.find("\nDo not upload files from your personal computer")
if start < 0 or end < 0:
    raise SystemExit(f"markers not found start={start} end={end}")

replacement = f'''Paste the entire file as the first message in the side chat. Expand
the preview below to copy the full tutor text, or
[download it](../assets/persistent-ais/data8-tutor-paste-into-chat.txt).

<details class="tutor-snippet">
<summary>
<span class="tutor-snippet__preview">{preview}</span>
<span class="tutor-snippet__action tutor-snippet__action--show">Show the full tutor text</span>
<span class="tutor-snippet__action tutor-snippet__action--hide">Hide the full tutor text</span>
</summary>

```text
{tutor}
```

</details>
'''

page.write_text(text[:start] + replacement + text[end + 1 :], encoding="utf-8")
print("rewrote tutor snippet")
