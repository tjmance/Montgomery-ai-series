ENV ?= .venv
.PHONY: setup images voices video edit all

setup:
\tpython -m venv $(ENV)
\t$(ENV)/Scripts/pip install -r env/requirements.txt || $(ENV)/bin/pip install -r env/requirements.txt

images:
\tpython scripts/image_generator_comfyui.py

voices:
\tpython scripts/synth_voices_opentts.py

video:
\tpython scripts/animate_svd.py

edit:
\tbash scripts/ffmpeg_concat.sh scenes/ep01_the_static
\tpython scripts/compose_timeline.py

all: images voices video edit
