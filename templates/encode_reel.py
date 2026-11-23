"""Encode Reel stills into an MP4.
Usage: python3 encode_reel.py <folder> name:seconds [name:seconds ...]
Each still gets a slow 4% push-in, 0.3s fade in/out, 30fps H.264 + silent AAC.
Aim for 30-40s total: ~4s hook, ~5s per content scene, ~6s end card."""
import subprocess, sys
from pathlib import Path
d = Path(sys.argv[1]); scenes = [a.split(':') for a in sys.argv[2:]]
inp, fil = [], []
for i, (n, t) in enumerate(scenes):
    t = float(t); fr = int(t * 30)
    inp += ['-loop', '1', '-framerate', '30', '-t', str(t), '-i', str(d / f'{n}.png')]
    fil.append(f"[{i}]scale=2160:3840,zoompan=z='1+0.04*on/{fr}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,"
               f"format=yuv420p,fade=t=in:st=0:d=0.3,fade=t=out:st={t-0.3}:d=0.3[v{i}]")
total = sum(float(t) for _, t in scenes)
fil.append(''.join(f'[v{i}]' for i in range(len(scenes))) + f'concat=n={len(scenes)}:v=1:a=0[v]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inp, '-f', 'lavfi', '-t', str(total), '-i', 'anullsrc=r=44100:cl=stereo',
    '-filter_complex', ';'.join(fil), '-map', '[v]', '-map', f'{len(scenes)}:a', '-c:v', 'libx264', '-profile:v', 'high',
    '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', str(d / 'reel.mp4')], check=True)
print(f'{d}/reel.mp4 {total}s')
