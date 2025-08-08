import subprocess
from pathlib import Path

SCENE = Path('scenes/ep01_the_static')
IMG_DIR = SCENE/'images'
VID_DIR = SCENE/'video'
VID_DIR.mkdir(parents=True, exist_ok=True)

for img in sorted(IMG_DIR.glob('*.png')):
    out = VID_DIR/(img.stem + '.mp4')
    subprocess.run([
      'ffmpeg','-y','-loop','1','-t','4','-i',str(img),
      '-vf','scale=1280:-2','-r','24','-pix_fmt','yuv420p',str(out)
    ], check=True)
