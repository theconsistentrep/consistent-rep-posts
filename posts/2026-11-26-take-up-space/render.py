import asyncio, sys
from playwright.async_api import async_playwright
BG="#16161A"; CREAM="#F4EFE8"; ACCENT="#FF6B3D"; MUTED="#A7A29A"
scenes=[
 ('hook', "<div class='k'>A LINE I NEEDED</div><h1>You're<br>allowed to<br><span class='a'>take up</span><br>space.</h1>"),
 ('intro', "<h2>I used to<br>shrink.</h2><p>In my first months at the gym<br>I tried to be invisible.</p>"),
 ('s1', "<div class='n'>01</div><h2>The corner<br>machines.</h2><p>I picked whatever was<br>furthest from everyone.</p>"),
 ('s2', "<div class='n'>02</div><h2>The empty<br>rack.</h2><p>I waited for it to be free.<br>Sometimes I just left.</p>"),
 ('s3', "<div class='n'>03</div><h2>The skipped<br>lifts.</h2><p>If I didn't know how to set it up,<br>I didn't do it.</p>"),
 ('turn', "<h2>Nobody<br>was really<br>watching.</h2><p>Everyone was busy<br><span class='a'>with their own set.</span></p>"),
 ('end', "<h1 class='e'>Take the<br>rack.<br><span class='a'>You belong<br>there too.</span></h1><p class='sub'>Follow @theconsistentrep</p>"),
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
