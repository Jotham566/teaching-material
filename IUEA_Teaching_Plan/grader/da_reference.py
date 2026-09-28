"""Lecturer-only reference implementations for the independent S09 checkpoint."""
from datetime import datetime
from collections import defaultdict

def normalise_orders(rows,customer_aliases):
    result=[]
    for source in rows:
        row=dict(source)
        for name in ('order_id','rep_id'):row[name]=int(row[name])
        raw=row['customer_id'];cid=None if raw in ('',None) else int(raw)
        row['customer_id']=customer_aliases.get(str(cid),customer_aliases.get(cid,cid)) if cid is not None else None
        text=str(row['order_date']);row['order_date']=datetime.strptime(text,'%d/%m/%Y' if '/' in text else '%Y-%m-%d').date().isoformat()
        result.append(row)
    return result

def clean_line_items(rows,products,usd_ugx):
    categories={int(r['product_id']):r['category'] for r in products};seen=set();sales=[];returns=[];duplicates=0
    for source in rows:
        identity=tuple(sorted(source.items()))
        if identity in seen:duplicates+=1;continue
        seen.add(identity);r=dict(source);quantity=int(r['quantity']);line=int(r['line_no'])
        if quantity<0:returns.append(dict(line_no=line,quantity_returned=-quantity));continue
        product=int(r['product_id']);price=float(r['unit_price'])
        if categories[product]=='Imported appliances':price*=usd_ugx
        discount=float(r['discount']);discount=discount/100 if discount>1 else discount
        sales.append(dict(order_id=int(r['order_id']),line_no=line,product_id=product,quantity=quantity,unit_price_ugx=price,discount=discount))
    return dict(sales=sales,returns=returns,duplicates_removed=duplicates)

def rep_month_report(orders,sales,returns,reps,year):
    orders={int(r['order_id']):r for r in orders};reps={int(r['rep_id']):r for r in reps};returned=defaultdict(float);totals=defaultdict(lambda:[0.,0.])
    for r in returns:returned[int(r['line_no'])]+=float(r['quantity_returned'])
    for line in sales:
        order=orders[int(line['order_id'])]
        if order['status']!='Delivered' or str(order['order_date'])[:4]!=str(year):continue
        rep=reps[int(order['rep_id'])];key=(rep['region'],rep['rep_name'],str(order['order_date'])[:7]);price=float(line['unit_price_ugx'])*(1-float(line['discount']))
        totals[key][0]+=float(line['quantity'])*price;totals[key][1]+=returned[int(line['line_no'])]*price
    return [list(key)+[gross,back,gross-back] for key,(gross,back) in sorted(totals.items())]
