import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BG = "#16161A"; CREAM = "#F4EFE8"; ACCENT = "#FF6B3D"; MUTED = "#A7A29A"

slides = [
    {"kind": "cover",
     "kicker": "THE CONSISTENT REP",
     "title": "5 lines I tell<br>myself before<br><span class='a'>I train.</span>",
     "foot": "Swipe →"},
    {"kind": "habit", "n": "01", "title": "Just start<br>the warm-up.",
     "body": "I don't promise myself a full session. Once I'm moving, I usually keep going."},
    {"kind": "habit", "n": "02", "title": "Today doesn't have to be a PR.",
     "body": "Some days the win is<br>simply that I trained."},
    {"kind": "habit", "n": "03", "title": "Future me<br>will be glad.",
     "body": "I've never once regretted a session.<br>I've regretted plenty of skipped ones."},
    {"kind": "habit", "n": "04", "title": "I'm not<br>starting over.",
     "body": "Every session adds to the last one.<br>Even an average day counts."},
    {"kind": "habit", "n": "05", "title": "Done beats perfect.",
     "body": "A messy workout still counts.<br>A perfect plan I never start doesn't."},
    {"kind": "cta",
     "title": "Talk to<br>yourself<br><span class='a'>kindly.</span>",
     "body": "Which line do you need most today? Comment 1–5.",
     "foot": "Follow @theconsistentrep for the real, unfiltered process."},
]

CSS = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; background:{BG}; color:{CREAM};
  font-family:'Poppins',sans-serif; position:relative; overflow:hidden; }}
.a {{ color:{ACCENT}; }}
.frame {{ position:absolute; inset:0; padding:110px 100px; display:flex; flex-direction:column; }}
.kicker {{ font-family:'Inter'; font-weight:600; letter-spacing:6px; font-size:26px; color:{ACCENT}; }}
.bar {{ width:90px; height:10px; background:{ACCENT}; border-radius:5px; margin:40px 0 50px; }}
h1 {{ font-weight:800; line-height:1.05; letter-spacing:-2px; }}
.cover h1 {{ font-size:118px; margin-top:auto; }}
.foot {{ margin-top:auto; font-family:'Inter'; font-size:30px; color:{MUTED}; display:flex; justify-content:space-between; }}
.num {{ font-weight:800; font-size:300px; line-height:.8; color:transparent; -webkit-text-stroke:4px {ACCENT}; }}
.habit h1 {{ font-size:92px; margin-top:auto; }}
.body {{ font-family:'Inter'; font-size:44px; line-height:1.4; color:{CREAM}; opacity:.85; margin-top:44px; max-width:860px; }}
.cta h1 {{ font-size:140px; margin-top:auto; }}
.dots {{ display:flex; gap:12px; }}
.dot {{ width:14px; height:14px; border-radius:7px; background:#3A3A40; }}
.dot.on {{ background:{ACCENT}; width:40px; }}
.glow {{ position:absolute; width:900px; height:900px; border-radius:50%;
  background:radial-gradient(circle, rgba(255,107,61,.18), rgba(255,107,61,0) 65%); right:-350px; top:-350px; }}
"""

def dots(i):
    return "<div class='dots'>" + "".join(
        f"<div class='dot{' on' if j==i else ''}'></div>" for j in range(len(slides))) + "</div>"

def html(i, s):
    if s["kind"] == "cover":
        inner = f"""<div class='frame cover'><div class='kicker'>{s['kicker']}</div>
        <h1>{s['title']}</h1><div class='bar'></div>
        <div class='foot'><span>{s['foot']}</span>{dots(i)}</div></div>"""
    elif s["kind"] == "habit":
        inner = f"""<div class='frame habit'><div class='num'>{s['n']}</div>
        <h1>{s['title']}</h1><div class='body'>{s['body']}</div><div class='bar'></div>
        <div class='foot'><span>@theconsistentrep</span>{dots(i)}</div></div>"""
    else:
        inner = f"""<div class='frame cta'><div class='kicker'>THE CONSISTENT REP</div>
        <h1>{s['title']}</h1><div class='body'>{s['body']}</div><div class='bar'></div>
        <div class='foot'><span>{s['foot']}</span></div></div>"""
    return f"<html><head><style>{CSS}</style></head><body><div class='glow'></div>{inner}</body></html>"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080, "height":1350})
        for i, s in enumerate(slides):
            await pg.set_content(html(i, s)); await pg.wait_for_timeout(150)
            png = OUT / f"slide{i+1}.png"
            await pg.screenshot(path=str(png))
            Image.open(png).convert("RGB").save(OUT / f"consistent-rep_lines_{i+1}.jpg", quality=92)
            png.unlink()
        await b.close()

asyncio.run(main())
