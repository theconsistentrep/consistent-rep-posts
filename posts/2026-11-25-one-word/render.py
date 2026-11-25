import asyncio, sys
from playwright.async_api import async_playwright
BG="#16161A"; CREAM="#F4EFE8"; ACCENT="#FF6B3D"; MUTED="#A7A29A"
scenes=[
 ('hook', "<div class='k'>YOUR TURN</div><h1>Pick one<br>word for<br>this week.</h1><p class='sub'>Here's how I use mine <span class='a'>↓</span></p>"),
 ('intro', '<h2>One word.<br>No plan.</h2><p>I pick it before I train.<br>It keeps my head quiet<br>when the session gets hard.</p>'),
 ('s1', "<div class='n'>01</div><h2>Steady.</h2><p>For the days I want to rush<br>through everything.</p>"),
 ('s2', "<div class='n'>02</div><h2>Again.</h2><p>For the days I want to stop<br>a set early.</p>"),
 ('s3', "<div class='n'>03</div><h2>Enough.</h2><p>For the days I want to do<br>more than I need.</p>"),
 ('turn', "<h2>That's the<br>whole trick.</h2><p>One word to come back to<br>when my head <span class='a'>gets loud.</span></p>"),
 ('end', "<h1 class='e'>What's your<br><span class='a'>word</span> this<br>week?</h1><p class='sub'>Comment it below 👇<br>Follow @theconsistentrep</p>"),
]
CSS=f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:{BG};color:{CREAM};font-family:Poppins;overflow:hidden;position:relative}}
.glow{{position:absolute;width:1200px;height:1200px;border-radius:50%;left:-60px;top:260px;background:radial-gradient(circle,rgba(255,107,61,.20),rgba(255,107,61,0) 62%)}}
.f{{position:absolute;left:100px;right:100px;top:420px;bottom:520px;display:flex;flex-direction:column;justify-content:center}}
.k{{font-family:Inter;font-weight:600;letter-spacing:8px;font-size:30px;color:{ACCENT};margin-bottom:50px}}
h1{{font-weight:800;font-size:150px;line-height:1.02;letter-spacing:-3px}}
h1.e{{font-size:108px}}
h2{{font-weight:800;font-size:132px;line-height:1.02;letter-spacing:-3px;margin-top:20px}}
.n{{font-weight:800;font-size:260px;line-height:.85;color:transparent;-webkit-text-stroke:5px {ACCENT}}}
p{{font-family:Inter;font-size:54px;line-height:1.35;opacity:.88;margin-top:50px}}
.sub{{color:{MUTED};opacity:1}}
.a{{color:{ACCENT}}}
.bar{{width:110px;height:12px;border-radius:6px;background:{ACCENT};margin-top:60px}}"""
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        for name,inner in scenes:
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body><div class='glow'></div><div class='f'>{inner}<div class='bar'></div></div></body></html>")
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=f"{name}.png")
        await b.close()
asyncio.run(m())
