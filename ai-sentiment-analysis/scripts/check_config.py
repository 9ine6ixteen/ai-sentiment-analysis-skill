import argparse,json,sys
from pathlib import Path

def validate_config(c):
    errors=[]
    if not isinstance(c,dict):return ['Configuration must be an object']
    if c.get('mode') not in ['code_and_analyze','analyze_reviewed']:errors.append('Unsupported mode')
    labels=c.get('labels')
    if not isinstance(labels,list) or not labels or any(not isinstance(x,str) or not x for x in labels):errors.append('labels must be nonempty strings')
    elif len(set(labels))!=len(labels):errors.append('labels must be unique')
    mapping=c.get('value_map',{})
    if not isinstance(mapping,dict):errors.append('value_map must be an object')
    elif isinstance(labels,list) and any(v not in labels for v in mapping.values()):errors.append('value_map targets must occur in labels')
    columns=c.get('columns',{});required=['id','text']+(['sentiment'] if c.get('mode')=='analyze_reviewed' else [])
    if not isinstance(columns,dict) or any(not isinstance(columns.get(k),str) or not columns[k] for k in required):errors.append('Missing required column mapping')
    if not isinstance(c.get('tasks'),list):errors.append('tasks must be a list')
    if not isinstance(c.get('analysis_confirmed'),bool):errors.append('analysis_confirmed must be boolean')
    if c.get('analysis_confirmed') and not c.get('tasks'):errors.append('Confirmed analysis needs explicit tasks')
    if c.get('analysis_confirmed') and not (isinstance(c.get('source'),dict) and c['source'].get('confirmed') is True):errors.append('Confirmed analysis needs a confirmed source')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('config');a=p.parse_args()
    try:c=json.loads(Path(a.config).read_text(encoding='utf-8-sig'));errors=validate_config(c)
    except (OSError,ValueError) as e:errors=[str(e)]
    print(json.dumps({'valid':not errors,'errors':errors,'scope':'Configuration validation only; no data read or analysis performed.'},ensure_ascii=False,indent=2));return int(bool(errors))

if __name__=='__main__':sys.exit(main())
