import csv, io, os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .db import init_db, add_record, add_records, get_records, record_counts, add_action, get_actions, replace_recommendations, get_recommendations, set_recommendation_status
from .source_catalog import SOURCE_CATALOG
from .importer import parse_upload
from .seed import seed_if_empty
from .analysis import dashboard, pl_analysis, recommendations

ROOT=Path(__file__).resolve().parents[1]
FRONTEND=ROOT/'frontend'

app=FastAPI(title='STEPS Performance Intelligence OS API', version='1.0.0')

@app.on_event('startup')
def startup():
    init_db(); seed_if_empty(); refresh_recommendations()

def refresh_recommendations(property_name='Harbour Crest Resort'):
    replace_recommendations(property_name, recommendations(property_name))

class ManualPayload(BaseModel):
    property_name: str='Harbour Crest Resort'
    period: str|None=None
    data: dict

class ActionPayload(BaseModel):
    property_name: str='Harbour Crest Resort'
    title: str
    domain: str|None=None
    owner: str|None=None
    priority: str='Medium'
    due_date: str|None=None
    target: str|None=None
    guardrail: str|None=None
    status: str='Open'

@app.get('/api/health')
def health(): return {'ok':True,'service':'STEPS Performance Intelligence OS'}

@app.get('/api/catalog')
def catalog(): return SOURCE_CATALOG

@app.get('/api/source-status')
def source_status(property_name:str='Harbour Crest Resort'):
    counts=record_counts(property_name)
    return {k:{**v, **counts.get(k,{'count':0,'last_update':None})} for k,v in SOURCE_CATALOG.items()}

@app.get('/api/source/{source_key}')
def source_records(source_key:str, property_name:str='Harbour Crest Resort', limit:int=200):
    if source_key not in SOURCE_CATALOG: raise HTTPException(404,'Unknown source')
    rows=get_records(source_key,property_name,limit)
    return {'source':SOURCE_CATALOG[source_key],'records':[r['payload'] for r in rows]}

@app.post('/api/source/{source_key}/manual')
def source_manual(source_key:str, payload:ManualPayload):
    if source_key not in SOURCE_CATALOG: raise HTTPException(404,'Unknown source')
    allowed=set(SOURCE_CATALOG[source_key]['fields'])
    clean={k:v for k,v in payload.data.items() if k in allowed and v not in (None,'')}
    rid=add_record(payload.property_name,source_key,clean,payload.period,'Manual entry')
    refresh_recommendations(payload.property_name)
    return {'ok':True,'id':rid,'saved':clean}

@app.post('/api/source/{source_key}/upload')
async def source_upload(source_key:str, property_name:str=Form('Harbour Crest Resort'), period:str=Form(''), file:UploadFile=File(...)):
    if source_key not in SOURCE_CATALOG: raise HTTPException(404,'Unknown source')
    data=await file.read()
    try: rows,mapping,unmapped=parse_upload(file.filename or 'upload.csv',data,source_key)
    except Exception as e: raise HTTPException(400,str(e))
    if not rows: raise HTTPException(400,'No usable rows found after mapping.')
    count=add_records(property_name,source_key,rows,period or None,file.filename)
    refresh_recommendations(property_name)
    return {'ok':True,'rows_imported':count,'mapping':mapping,'unmapped':unmapped}

@app.get('/api/dashboard')
def get_dashboard(property_name:str='Harbour Crest Resort'):
    return dashboard(property_name)

@app.get('/api/pl')
def get_pl(property_name:str='Harbour Crest Resort'):
    return pl_analysis(property_name)

@app.get('/api/recommendations')
def get_recs(property_name:str='Harbour Crest Resort'):
    return get_recommendations(property_name)

@app.post('/api/recommendations/{rec_id}/{status}')
def rec_status(rec_id:int,status:str):
    if status not in ('Approved','Rejected','Draft'): raise HTTPException(400,'Invalid status')
    set_recommendation_status(rec_id,status); return {'ok':True}

@app.get('/api/actions')
def actions(property_name:str='Harbour Crest Resort'): return get_actions(property_name)

@app.post('/api/actions')
def create_action(payload:ActionPayload):
    aid=add_action(payload.model_dump()); return {'ok':True,'id':aid}

@app.get('/api/export/owner-brief.csv')
def export_owner_brief(property_name:str='Harbour Crest Resort'):
    d=dashboard(property_name); recs=get_recommendations(property_name)
    out=io.StringIO(); w=csv.writer(out)
    w.writerow(['STEPS Owner Performance Brief',property_name]); w.writerow([])
    w.writerow(['Domain','Metric','Value'])
    for domain,metrics in d['domains'].items():
        for k,v in metrics.items(): w.writerow([domain,k,v])
    w.writerow([]); w.writerow(['Priority Recommendations'])
    w.writerow(['Domain','Title','Impact','Confidence','Status'])
    for r in recs: w.writerow([r['domain'],r['title'],r['impact'],r['confidence'],r['status']])
    data=out.getvalue().encode('utf-8-sig')
    return StreamingResponse(io.BytesIO(data),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=STEPS_Owner_Performance_Brief.csv'})

@app.get('/')
def root(): return FileResponse(FRONTEND/'index.html')

app.mount('/', StaticFiles(directory=FRONTEND, html=True), name='frontend')
