# Montgomery AI Series — EP01 Pipeline

## Prereqs
- ComfyUI running with HTTP API
- FFmpeg in PATH
- (Optional) OpenTTS/Coqui server

## Setup
cp .env.example .env
make setup

## Generate
make images
make voices
make video
make edit
