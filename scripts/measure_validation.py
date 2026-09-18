"""Measure original and reference validation in clean temporary fixture copies."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'tasks/task-004'
PROBE = r'''
import { performance } from 'node:perf_hooks';
import { validate } from './dist/src/validator.js';
const payloads = Array.from({length:1000},(_,i)=>JSON.stringify({id:String(i),title:'',body:'synthetic'}));
const samples=[];let output;
for(let i=0;i<17;i++){const start=performance.now();output=validate(payloads);samples.push(performance.now()-start);}
const original=JSON.parse;let parseCalls=0;
JSON.parse=(...args)=>{parseCalls++;return original(...args)};
try{output=validate(payloads);}finally{JSON.parse=original;}
samples.sort((a,b)=>a-b);
console.log(JSON.stringify({payload_count:payloads.length,actual_parse_calls:parseCalls,reported_parse_passes:output.parsePasses,valid_count:output.values.length,error_count:output.errors.length,median_ms:samples[8],node:process.version,platform:process.platform,arch:process.arch}));
'''
results = {}
for label in ('baseline', 'reference'):
    with tempfile.TemporaryDirectory(prefix='validation-measure-') as temporary:
        workspace = Path(temporary) / 'workspace'
        shutil.copytree(TASK / 'baseline/workspace', workspace)
        if label == 'reference':
            subprocess.run(['git', 'apply', str(TASK / 'golden/solution.patch')], cwd=workspace, check=True)
        subprocess.run(['bash', 'scripts/build.sh', str(ROOT / 'node_modules/.bin/tsc'), str(ROOT)], cwd=workspace, check=True)
        result = subprocess.check_output(['node', '--input-type=module', '-e', PROBE], cwd=workspace, text=True)
        results[label] = json.loads(result)
if results['baseline']['actual_parse_calls'] != 3000 or results['reference']['actual_parse_calls'] != 1000:
    raise SystemExit('Unexpected measured parse counts')
if any(results[label]['valid_count'] != 1000 or results[label]['error_count'] != 0 for label in results):
    raise SystemExit('Benchmark changed valid output behavior')
report={'measured_at':datetime.now(timezone.utc).isoformat(),'starting_commit':'d0f1cea344df7858fb8393f9df6672dd7e98e4d5','command':'python3 scripts/measure_validation.py','classification':'synthetic fixtures; actual local execution','warmup_and_samples':'17 sequential samples; median; no cross-machine speed claim','results':results}
(ROOT / 'reports/measured-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
