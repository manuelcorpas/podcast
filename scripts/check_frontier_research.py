#!/usr/bin/env python3
"""Fail-closed, reproducible minimum research-quality gate for Frontier Agents.

Usage:
  python3 scripts/check_frontier_research.py episodes/YYYY-MM-DD-frontier-agents-NN
Checks traceability/consistency; it does NOT independently establish scientific truth.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import urllib.parse

def validate(folder):
    failures=[]
    def require(ok,message):
        if not ok: failures.append(message)
    script=folder/'transcript.txt'
    notes=folder/'show-notes.md'
    ledger=folder/'evidence-ledger.json'
    review=folder/'research-review.md'
    for f in (script,notes,ledger,review):
        require(f.is_file(),f'missing: {f.name}')
    if failures: return failures
    transcript=script.read_text(encoding='utf-8')
    show=notes.read_text(encoding='utf-8')
    review=review.read_text(encoding='utf-8')
    data=json.loads(ledger.read_text(encoding='utf-8'))
    claims=data.get('claims',[])
    require(len(claims)>=10,'at least ten major technical/empirical claims must be audited')
    require('AI-generated' in show or 'AI-generated' in transcript,'AI voice disclosure required')
    require('limitations' in review.lower(),'limitations section required')
    require('adversarial' in review.lower(),'adversarial reviewer checklist required')
    require('reproducibility' in review.lower(),'reproducibility checklist required')
    require(data.get('reviewed_on'),'research review date required')
    require(data.get('literature_cutoff'),'literature cutoff required')
    require(data.get('scope'),'scope declaration required')
    require(data.get('release_readiness') in ['pass','fail'],'release readiness must be pass/fail')
    require(data.get('release_readiness')=='pass','release readiness is not pass')
    sources=data.get('sources',{})
    require(len(sources)>=5,'at least five inspected source records required')
    domains=set()
    for name,src in sources.items():
        url=src.get('url','')
        parsed=urllib.parse.urlparse(url)
        require(parsed.scheme=='https' and bool(parsed.netloc),f'source {name}: invalid HTTPS URL')
        domains.add(parsed.netloc.lower())
        require(src.get('date'),f'source {name}: missing publication/update date')
        require(src.get('evidence_type') in ('primary research','official technical documentation','peer-reviewed research','primary preprint'),f'source {name}: classify source type')
        require(src.get('specific_finding'),f'source {name}: missing specifically supported finding')
        require(src.get('limitations'),f'source {name}: missing limitations')
    require(len(domains)>=3,'at least 3 institutional/source domains required to reduce single-source dependence')
    ids=set()
    for claim in claims:
        cid=claim.get('id','missing-id')
        require(cid not in ids,f'duplicate claim ID: {cid}')
        ids.add(cid)
        excerpt=claim.get('excerpt','')
        require(len(excerpt)>=18 and excerpt in transcript,f'{cid}: exact excerpt missing from audio transcript')
        require(claim.get('type') in ('empirical','technical','interpretation','methodological','hypothesis'),f'{cid}: classify claim')
        require(claim.get('assessment') in ('verified-in-source','qualified','illustrative','proposed-not-tested'),f'{cid}: invalid assessment')
        require(len(claim.get('limitations',''))>=25,f'{cid}: must describe meaningful qualification/limitation')
        links=claim.get('sources',[])
        require(bool(links),f'{cid}: at least one source required')
        for source_id in links:
            require(source_id in sources,f'{cid}: unknown source ID {source_id}')
        if claim.get('type')=='empirical':
            require(claim.get('assessment')!='proposed-not-tested',f'{cid}: empirical claim cannot be untested')
    # Regression: a known post-February contradiction must not be omitted again.
    if 'SWE-bench Verified' in transcript:
        require('SWE-bench Pro' in transcript and 'July twenty twenty-six' in transcript,
                'SWE-bench benchmark timeline must include the July 2026 correction')
        require('OPENAI_JUL2026' in sources,'OpenAI July 2026 correction source is missing')
    return failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('episode',type=Path)
    args=ap.parse_args()
    failures=validate(args.episode)
    if failures:
        for f in failures: print('FAIL:',f)
        sys.exit(1)
    print('RESEARCH GATE PASS:',args.episode)

if __name__=='__main__': main()
