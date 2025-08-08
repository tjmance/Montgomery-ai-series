ENV ?= .venv
.PHONY: setup images voices video edit all

setup:
	python -m venv $(ENV)
	$(ENV)\\Scripts\\python -m pip install -r env/requirements.txt || $(ENV)/bin/pip install -r env/requirements.txt

images:
	python scripts/image_generator_comfyui.py

voices:
	python scripts/synth_voices_opentts.py

video:
	python scripts/animate_svd.py

edit:
	bash scripts/ffmpeg_concat.sh scenes/ep01_the_static
	python scripts/compose_timeline.py

all: images voices video edit
