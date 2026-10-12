#!/usr/bin/env python3
"""LOCAL-ONLY read-only learning context from AGENTIC-AI activity; never publish output."""
import argparse,datetime,subprocess,os,re
from pathlib import Path
ROOT=Path.home()/"dev/AGENTIC-AI"
SELECTED=["00-CORE-MEMORY/STRATEGY/SOUL.md","00-CORE-MEMORY/CONTEXT/CURRENT-STATE.md","00-CORE-MEMORY/CONTEXT/PERSONAL-AGI-PROOF.md","SOUL.md"]
AREAS={
"agent evaluation":["eval","benchmark","test","judge","trace","audit"],
"context and memory":["gbrain","memory","retrieval","search","oauth","context","compaction"],
"agent orchestration":["agent","skill","handoff","codex","roboterri","tool"],
"failure recovery":["restore","failure","recovery","retry","service","error","fix"],
"measured leverage":["attention","proof","measurement","time","cost","leverage"]
}
def recent(repo,n=45):
 r=subprocess.run(["git","-C",str(repo),"log",f"-{n}","--pretty=format:%as %s"],capture_output=True,text=True)
 return r.stdout.splitlines() if r.returncode==0 else []
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--output",type=Path,default=Path.home()/".local/share/frontier-agents/private-learning-context.md")
 p.add_argument("--days",type=int,default=30)
 a=p.parse_args()
 if not ROOT.is_dir(): raise SystemExit("AGENTIC-AI project not found; no inferred context")
 today=datetime.date.today()
 commits=[]
 for repo in [ROOT,Path.home()/"dev/ClawBio",Path.home()/"dev/gbrain"]:
  for s in recent(repo):
   try: date=datetime.date.fromisoformat(s[:10])
   except ValueError: continue
   if 0<=(today-date).days<=a.days: commits.append((repo.name,s))
 lines=["# PRIVATE — Frontier Agents learning context", "",
 f"Date: {today}. Local-source window: {a.days} days.",
 "Never commit, upload or publish this brief verbatim. Its activity counts do not establish improved capability.",
 "", "## Authoritative project files"]
 for x in SELECTED: lines.append("- "+str(ROOT/x)+" ("+("present" if (ROOT/x).is_file() else "missing")+")")
 proof=ROOT/"00-CORE-MEMORY/CONTEXT/PERSONAL-AGI-PROOF.md"
 if proof.is_file():
  lines+=["","## Current proof boundaries"]
  for s in proof.read_text(errors="replace").splitlines():
   if s.startswith("Overall:") or ("|" in s and "not demonstrated" in s) or s.startswith("CLR:"): lines.append(s)
 lines+=["","## Recent engineering activity — commit subjects only"]
 for name,terms in AREAS.items():
  hits=[repo+": "+msg for repo,msg in commits if any(re.search(r"\b"+re.escape(t)+r"\b",msg,re.I) for t in terms)]
  lines.append("### "+name+" ("+str(len(hits))+" commits)")
  lines.extend("- "+x for x in hits[:3])
 lines+=["","## Required curriculum decisions",
 "1. Identify two specific learning-gap hypotheses from project evidence, not assumptions.",
 "2. Teach one general frontier agentic-AI mechanism; personal projects only motivate private selection.",
 "3. Use at least two original external research sources; check contradictions and recency.",
 "4. Design a reproducible independent experiment with public or synthetic data.",
 "5. Track understanding via five active-recall questions and a verifiable coding exercise.",
 "6. Suggest one confidential project improvement after the episode, separately from publishable show notes.",
 "7. Do not expose personal, medical, patient, institutional, credential or unpublished research information.",
 ""]
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text("\n".join(lines),encoding="utf-8")
 os.chmod(a.output,0o600)
 print("PRIVATE_BRIEF",a.output)
 print("RECENT_COMMIT_SUBJECTS",len(commits))
 print("COUNTS",{n:sum(any(re.search(r"\b"+re.escape(t)+r"\b",s,re.I) for t in terms) for _,s in commits) for n,terms in AREAS.items()})
if __name__=="__main__": main()
