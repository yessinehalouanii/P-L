from collections import defaultdict
from .db import get_records


def _payloads(source, property_name):
    return [r['payload'] for r in get_records(source, property_name)]

def _num(v, default=0.0):
    try:
        if v is None or v == '': return default
        if isinstance(v, str):
            v = v.replace('$','').replace(',','').replace('%','').strip()
        return float(v)
    except Exception:
        return default

def _sum(rows, field):
    return sum(_num(r.get(field)) for r in rows)

def pl_analysis(property_name="Harbour Crest Resort"):
    rows = _payloads('pl', property_name)
    lines=[]
    operating_revenue=budget_revenue=prior_revenue=0
    departmental_expenses=budget_departmental=0
    undistributed_expenses=budget_undistributed=0
    management_fees=budget_management=0
    nonop_expenses=budget_nonop_expenses=0
    nonop_income=budget_nonop_income=0
    dept = defaultdict(lambda: {'revenue':0,'expense':0,'budget_revenue':0,'budget_expense':0})
    for r in rows:
        actual=_num(r.get('actual')); budget=_num(r.get('budget')); prior=_num(r.get('prior_year'))
        category=str(r.get('category','')).lower(); department=r.get('department') or 'Unassigned'; section=str(r.get('section','')).lower()
        is_expense=category in ('expense','cost')
        if not is_expense:
            if 'non-operating' in section or 'non operating' in section:
                nonop_income += actual; budget_nonop_income += budget
            else:
                operating_revenue += actual; budget_revenue += budget; prior_revenue += prior
                if 'operated' in section or department.lower() in ('rooms','f&b','food & beverage','food and beverage','other operated'):
                    dept[department]['revenue'] += actual; dept[department]['budget_revenue'] += budget
        else:
            if 'management' in section:
                management_fees += actual; budget_management += budget
            elif 'non-operating' in section or 'non operating' in section:
                nonop_expenses += actual; budget_nonop_expenses += budget
            elif 'undistributed' in section:
                undistributed_expenses += actual; budget_undistributed += budget
            else:
                departmental_expenses += actual; budget_departmental += budget
                dept[department]['expense'] += actual; dept[department]['budget_expense'] += budget
        lines.append({**r, 'variance': actual-budget, 'variance_pct': ((actual-budget)/budget*100 if budget else None), 'prior_variance': actual-prior})
    departmental_profit=operating_revenue-departmental_expenses
    budget_departmental_profit=budget_revenue-budget_departmental
    gop=departmental_profit-undistributed_expenses
    gop_budget=budget_departmental_profit-budget_undistributed
    income_before_nonop=gop-management_fees
    income_before_nonop_budget=gop_budget-budget_management
    ebitda=income_before_nonop+nonop_income-nonop_expenses
    ebitda_budget=income_before_nonop_budget+budget_nonop_income-budget_nonop_expenses
    dept_rows=[]
    for name,d in dept.items():
        if d['revenue']==0 and d['expense']==0: continue
        profit=d['revenue']-d['expense']
        margin=(profit/d['revenue']*100) if d['revenue'] else None
        dept_rows.append({'department':name,'revenue':d['revenue'],'expense':d['expense'],'profit':profit,'margin':margin,'budget_profit':d['budget_revenue']-d['budget_expense']})
    dept_rows.sort(key=lambda x:x['revenue'], reverse=True)
    return {
        'lines': lines,
        'summary': {
            'revenue': operating_revenue,'budget_revenue':budget_revenue,'prior_revenue':prior_revenue,
            'departmental_expenses':departmental_expenses,'budget_departmental_expenses':budget_departmental,
            'departmental_profit':departmental_profit,'budget_departmental_profit':budget_departmental_profit,
            'undistributed_expenses':undistributed_expenses,'budget_undistributed_expenses':budget_undistributed,
            'gop':gop,'gop_budget':gop_budget,'gop_variance':gop-gop_budget,
            'gop_margin': (gop/operating_revenue*100 if operating_revenue else 0),
            'management_fees':management_fees,'nonop_expenses':nonop_expenses,'nonop_income':nonop_income,
            'income_before_nonop':income_before_nonop,
            'ebitda':ebitda,'ebitda_budget':ebitda_budget,'ebitda_variance':ebitda-ebitda_budget,
            'ebitda_margin':(ebitda/operating_revenue*100 if operating_revenue else 0),
            'operating_expenses':departmental_expenses+undistributed_expenses,
            'expense_ratio': ((departmental_expenses+undistributed_expenses)/operating_revenue*100 if operating_revenue else 0)
        },
        'departments': dept_rows
    }

def dashboard(property_name="Harbour Crest Resort"):
    pl = pl_analysis(property_name)
    pms=_payloads('pms',property_name); payroll=_payloads('payroll',property_name); pos=_payloads('pos',property_name)
    guest=_payloads('guest',property_name); hr=_payloads('hr',property_name); cmms=_payloads('cmms',property_name)
    utility=_payloads('utility',property_name); web=_payloads('web',property_name); strr=_payloads('str',property_name); rms=_payloads('rms',property_name)
    consultant=_payloads('consultant',property_name); crm=_payloads('crm',property_name)

    available=_sum(pms,'available_rooms'); sold=_sum(pms,'rooms_sold') or _sum(pms,'occupied_rooms'); room_rev=_sum(pms,'room_revenue')
    occ=(sold/available*100) if available else 0
    adr=(room_rev/sold) if sold else 0
    revpar=(room_rev/available) if available else 0

    labour_cost=_sum(payroll,'total_labour_cost'); labour_hours=_sum(payroll,'actual_hours'); ot_hours=_sum(payroll,'overtime_hours')
    budget_labour=_sum(payroll,'budget_labour_cost'); labour_pct=(labour_cost/pl['summary']['revenue']*100) if pl['summary']['revenue'] else 0
    hrs_per_occ=(labour_hours/sold) if sold else 0

    fb_sales=_sum(pos,'net_sales') or _sum(pos,'item_sales'); covers=_sum(pos,'covers'); item_cost=_sum(pos,'item_cost')
    avg_cheque=(fb_sales/covers) if covers else 0; food_cost=(item_cost/fb_sales*100) if fb_sales else 0

    ratings=[_num(x.get('rating')) for x in guest if _num(x.get('rating'))>0]
    sat=[_num(x.get('overall_satisfaction')) for x in guest if _num(x.get('overall_satisfaction'))>0]
    nps=[_num(x.get('nps')) for x in guest if x.get('nps') not in (None,'')]
    guest_rating=sum(ratings)/len(ratings) if ratings else 0
    guest_sat=sum(sat)/len(sat) if sat else 0
    guest_nps=sum(nps)/len(nps) if nps else 0

    active=sum(1 for x in hr if str(x.get('status','')).lower()=='active'); terminated=sum(1 for x in hr if x.get('termination_date'))
    turnover=(terminated/(active+terminated)*100) if active+terminated else 0
    training=[_num(x.get('training_completion_pct')) for x in hr if x.get('training_completion_pct') not in (None,'')]
    training_pct=sum(training)/len(training) if training else 0

    reactive=sum(1 for x in cmms if str(x.get('type','')).lower()=='reactive'); preventive=sum(1 for x in cmms if str(x.get('type','')).lower()=='preventive')
    pm_pct=(preventive/(preventive+reactive)*100) if preventive+reactive else 0
    downtime=_sum(cmms,'downtime_hours')

    util_cost=sum(_sum(utility,f) for f in ['electricity_cost','gas_cost','water_cost','waste_cost'])
    direct_bookings=_sum(web,'direct_bookings'); completed=_sum(web,'completed_bookings'); direct_pct=(direct_bookings/completed*100) if completed else 0
    web_sessions=_sum(web,'sessions'); web_conv=(completed/web_sessions*100) if web_sessions else 0
    pipe=_sum(crm,'total_opportunity')

    latest_str=strr[0] if strr else {}; latest_rms=rms[0] if rms else {}
    mystery_scores=[_num(x.get('score')) for x in consultant if _num(x.get('score'))>0]
    mystery=sum(mystery_scores)/len(mystery_scores) if mystery_scores else 0

    domains = {
        'revenue': {'Occupancy':occ,'ADR':adr,'RevPAR':revpar,'ARI':_num(latest_str.get('ari')),'RGI':_num(latest_str.get('rgi')),'Forecast occupancy':_num(latest_rms.get('forecast_occupancy'))},
        'profit': {'Revenue':pl['summary']['revenue'],'GOP':pl['summary']['gop'],'GOP margin':pl['summary']['gop_margin'],'EBITDA':pl['summary']['ebitda'],'EBITDA margin':pl['summary']['ebitda_margin'],'GOP variance':pl['summary']['gop_variance']},
        'labour': {'Labour cost':labour_cost,'Labour % revenue':labour_pct,'Hours / occupied room':hrs_per_occ,'Overtime hours':ot_hours,'Payroll variance':labour_cost-budget_labour},
        'guest': {'Online rating':guest_rating,'Guest satisfaction':guest_sat,'NPS':guest_nps,'Mystery shop score':mystery},
        'employee': {'Active headcount':active,'Turnover':turnover,'Training completion':training_pct},
        'operations': {'F&B revenue':fb_sales,'Covers':covers,'Average cheque':avg_cheque,'Food cost %':food_cost,'Preventive maintenance %':pm_pct},
        'asset': {'Maintenance downtime':downtime,'Utility cost':util_cost,'Reactive work orders':reactive},
        'sales': {'Direct booking %':direct_pct,'Website conversion %':web_conv,'Pipeline value':pipe}
    }
    return {'property':property_name,'domains':domains,'pl':pl,'source_counts':{k:len(_payloads(k,property_name)) for k in ['pl','pms','rms','str','pos','payroll','hr','guest','cmms','utility','crm','web','consultant']}}

def recommendations(property_name="Harbour Crest Resort"):
    d=dashboard(property_name); pl=d['pl']; out=[]
    # Labour
    lab=d['domains']['labour']; guest=d['domains']['guest']
    if lab['Hours / occupied room'] > 1.65 or lab['Payroll variance'] > 0:
        out.append({'domain':'Labour','title':'Labour deployment is running above demand','evidence':[f"Hours/occupied room: {lab['Hours / occupied room']:.2f}",f"Payroll variance: ${lab['Payroll variance']:,.0f}",f"Guest satisfaction: {guest['Guest satisfaction']:.1f}"], 'recommendation':'Rebuild departmental schedules from forecast demand and service guardrails. Flex start times before reducing total coverage.', 'impact':'Recover controllable labour while protecting service', 'confidence':92})
    # F&B
    ops=d['domains']['operations']
    fbdept=next((x for x in pl['departments'] if x['department'].lower() in ('f&b','food & beverage','food and beverage')),None)
    if (fbdept and fbdept.get('margin') is not None and fbdept['margin'] < 25) or ops['Food cost %'] > 34:
        out.append({'domain':'F&B','title':'F&B profit conversion is under pressure','evidence':[f"Food cost: {ops['Food cost %']:.1f}%",f"Average cheque: ${ops['Average cheque']:.2f}",f"F&B margin: {fbdept['margin']:.1f}%" if fbdept else 'Department margin requires review'], 'recommendation':'Run menu engineering, supplier-cost variance and meal-period staffing review. Separate demand weakness from cost leakage.', 'impact':'Improve departmental margin and average spend', 'confidence':89})
    # Revenue
    rev=d['domains']['revenue']
    if rev['ARI'] and rev['ARI'] < 100 and rev['Occupancy'] > 75:
        out.append({'domain':'Revenue','title':'Strong occupancy is not fully converting into rate','evidence':[f"Occupancy: {rev['Occupancy']:.1f}%",f"ARI: {rev['ARI']:.1f}",f"RevPAR: ${rev['RevPAR']:.2f}"], 'recommendation':'Review high-demand dates, BAR floors and discount leakage. Test firmer pricing where pace supports it.', 'impact':'Capture rate without relying on more room volume', 'confidence':87})
    # Asset
    asset=d['domains']['asset']
    if asset['Reactive work orders'] > 5 or d['domains']['operations']['Preventive maintenance %'] < 50:
        out.append({'domain':'Asset','title':'Maintenance mix is too reactive','evidence':[f"Reactive work orders: {asset['Reactive work orders']}",f"Preventive share: {d['domains']['operations']['Preventive maintenance %']:.1f}%",f"Downtime: {asset['Maintenance downtime']:.1f}h"], 'recommendation':'Prioritize repeat-failure assets, clear overdue PM and move high-cost recurring failures into the capital plan.', 'impact':'Protect asset value and reduce emergency repair cost', 'confidence':84})
    # Guest / arrival
    if guest['Guest satisfaction'] and guest['Guest satisfaction'] < 85:
        out.append({'domain':'Guest','title':'Guest experience needs targeted service recovery','evidence':[f"Guest satisfaction: {guest['Guest satisfaction']:.1f}",f"Online rating: {guest['Online rating']:.2f}/5",f"NPS: {guest['NPS']:.0f}"], 'recommendation':'Use complaint themes and mystery-shop evidence to isolate service breakdowns before changing staffing or standards.', 'impact':'Improve loyalty and service consistency', 'confidence':82})
    # Sales
    sales=d['domains']['sales']
    if sales['Direct booking %'] and sales['Direct booking %'] < 40:
        out.append({'domain':'Sales','title':'Direct-booking contribution can be strengthened','evidence':[f"Direct booking: {sales['Direct booking %']:.1f}%",f"Website conversion: {sales['Website conversion %']:.2f}%",f"Pipeline: ${sales['Pipeline value']:,.0f}"], 'recommendation':'Review booking-engine conversion, paid acquisition and channel economics before adding more OTA volume.', 'impact':'Reduce acquisition cost and improve net revenue', 'confidence':80})
    return out
