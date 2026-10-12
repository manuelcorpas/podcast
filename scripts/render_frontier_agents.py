#!/usr/bin/env python3
"""Reusable frontier-agentic-AI spoken masterclass renderer.

Dry-run needs no credentials: python3 scripts/render_frontier_agents.py --script FILE --output OUT --dry-run
Render uses OPENAI_API_KEY: python3 scripts/render_frontier_agents.py --script FILE --output OUT
No secrets are saved, printed or committed.  Requires ffmpeg and ffprobe.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

ENDPOINT = "https://api.openai.com/v1/audio/speech"

def run(args, *, check=True):
    return subprocess.run(args, check=check, text=True, capture_output=True)

def seconds(path: Path) -> float:
    p=run(["ffprobe","-v","error","-show_entries","format=duration",
           "-of","default=noprint_wrappers=1:nokey=1",str(path)])
    return float(p.stdout.strip())

def split_script(text: str, limit: int=2850) -> list[str]:
    """Chunk on paragraphs, then sentence boundaries; never discard content."""
    paras=[p.strip() for p in re.split(r"\n\s*\n",text) if p.strip()]
    chunks=[]
    current=""
    def emit():
        nonlocal current
        if current.strip(): chunks.append(current.strip())
        current=""
    for para in paras:
        if len(para) <= limit:
            if len(current)+len(para)+2>limit: emit()
            current+=("\n\n" if current else "")+para
            continue
        for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z])",para):
            if len(sentence)>limit:
                words=sentence.split()
                for w in words:
                    if len(current)+len(w)+1>limit: emit()
                    if len(w)>limit: raise ValueError("An individual word exceeds input limit")
                    current+=(" " if current else "")+w
            else:
                if len(current)+len(sentence)+1>limit: emit()
                current+=(" " if current else "")+sentence
        emit()
    emit()
    assert all(0<len(x)<=limit for x in chunks)
    return chunks

def synthesise(i:int, text:str, work:Path, model:str, voice:str, key:str, retries:int=3) -> tuple[int,Path,float]:
    audio=work/f"segment_{i:03d}.mp3"
    if audio.is_file() and audio.stat().st_size>30000:
        try: return i,audio,seconds(audio)
        except (subprocess.CalledProcessError,ValueError): audio.unlink()
    payload={"model":model,"voice":voice,"response_format":"mp3","speed":1.0,"input":text}
    data=work/f"segment_{i:03d}.json"
    data.write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
    last=""
    for attempt in range(retries):
        p=run(["curl","-f","-sS","--connect-timeout","15","--max-time","240",
               "-X","POST",ENDPOINT,"-H",f"Authorization: Bearer {key}",
               "-H","Content-Type: application/json",
               "--data-binary","@"+str(data),"-o",str(audio)],check=False)
        if p.returncode==0 and audio.exists() and audio.stat().st_size>30000:
            try: return i,audio,seconds(audio)
            except (ValueError,subprocess.CalledProcessError): pass
        last=(p.stderr or f"curl returncode {p.returncode}")[-300:]
        time.sleep((attempt+1)*2)
    raise RuntimeError(f"TTS segment {i} failed: {last}")

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--script",required=True,type=Path)
    a.add_argument("--output",required=True,type=Path)
    a.add_argument("--target-minutes",type=float,default=30)
    a.add_argument("--model",default="tts-1-hd")
    a.add_argument("--voice",default="onyx")
    a.add_argument("--workers",type=int,default=4)
    a.add_argument("--dry-run",action="store_true")
    args=a.parse_args()
    if args.target_minutes<5 or args.target_minutes>90: a.error("Choose 5 to 90 minutes")
    if args.workers<1 or args.workers>6: a.error("Choose 1 to 6 workers")
    text=args.script.read_text(encoding="utf-8")
    if len(text.split())<700: a.error("Transcript is too short for a full masterclass")
    chunks=split_script(text)
    print(json.dumps({"script":str(args.script),"words":len(text.split()),
        "segments":len(chunks),"target_minutes":args.target_minutes,
        "model":args.model,"voice":args.voice,"output":str(args.output)},indent=2),flush=True)
    if args.dry_run: return
    key=os.environ.get("OPENAI_API_KEY")
    if not key: a.error("OPENAI_API_KEY is required for audio synthesis")
    for tool in ("ffmpeg","ffprobe","curl"):
        if run(["/usr/bin/env","which",tool],check=False).returncode:
            a.error(f"Missing dependency: {tool}")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    work=args.output.parent/(".render_"+args.output.stem)
    work.mkdir(parents=True,exist_ok=True)
    results={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs=[pool.submit(synthesise,i,s,work,args.model,args.voice,key)
              for i,s in enumerate(chunks)]
        for f in concurrent.futures.as_completed(futs):
            i,p,dur=f.result()
            results[i]=(p,dur)
            print(f"segment {i+1}/{len(chunks)}: {dur:.1f}s",flush=True)
    concat=work/"concat.txt"
    concat.write_text("".join("file '"+str(results[i][0]).replace("'","'\\''")+"'\n"
                        for i in range(len(chunks))))
    joined=work/"joined.mp3"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y",
         "-f","concat","-safe","0","-i",str(concat),"-c","copy",str(joined)])
    raw_seconds=seconds(joined)
    requested=args.target_minutes*60
    factor=raw_seconds/requested
    if factor<0.85 or factor>1.20:
        raise RuntimeError(f"Script is poorly calibrated: raw {raw_seconds/60:.1f} min. "
                           f"Needed tempo {factor:.3f} outside 0.85–1.20; revise script.")
    temp=args.output.with_name(args.output.stem+".partial.mp3")
    filt=f"atempo={factor:.7f},highpass=f=65,lowpass=f=15500,loudnorm=I=-19:TP=-2:LRA=9,afade=t=in:st=0:d=1.5"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(joined),
         "-af",filt,"-ar","44100","-ac","1","-c:a","libmp3lame","-b:a","192k",
         "-metadata","album=Personal Genomics Zone / Frontier Agents",
         "-metadata","comment=AI-generated narration",str(temp)])
    dur=seconds(temp)
    if abs(dur-requested)>60:
        raise RuntimeError(f"Final duration {dur/60:.2f} min too far from target")
    run(["ffmpeg","-v","error","-i",str(temp),"-f","null","-"])
    temp.replace(args.output)
    digest=hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(json.dumps({"status":"verified","duration_seconds":round(dur,2),
           "bytes":args.output.stat().st_size,"sha256":digest,
           "output":str(args.output)},indent=2))

if __name__=="__main__":
    main()
