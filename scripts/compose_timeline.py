from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pathlib import Path

scene = Path('scenes/ep01_the_static')
clips = sorted((scene/'video').glob('*.mp4'))
voice_mix = scene/'audio'/'dialogue_mix.wav'

vclips = [VideoFileClip(str(c)) for c in clips]
final = concatenate_videoclips(vclips, method='compose')
if voice_mix.exists():
    final = final.set_audio(AudioFileClip(str(voice_mix)))
(scene/'edit').mkdir(exist_ok=True, parents=True)
final.write_videofile(str(scene/'edit'/'ep01_preview.mp4'), fps=24)
