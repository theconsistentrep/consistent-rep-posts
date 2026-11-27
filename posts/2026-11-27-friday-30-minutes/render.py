import asyncio, sys
from playwright.async_api import async_playwright
BG="#16161A"; CREAM="#F4EFE8"; ACCENT="#FF6B3D"; MUTED="#A7A29A"
scenes=[
 ("hook", "<div class='k'>MY WORKOUT TODAY</div><h1>Friday.<br>30 minutes.</h1><p class='sub'>The 3 moves I do<br>when time is short <span class='a'>↓</span></p>"),
 ("intro", "<h2>Busy<br>day.</h2><p>So I keep it short,<br>I keep it simple,<br>and I keep it.</p>"),
 ("s1", "<div class='n'>01</div><h2>Kettlebell<br>swings.</h2><p>Quick, loud, and they<br>wake me right up.</p>"),
 ("s2", "<div class='n'>02</div><h2>Push&#8209;ups.</h2><p>On my knees when I need to.<br>Every rep still counts.</p>"),
 ("s3", "<div class='n'>03</div><h2>Step&#8209;ups.</h2><p>One leg at a time.<br>Slow and steady on the box.</p>"),
 ("turn", "<h2>Thirty<br>minutes.<br><span class='a'>Still counts.</span></h2><p>A short session beats<br>the perfect one I never start.</p>"),
 ("end", "<h1 class='e'>Short session.<br>Full effort.<br><span class='a'>Week done.</span></h1><p class='sub'>Follow @theconsistentrep</p>"),
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
