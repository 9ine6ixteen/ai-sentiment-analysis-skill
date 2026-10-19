import argparse,json,sys
from pathlib import Path

def read_jsonl(path):
    rows=[]
    for line_no,line in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(),1):
        if line.strip():
            obj=json.loads(line)
            if not isinstance(obj,dict):raise ValueError(f'{path}:{line_no}: object required')
            rows.append(obj)
    return rows

def validate(inputs,results,labels):
    errors=[];source={};seen=set()
    for row in inputs:
        key=row.get('record_id')
        if not isinstance(key,str) or not key or key in source:
            errors.append('invalid or duplicate input ID');continue
        if not isinstance(row.get('comment_text'),str):errors.append(f'{key}: missing comment_text')
        source[key]=row
    for row in results:
        key=row.get('record_id')
        if not isinstance(key,str) or key not in source:
            errors.append(f'{key}: unknown output ID');continue
        if key in seen:errors.append(f'{key}: duplicate output ID')
        seen.add(key);text=source[key].get('comment_text','')
        if row.get('sentiment') not in labels:errors.append(f'{key}: invalid label')
        if not isinstance(row.get('reason'),str) or not row['reason'].strip():errors.append(f'{key}: missing reason')
        if not isinstance(row.get('review_flag'),bool):errors.append(f'{key}: review_flag must be boolean')
        evidence=row.get('evidence')
        if not isinstance(evidence,list) or any(not isinstance(q,str) or not q or q not in text for q in evidence):
            errors.append(f'{key}: evidence must be exact nonempty comment substrings')
        elif not evidence and (row.get('sentiment')!='无法判断' or row.get('review_flag') is not True):
            errors.append(f'{key}: no evidence requires uncodable label and review')
        if row.get('sentiment')=='无法判断' and row.get('review_flag') is not True:
            errors.append(f'{key}: uncodable requires review')
        aspects=row.get('aspects',[])
        if not isinstance(aspects,list):errors.append(f'{key}: aspects must be a list');continue
        for a in aspects:
            if not isinstance(a,dict):errors.append(f'{key}: aspect must be an object');continue
            if any(not isinstance(a.get(k),str) or not a[k].strip() for k in ['target','aspect']):errors.append(f'{key}: aspect target and name required')
            if a.get('sentiment') not in labels:errors.append(f'{key}: invalid aspect sentiment')
            quotes=a.get('evidence')
            if not isinstance(quotes,list) or not quotes or any(not isinstance(q,str) or not q or q not in text for q in quotes):errors.append(f'{key}: invalid aspect evidence')
    errors.extend(f'{key}: missing output' for key in sorted(set(source)-seen))
    return {'input_records':len(inputs),'output_records':len(results),'structural_valid':not errors,'errors':errors,'scope':'Checks format, identifiers and quote presence only; does not verify semantic correctness.'}

def validate_configured(inputs,results,config):
    from check_config import validate_config
    errors=validate_config(config)
    if config.get('mode')!='code_and_analyze':errors.append('Reviewed-label mode skips AI coding validation; preserve reviewed labels')
    source={};seen=set();labels=config.get('labels',[])
    for row in inputs:
        key=row.get('record_id')
        if not isinstance(key,str) or not key or key in source:errors.append('invalid or duplicate input ID');continue
        if not isinstance(row.get('comment_text'),str):errors.append(f'{key}: missing comment_text')
        source[key]=row
    for row in results:
        key=row.get('record_id')
        if not isinstance(key,str) or key not in source:errors.append(f'{key}: unknown output ID');continue
        if key in seen:errors.append(f'{key}: duplicate output ID')
        seen.add(key);rel=row.get('relevance');status=row.get('coding_status');sentiment=row.get('sentiment')
        if rel not in ['relevant','off_target','uncertain']:errors.append(f'{key}: invalid relevance')
        if status not in ['coded','needs_review','not_applicable']:errors.append(f'{key}: invalid coding_status')
        if not isinstance(row.get('target'),str):errors.append(f'{key}: target must be a string')
        if not isinstance(row.get('reason'),str) or not row['reason'].strip():errors.append(f'{key}: missing reason')
        if not isinstance(row.get('review_flag'),bool):errors.append(f'{key}: review_flag must be boolean')
        evidence=row.get('evidence');text=source[key].get('comment_text','')
        if not isinstance(evidence,list) or any(not isinstance(q,str) or not q or q not in text for q in evidence):errors.append(f'{key}: invalid exact comment evidence')
        if status=='coded':
            if rel!='relevant' or sentiment not in labels or not row.get('target') or not evidence:errors.append(f'{key}: coded requires relevant target, configured label and evidence')
        elif sentiment is not None:errors.append(f'{key}: non-coded sentiment must be null')
        if rel=='off_target' and status!='not_applicable':errors.append(f'{key}: off_target must be not_applicable')
        if status=='not_applicable' and rel!='off_target':errors.append(f'{key}: not_applicable requires off_target')
        if rel=='uncertain' and status!='needs_review':errors.append(f'{key}: uncertain relevance requires review')
        if status=='needs_review' and row.get('review_flag') is not True:errors.append(f'{key}: needs_review requires review_flag')
        if row.get('aspects'):errors.append(f'{key}: aspect validation is not implemented in this configured mode')
    errors.extend(f'{key}: missing output' for key in sorted(set(source)-seen))
    return {'input_records':len(inputs),'output_records':len(results),'structural_valid':not errors,'errors':errors,'scope':'Configured relevance/status/polarity and quote checks only; not semantic accuracy.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('inputs');p.add_argument('results');p.add_argument('--config');p.add_argument('--labels',nargs='+',default=['正面','中性','负面','混合','无法判断']);a=p.parse_args()
    try:
        inputs=read_jsonl(a.inputs);results=read_jsonl(a.results)
        report=validate_configured(inputs,results,json.loads(Path(a.config).read_text(encoding='utf-8-sig'))) if a.config else validate(inputs,results,a.labels)
    except (OSError,ValueError) as e:
        print(json.dumps({'structural_valid':False,'errors':[str(e)]},ensure_ascii=False));return 2
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if report['structural_valid'] else 1

if __name__=='__main__':sys.exit(main())
