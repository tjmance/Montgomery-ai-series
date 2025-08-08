import os, json, time, uuid
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
COMFY = os.getenv("COMFY_HOST", "http://127.0.0.1:8188")
SCENE_DIR = Path("scenes/ep01_the_static")
WF = Path("comfyui/workflows/sd_establishing_plates_api.json")
PROMPTS = json.loads(Path("prompts/scenes.json").read_text())

OUT_DIR = SCENE_DIR/"images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def submit_workflow(prompt_text: str, out_name: str):
    wf = json.loads(WF.read_text())
    # Replace POS_PROMPT text
    for node_id, node in wf["nodes"].items():
        if node.get("class_type") == "CLIPTextEncode" and "POS_PROMPT" in node.get("_meta", {}).get("title", ""):
            node["inputs"]["text"] = prompt_text
    # Save target filename prefix
    for node_id, node in wf["nodes"].items():
        if node.get("class_type") == "SaveImage":
            node["inputs"]["filename_prefix"] = out_name

    rid = str(uuid.uuid4())
    r = requests.post(f"{COMFY}/prompt", json={"prompt": wf, "client_id": rid}, timeout=120)
    r.raise_for_status()

    # poll until completed
    while True:
        time.sleep(1)
        h = requests.get(f"{COMFY}/history/{rid}")
        if h.ok:
            data = h.json()
            if data and list(data.values())[0].get("status") == "completed":
                break

if __name__ == "__main__":
    shotlist = (SCENE_DIR/"shotlist.csv").read_text().strip().splitlines()[1:]
    for row in shotlist:
        clip_id, loc, desc, dur, prompt_ref, audio_ref = [s.strip() for s in row.split(',')]
        ptxt = PROMPTS[prompt_ref]
        out = f"{clip_id}_{prompt_ref}"
        print(f"[ComfyUI] {clip_id} -> {prompt_ref}")
        submit_workflow(ptxt, out)
