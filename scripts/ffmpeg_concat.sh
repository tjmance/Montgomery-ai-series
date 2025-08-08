#!/usr/bin/env bash
set -euo pipefail
SCENE_DIR=${1:-scenes/ep01_the_static}
TMP=list.txt
pushd "$SCENE_DIR/video" >/dev/null
ls -1 *.mp4 | sort | awk '{print "file '\'',"$0,"'\''"}' > $TMP
ffmpeg -y -f concat -safe 0 -i $TMP -c copy ../edit/ep01_preview_concat.mp4
rm -f $TMP
popd >/dev/null
