"""Trusted unseen-input checks for the independent pandas checkpoint."""
import copy,math,random
from da_reference import normalise_orders,clean_line_items,rep_month_report
TASKS={
 'normalise_orders':('normalise_orders(rows, customer_aliases)',10,'Return copied order dictionaries in the same order. Convert order_id and rep_id to integers; customer_id is an integer or None for a blank walk-in ID. Apply the supplied customer-ID alias map. Parse dates explicitly as ISO YYYY-MM-DD or day/month/year and return ISO dates. Preserve all other fields and the input. Never drop a missing-customer order.'),
 'clean_line_items':('clean_line_items(rows, products, usd_ugx)',10,'Remove exact duplicate raw rows, not every repeated line_no. Separate negative quantities into returns with positive quantity_returned. Convert Imported appliances unit_price to UGX at the supplied rate; other prices are already UGX. Divide discounts above 1 by 100. Return a dictionary with sales (order_id,line_no,product_id,quantity,unit_price_ugx,discount), returns (line_no,quantity_returned), and duplicates_removed. Retain source order within each list; preserve inputs.'),
 'rep_month_report':('rep_month_report(orders, sales, returns, reps, year)',30,'Return one row per delivered-order rep/month for the supplied year. Columns in order: region,rep_name,month,gross_ugx,returned_ugx,net_ugx. Return a list of six-element rows or a pandas DataFrame with those columns. Missing customer IDs must not remove sales. Aggregate multiple return events per line before joining, so gross is counted once. Extra/missing rows fail the contract; each amount allows 1 UGX after rounding.')}

def fixture(seed):
    rng=random.Random(seed);base=seed*100;orders=[];raw=[]
    products=[dict(product_id=1,category='Rice' if seed==41 else 'Imported appliances'),dict(product_id=2,category='Imported appliances' if seed==41 else 'Rice')]
    reps=[dict(rep_id=10,rep_name='Rep A',region='Central'),dict(rep_id=20,rep_name='Rep B',region='Western')]
    for i,(stamp,status,cid) in enumerate([('15/01/2025','Delivered',''),('2025-01-22','Delivered',str(base+99)),('2024-02-03','Delivered',str(base+7)),('2025-03-04','Cancelled',str(base+8))]):
        orders.append(dict(order_id=str(base+i),customer_id=cid,rep_id=str(10 if i%2==0 else 20),order_date=stamp,status=status,channel='Walk-in' if not cid else 'Online'))
        for product in (1,2):raw.append(dict(order_id=str(base+i),line_no=str(base+i*2+product),product_id=str(product),quantity=str(rng.randint(2,9)),unit_price=str(rng.randint(10,50) if product==1 else rng.randint(500,2000)),discount='15' if product==1 else '0.05'))
    raw[0]['quantity']='5'
    back=dict(raw[0],quantity='-1');raw+=[back,dict(raw[0]),dict(back)]
    rng.shuffle(raw)
    return orders,raw,products,reps,{str(base+99):base+7}

def equivalent(actual,expected):
    if isinstance(expected,dict):return isinstance(actual,dict) and actual.keys()==expected.keys() and all(equivalent(actual[k],v) for k,v in expected.items())
    if isinstance(expected,list):return isinstance(actual,list) and len(actual)==len(expected) and all(equivalent(a,e) for a,e in zip(actual,expected))
    if isinstance(expected,(float,int)) and not isinstance(expected,bool):return isinstance(actual,(float,int)) and math.isfinite(actual) and abs(actual-expected)<1e-6
    return actual==expected

def check(ns,task):
    function=ns.get(task)
    if not callable(function):return False,'Implement '+TASKS[task][0]
    try:
        for seed in (19,41,83):
            orders,raw,products,reps,aliases=fixture(seed)
            if task=='normalise_orders':
                args=[orders,aliases];expected=normalise_orders(*copy.deepcopy(args));actual=function(*args)
                if not equivalent(actual,expected):return False,'Check day-first dates, blank walk-in IDs and supplied customer aliases.'
            elif task=='clean_line_items':
                args=[raw,products,{19:3780,41:4000,83:3500}[seed]];expected=clean_line_items(*copy.deepcopy(args));actual=function(*args)
                if not equivalent(actual,expected):return False,'Check exact duplicates, return signs, currency and percentage discounts.'
            else:
                clean=clean_line_items(raw,products,3780);clean_orders=normalise_orders(orders,aliases)
                # Two distinct return events must not multiply gross revenue.
                events=clean['returns']+[dict(clean['returns'][0],quantity_returned=2)]
                args=[clean_orders,clean['sales'],events,reps,2025 if seed!=83 else 2024]
                expected=rep_month_report(*copy.deepcopy(args));actual=function(*args)
                if hasattr(actual,'columns'):
                    if list(actual.columns)!=['region','rep_name','month','gross_ugx','returned_ugx','net_ugx']:return False,'Use the required six output columns.'
                    actual=actual.values.tolist()
                actual=sorted(actual,key=lambda r:tuple(r[:3]))
                if len(actual)!=len(expected):return False,'Check delivered/year filters and rep/month grain.'
                for got,want in zip(actual,expected):
                    if list(got[:3])!=want[:3] or len(got)!=6 or any(not isinstance(a,(int,float)) or not math.isfinite(a) or abs(a-b)>1 for a,b in zip(got[3:],want[3:])):
                        return False,'Reconcile gross, returned and net amounts without join multiplication.'
        return True,'Passed unseen input checks.'
    except Exception as exc:return False,'Interface failed: '+str(exc)[:160]
