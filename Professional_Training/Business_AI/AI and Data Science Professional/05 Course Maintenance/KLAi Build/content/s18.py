"""Session 18: Finding structure without labels (author i). Python lab, notebook in content/labs/s18_nb.py.

Every number on a slide, in a note or in the notebook checks comes from s18_facts.facts(): Lakeside Mart orders.csv (30,229 orders), with RFM, the log transform, scaling, k-means, PCA and an isolation forest
written in NumPy (scikit-learn is not installed in the build sandbox). The slides say so where it matters."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s18_facts as SF  # noqa: E402

NAMES = ['Best customers', 'Drifting regulars', 'Recent regulars', 'Lapsed low spenders']
ACTIONS = ['Protect them: early access to promotions and one named contact.', 'Win them back before they lapse: a reminder offer in the next month.',
           'Grow the basket: promote higher-value products to them.', 'Send a low-cost reactivation message and do not spend heavily.']


def n(x):
    return f'{int(round(x)):,}'


def build():
    F = SF.facts()
    st = F['rfm_stats']
    pr = F['profile']
    inert = F['inertia']
    pca = F['pca']
    rule = F['rule']
    iso = F['iso']
    demo = F['isodemo']
    mv = F['moves']
    rfm = F['rfm_np']
    c1 = F['c1']
    c1o = F['c1_orders']
    # histogram data for the log transform picture
    spend = rfm[:, 2].astype(float)
    cnt_raw, _ = np.histogram(spend, bins=16, range=(0, 3_200_000))
    lg = np.log1p(spend)
    lo_, hi_ = lg.min(), lg.max()
    cnt_log, _ = np.histogram(lg, bins=16, range=(lo_, hi_))
    fr = lambda v: (np.log(v) - lo_) / (hi_ - lo_)
    lapsed = int(sum(1 for r_, s_ in zip(iso['rec'], iso['spend']) if r_ > 100 and s_ < 100000))
    heavy = int(sum(1 for s_ in iso['spend'] if s_ > 800000))
    other = iso['n'] - lapsed - heavy
    sizes_rng = F['k4_size_range']
    spread_max = max(b - a for a, b in sizes_rng)
    walk_pct = F['walkin'] / F['orders'] * 100
    ratio = pca['ratio']
    comps = pca['comps']
    sess = dict(
        num=18, block='Module D: Machine learning', short_title='Finding structure without labels',
        title='Finding structure without labels: customer segments and unusual orders',
        question='How do we group customers, or spot odd cases, when nobody gave us the answers?',
        outcomes=['Build recency, frequency and monetary value (RFM) variables, then apply a log transform and standardisation',
                  'Run k-means clustering, choose k with the elbow method, reduce three variables to two with PCA, and name each segment in business words',
                  'Flag unusual orders and customers with a percentile rule and an isolation forest, and say what to do with them'],
        outcome_icons=['people', 'chart', 'magnifier'],
        outcome_note=('Here is what you can do by the end of today. You can build recency, frequency and monetary value for each customer, and prepare them with a log transform and standardisation. '
                      'You can run k-means clustering, choose the number of groups with the elbow method, squeeze three variables into two with principal component analysis, and give each segment a name a manager can use. '
                      'And you can flag unusual orders and customers with a percentile rule and an isolation forest, and say what to do with them. We use the Lakeside Mart orders for all of it. There is no answer column today.'),
        clock=[(10, 'Recall and the question of the day'), (45, 'Concepts: picture, plain words, one example by hand'), (10, 'Break'), (45, 'Lab: predict, run, read, change'), (10, 'Exit check, keep and next')],
        plan_title='Your two hours: concepts first, then a Python lab',
        plan_caption='Ideas with pictures first. Then you open the notebook. Then the checks and what you keep.',
        plan_note=('We have two hours. The first ten minutes bring back Session 17 and set the question for today. Then forty-five minutes of concepts, with no laptops open, so you can watch the pictures and the worked numbers. '
                   'After a ten minute break we open the notebook for a forty-five minute lab on the Lakeside Mart customers. You will predict each result, run it, read it, and change one thing. '
                   'The last ten minutes are an exit check and what you keep. The lab is where the learning sticks, so please protect that time.'),
        recall_from='Session 17',
        recall=[('A model scores very well on its training rows and much worse on its test rows. What is that called?', 'Overfitting. The distance between the two scores is the generalisation gap.'),
                ('A forest reports a high permutation importance for one variable. What can you safely say?', 'The model relies on that variable. It does not show a cause.'),
                ('Two models score about the same. Which one do you ship, and what is the rule called?', 'The simpler one. The rule is parsimony.')],
        words=[('Unsupervised learning (for example clustering, anomaly detection)', 'Learning with no answer column. The algorithm looks for groups or odd rows by itself.'),
               ('RFM analysis', 'Three numbers per customer: recency (days since the last order), frequency (number of orders) and monetary value (total spend).'),
               ('Feature scaling and log transform', 'Standardisation (z-score) puts variables on one scale. A log transform squeezes a long right tail.'),
               ('k-means clustering', 'Splits records into k clusters around k centroids. Inertia measures how tight they are. The elbow method suggests k.'),
               ('Principal component analysis (PCA)', 'A dimensionality reduction method: it mixes many variables into a few principal components that keep most of the variance.')],
        word_icons=['people', 'receipt', 'calculator', 'chart', 'magnifier'],
        words_note=('Five words for today. Unsupervised learning means learning with no answer column. RFM analysis is recency, frequency and monetary value, three numbers per customer. '
                    'Feature scaling puts variables on one scale, and a log transform squeezes a long tail. K-means clustering splits records into k groups around k centre points, and the elbow method helps you choose k. '
                    'And principal component analysis mixes many variables into a few so you can draw them. We also meet anomaly detection later in the session.'),
        keep='Keep your customer segment table: each of the 2,499 loyalty customers with its RFM numbers, its segment name and one action, saved as a file, plus a list of unusual orders to review.',
        keep_visual=dict(kind='card', title='Take away', fields=[dict(label='Your lab file', value='keep/customer_segments.csv'), dict(label='The names', value='4 segments, 4 actions'), dict(label='Next session', value='Forecasting')]),
        keep_title='Save your notebook and customer_segments.csv',
        next='Session 19: Forecasting and a first end-to-end model. Project milestone 3.', next_label='Next session',
        keep_note=('Before you go, save your notebook and the file customer segments dot csv. That file is your keepsake from today: every loyalty customer with recency, frequency and spend, a segment name and an action. '
                   'If you can show it to a shop manager and they know what to do on Monday, it is good. Next session we forecast the future, build a pipeline that packages a whole modelling job, and reach Project milestone 3. '
                   'If anything was unclear today, write the question down and bring it.'),
        cover_note=('Welcome back. Last session we learned to get a stronger model without fooling ourselves, and we saw that the simple model often wins. '
                    'Today there is no answer column at all. We take the Lakeside Mart orders and ask who our customers are, in groups a manager can describe. We prepare three numbers per customer, let k-means find the groups, name them, and flag unusual orders. '
                    'The test is whether you could take the result into a meeting.'),
        use_at_work='Segment customers with RFM and k-means, name each segment with an action, and flag unusual records for review.',
        slides=[])
    S = sess['slides']

    # ------------------------------------------------------------------ 1 answers
    S.append(dict(kind='table', title='Answers to the three questions from Session 17', headers=['Question', 'Short answer'], rows=[[q, a] for q, a in sess['recall']], widths=[5.2, 6.8], icons=['chart', 'magnifier', 'check'],
                  notes=('Here are the answers to the three warm-up questions. A model that scores very well on its training rows and much worse on its test rows is overfitting, and the distance between the two scores is the generalisation gap. '
                         'A high permutation importance tells you the model relies on that variable. It does not show that the variable causes the outcome. '
                         'And when two models score about the same, you ship the simpler one, which is the rule of parsimony. Today we leave answer columns behind. Which of the three did you find hardest?')))

    # ------------------------------------------------------------------ 2 supervised vs unsupervised
    S.append(dict(kind='compare', title='Supervised learning has an answer column. Unsupervised learning has none',
                  left=dict(head='Sessions 14 to 17: supervised', points=['The loans table has a default column.', 'The model learns to predict it.', 'We score it against the known answer.']),
                  right=dict(head='Today: unsupervised', points=['The orders have no segment column.', 'Nobody told us the groups.', 'We look for structure, then judge it ourselves.']),
                  verdict='No accuracy to chase. Inertia and the silhouette score help. A person judges.',
                  notes=('Everything so far had an answer column. In the loan data each loan said whether it defaulted, so the model could learn from it and we could score it afterwards. That is supervised learning. '
                         'Today the orders have no segment column. Nobody went through the customers and wrote down who is a big spender or who has drifted away. The algorithm must look for structure by itself. That is unsupervised learning, and grouping records is called clustering. '
                         'The consequence matters. With no known answer there is no AUC to chase, so a person has to decide whether the groups make sense for the business. Internal measures such as inertia and the silhouette score help you compare choices of k. Also remember that k-means assumes round clusters of similar size. Where would you want groups of customers at your work?')))

    # ------------------------------------------------------------------ 3 walk-ins
    S.append(dict(kind='stat', title='Walk-in orders have no customer_id, so 30 percent of orders cannot join a customer segment', big=f'{walk_pct:.0f}%',
                  text=f'{n(F["walkin"])} of {n(F["orders"])} orders are walk-ins. We keep the {n(F["loyal_orders"])} loyalty orders, from {n(F["n_cust"])} customers.', waffle_label='orders in every 100 are walk-ins',
                  notes=(f'Our file is the Lakeside Mart orders again, {n(F["orders"])} orders from {F["first"]} to {F["end"]}. To group customers, every order we use must say which customer it belongs to. '
                         f'A walk-in order has a blank customer id, so we cannot follow that person across visits. That is {n(F["walkin"])} orders, about {walk_pct:.0f} in every hundred, and they are left out of the segments. '
                         f'Anyone reading your segments must know that walk-in shoppers are not in them. What remains is {n(F["loyal_orders"])} loyalty orders from {n(F["n_cust"])} customers. The customers file lists {n(F["customers_file"])}, so {F["never_ordered"]} loyalty customer never ordered. '
                         'Why is it honest to say that out loud?')))

    # ------------------------------------------------------------------ 4 RFM
    S.append(dict(kind='wide', title='RFM analysis turns one customer\'s orders into three numbers: recency, frequency and monetary value',
                  visual=dict(kind='ds_i_rfm', customer='C0001', orders=[[a, int(b)] for a, b in c1o[-5:]], total=len(c1o), last_date=c1o[-1][0], end_date=F['end'], r=int(F['rfm_head'][0][1]), f=int(F['rfm_head'][0][2]), m=int(F['rfm_head'][0][3])),
                  caption=f'One record per customer: C0001 made {len(c1o)} orders, the last on {c1o[-1][0]}.',
                  notes=(f'Most customer segments start from three numbers, and the set has a name: RFM analysis. R is recency, the days from the customer\'s last order to the last date in the file. F is frequency, the number of orders. '
                         f'M is monetary value, the total spent. Take customer C0001. The picture shows the last five of {len(c1o)} orders. The last was on {c1o[-1][0]}, which is {F["rfm_head"][0][1]} days before the end of the file on {F["end"]}. '
                         f'The customer made {F["rfm_head"][0][2]} orders and spent {n(F["rfm_head"][0][3])} shillings in total. We use the last date in the file as today, so the numbers stay the same each time you open the notebook. '
                         'In Excel this is a pivot table with the customer on the rows. Which of the three would a shop manager care about most?')))

    # ------------------------------------------------------------------ 5 RFM table
    S.append(dict(kind='table', title=f'The RFM table has one record per customer: {n(F["n_cust"])} records and three variables',
                  headers=['Customer', 'Recency (days)', 'Frequency (orders)', 'Monetary value (UGX)'],
                  rows=[[r_[0], str(r_[1]), str(r_[2]), n(r_[3])] for r_ in F['rfm_head']] + [['Mean', f'{st["recency"]["mean"]:.1f}', f'{st["frequency"]["mean"]:.1f}', n(st['spend']['mean'])], ['Median', f'{st["recency"]["median"]:.0f}', f'{st["frequency"]["median"]:.0f}', n(st['spend']['median'])],
                                                                                                    ['Standard deviation', f'{st["recency"]["sd"]:.1f}', f'{st["frequency"]["sd"]:.1f}', n(st['spend']['sd'])]],
                  widths=[3.2, 2.7, 3.0, 3.1], icons=['person', 'person', 'person', 'calculator', 'calculator', 'calculator'], note='Each record is one loyalty customer. The mean spend is above the median: a few large spenders pull it up.',
                  notes=(f'Here is the result in pandas. Each record is one loyalty customer, so there are {n(F["n_cust"])} records and three variables. The first three customers are shown, then the mean, the median and the standard deviation of each variable. '
                         f'Look at monetary value. The mean is {n(st["spend"]["mean"])} shillings but the median is {n(st["spend"]["median"])}. When the mean sits well above the median, a few big spenders are pulling it up. That is a right-skewed variable, with a long right tail. '
                         f'Recency is the same: mean {st["recency"]["mean"]:.1f} days, median {st["recency"]["median"]:.0f}. The three variables are also on very different scales, from a few orders to hundreds of thousands of shillings. Both facts matter for k-means. What do you notice about the standard deviations?')))

    # ------------------------------------------------------------------ 6 log transform
    S.append(dict(kind='wide', title=f'A log transform squeezes the long right tail: the skewness of spend falls from {st["spend"]["skew"]:.2f} to {F["skew_log"]["spend"]:.2f}',
                  visual=dict(kind='ds_i_hist2', panels=[dict(title='Spend per customer', sub=f'skewness {st["spend"]["skew"]:.2f}: a long right tail', counts=cnt_raw.tolist(), xticks=[(0, '0'), (1_000_000 / 3_200_000, '1,000,000'), (2_000_000 / 3_200_000, '2,000,000')], xlabel='spend, UGX'),
                                                           dict(title='Log of spend', sub=f'skewness {F["skew_log"]["spend"]:.2f}: roughly symmetric', counts=cnt_log.tolist(), gold=True, xticks=[(fr(v), f'{v:,}') for v in (10_000, 100_000, 1_000_000)], xlabel='spend, UGX, on a log scale')]),
                  caption=f'Skewness measures lopsidedness. We log all three variables: frequency goes from {st["frequency"]["skew"]:.2f} to {F["skew_log"]["frequency"]:.2f}.',
                  notes=(f'Spend has a long right tail, so a few customers sit far from the rest. The skewness of spend is {st["spend"]["skew"]:.2f}. Skewness measures how lopsided a variable is, and zero means symmetric. '
                         f'A log transform replaces each value by its logarithm. It squeezes big values a lot and small values a little, like a log scale on an Excel chart. After the transform the skewness of spend is {F["skew_log"]["spend"]:.2f}, so the histogram is roughly symmetric. '
                         'We use log of one plus x, called log1p, so a value of zero would not break the logarithm. Recency also has a right tail, and its skewness falls from '
                         f'{st["recency"]["skew"]:.2f} to {F["skew_log"]["recency"]:.2f}. Frequency was only mildly skewed ({st["frequency"]["skew"]:.2f}) and becomes slightly left-skewed ({F["skew_log"]["frequency"]:.2f}). Many analysts log only spend. We log all three for one simple recipe. Why would k-means treat a skewed variable badly?')))

    # ------------------------------------------------------------------ 7 z-score
    S.append(dict(kind='formula', title='Standardisation turns each variable into a z-score: how many standard deviations from the mean',
                  size=24,
                  formulas=[('z-score', r'$z = \frac{x - \bar{x}}{s}$'), ('Customer C0001, spend', rf'$z = \frac{{{c1["logspend"]:.2f} - {F["log_mean"]["spend"]:.2f}}}{{{F["log_sd"]["spend"]:.2f}}} = {c1["z_spend"]:.2f}$')],
                  symbols=[['x', 'The value of one customer: here the log of spend', f'{c1["logspend"]:.2f} for C0001 (spend {n(c1["spend"])} UGX)'], ['x-bar and s', 'The mean and the standard deviation of that variable over all customers', f'{F["log_mean"]["spend"]:.2f} and {F["log_sd"]["spend"]:.2f}'],
                           ['z', 'The z-score: 0 is average, +1 is one standard deviation above', f'{c1["z_spend"]:.2f}: well above average']],
                  widths=[2.3, 5.8, 3.8], note='Computed from unrounded values, so a hand calculation differs by 0.01. In scikit-learn: StandardScaler.',
                  notes=(f'Standardisation, also called the z-score, rewrites each variable so its mean is zero and its standard deviation is one. Subtract the mean, divide by the standard deviation. '
                         f'Take customer C0001. The log of spend is {c1["logspend"]:.2f}. The mean of log spend is {F["log_mean"]["spend"]:.2f} and the standard deviation is {F["log_sd"]["spend"]:.2f}. So the z-score is {c1["z_spend"]:.2f}. '
                         'That customer is one and a half standard deviations above the average spender. Zero means average, and minus one means one standard deviation below. In scikit-learn the tool is StandardScaler. '
                         'Why is a z-score easier to compare across variables than the raw value?')))

    # ------------------------------------------------------------------ 8 why scale
    S.append(dict(kind='table', title='Feature scaling puts recency, frequency and spend on one scale before k-means measures distance',
                  headers=['Variable', 'Standard deviation, raw', 'Standard deviation, logged and scaled'],
                  rows=[['Recency', f'{F["raw_sd"]["recency"]:.1f} days', '1.0'], ['Frequency', f'{F["raw_sd"]["frequency"]:.1f} orders', '1.0'], ['Monetary value', f'{n(F["raw_sd"]["spend"])} UGX', '1.0']],
                  widths=[3.4, 4.2, 4.4], icons=['clock', 'receipt', 'coin'], note='k-means uses distance. Without scaling, spend (in shillings) would decide almost every distance and the other two would count for nothing.',
                  notes=(f'Why scale at all? k-means works with distance between customers. The raw standard deviation of recency is {F["raw_sd"]["recency"]:.1f} days, of frequency {F["raw_sd"]["frequency"]:.1f} orders, and of spend {n(F["raw_sd"]["spend"])} shillings. '
                         'If we feed those to k-means, spend decides almost every distance, because its numbers are thousands of times bigger. Recency and frequency would count for nothing. '
                         'After the log transform and standardisation, every variable has a standard deviation of one, so each gets an equal say. This is called feature scaling. Distance-based methods such as k-means and k-nearest neighbours need it. '
                         'Which other method from this course used distance?')))

    # ------------------------------------------------------------------ 9 four moves
    S.append(dict(kind='steps', title='k-means clustering repeats two moves until the groups stop changing',
                  steps=[dict(head='1 Assign', text='Put each customer in the cluster with the nearest centroid', icon='pin'), dict(head='2 Update', text='Move each centroid to the mean of its cluster', icon='calculator'),
                         dict(head='3 Repeat', text='Assign again with the new centroids', icon='clock'), dict(head='4 Converge', text='Stop when no customer changes cluster', icon='check')], highlight=None,
                  caption='k is the number of clusters you choose. A centroid is the mean point of a cluster. Inertia is the sum of squared distances from each customer to its centroid.',
                  notes=('Here is k-means in four moves. You choose k, the number of clusters, and the algorithm starts with k centre points. Move one, assign: put each customer in the cluster with the nearest centre, which is called a centroid. '
                         'Move two, update: move each centroid to the mean of the customers now in its cluster. Move three, repeat: assign again with the new centroids. Move four, converge: stop when no customer changes cluster. '
                         'The number we track is inertia, the sum of squared distances from each customer to its centroid. It can only fall or stay the same at each step. The following picture shows these moves on ten real customers. Why must the loop end?')))

    # ------------------------------------------------------------------ 10 moves picture
    st_ = mv['steps']
    titles = [('Assign', 'two starting centroids', False), ('Update, assign', 'centroids move', True), ('Repeat', 'centroids move again', True), ('Converge', 'no one changes cluster', True)]
    S.append(dict(kind='wide', title='k-means on ten real customers: the centroids move and the inertia falls until nothing changes',
                  visual=dict(kind='ds_i_moves', points=mv['points'], steps=st_, titles=titles, xlabel='x: scaled log recency. y: scaled log spend. Gold square: centroid. Filled and hollow dots: the two clusters.'),
                  caption=f'k = 2. Inertia falls from {st_[0]["inertia"]:.2f} to {st_[-1]["inertia"]:.2f} in {len(st_) - 1} updates.',
                  notes=(f'Here are the four moves on ten real customers, with two variables and k equal to two. The gold squares are the centroids, and the filled and hollow dots are the two clusters. '
                         f'On the left we start with two centroids and assign each customer to the nearest one. The inertia is {st_[0]["inertia"]:.2f}. Then each centroid moves to the mean of its cluster, and we assign again. The inertia falls to {st_[1]["inertia"]:.2f}, then {st_[2]["inertia"]:.2f}. '
                         f'On the right, after {len(st_) - 1} updates, no customer changes cluster, so the algorithm has converged at {st_[-1]["inertia"]:.2f}. Our real run uses all {n(F["n_cust"])} customers and three variables, and the same two moves. '
                         'Where did the centroids move to?')))

    # ------------------------------------------------------------------ 11 elbow
    S.append(dict(kind='idea', title='The elbow method plots inertia against k and looks for the bend',
                  visual=dict(kind='ds_i_curves', xs=[str(k) for k in SF.K_RANGE], series=[dict(label='Inertia', ys=[inert[k] for k in SF.K_RANGE], kind='red')], xlabel='k: number of clusters', ylabel='inertia',
                              ymin=0, ymax=8000, ticks=[0, 2000, 4000, 6000, 8000], fmt='{:,.0f}', mark=3, mark_label='our choice: k = 4', right=1.7),
                  lead='Inertia always falls as k grows. Look for where the fall slows.',
                  points=[f'k = 3: {n(inert[3])}. k = 4: {n(inert[4])}. k = 5: {n(inert[5])}.', 'The bend is gentle, so 3, 4 or 5 are all defensible.', 'We pick 4: four segments can each be named and acted on.'],
                  notes=(f'How do we choose k? The elbow method plots inertia against k. With k equal to one, the inertia is {n(inert[1])}, which is three variables times {n(F["n_cust"])} customers. It falls as k grows, always. We look for the bend, where extra groups buy little. '
                         f'Here it falls by {n(inert[1] - inert[2])} from one to two, {n(inert[2] - inert[3])} from two to three, about {round((inert[3] - inert[4]) / 10) * 10:,.0f} from three to four, and about {round((inert[4] - inert[5]) / 5) * 5:,.0f} from four to five. The bend is gentle. '
                         'The elbow is a hint, and the final choice is a judgement. We choose four, because we can name four segments and give each a different action. That is a business reason, and we say so. Would you choose three?')))

    # ------------------------------------------------------------------ 12 segments scatter
    S.append(dict(kind='wide', title='Four customer segments on recency and spend: the groups touch, so the edges are soft',
                  visual=dict(kind='ds_i_segments', x=F['scatter']['x'], y=F['scatter']['y'], seg=F['scatter']['seg'], names=NAMES, xticks=[(0, '0'), (float(np.log10(11)), '10'), (float(np.log10(101)), '100')],
                              yticks=[(4, '10,000'), (5, '100,000'), (6, '1,000,000')], xlabel='recency, days since the last order (log scale)', ylabel='spend, UGX (log scale)'),
                  caption=f'One dot per customer ({n(F["n_cust"])}). Colours are k-means segments; your run differs by up to 5 percent.',
                  notes=('Here are all the customers on two of the three variables, recency across and spend up, both on log scales. The colours are the four segments k-means found using all three variables. '
                         'Notice that the clouds touch. There is no gap that separates the groups, because customers behave on a continuum. The segments are slices of that cloud, and the edges are soft. '
                         'That is normal for customer data, and it is why we treat segments as useful groupings and never as natural facts. The names on the right come from the next two slides. '
                         'Where would you draw the line between the red and the black dots?')))

    # ------------------------------------------------------------------ 13 centroids
    S.append(dict(kind='wide', title='What each segment is like: how far its average sits from the average customer',
                  visual=dict(kind='ds_i_centroids', names=NAMES, vals=[[float(v) for v in c] for c in F['centroids_scaled']], vars=['Recency', 'Frequency', 'Spend']),
                  caption='Bars: standard deviations from the average customer. Red above, black below.',
                  notes=('To name a segment, read its average against the average customer, in standard deviations. Remember that high recency is bad: it means a long time since the last order. '
                         'The first segment sits high on frequency and spend and low on recency: frequent, recent, big spenders. We call them best customers. The second has high recency, so it has been away a while, with about average frequency and spend: drifting regulars. '
                         'The third has very low recency, so it ordered recently, with about average spend: recent regulars. The fourth is high on recency and low on frequency and spend: lapsed low spenders. '
                         'The names are our judgement, and a colleague might choose others. Do these names fit what you would expect?')))

    # ------------------------------------------------------------------ 14 profile table
    S.append(dict(kind='table', title='Naming each segment in business words: who they are, in real units',
                  headers=['Segment name', 'Customers', 'Recency (days)', 'Orders', 'Spend (UGX)', 'Share of spend'],
                  rows=[[NAMES[k], n(r_['customers']), f'{r_["recency"]:.0f}', f'{r_["orders"]:.1f}', n(r_['spend']), f'{r_["share_spend"]:.0f}%'] for k, r_ in enumerate(pr)],
                  widths=[3.0, 1.7, 1.9, 1.5, 2.0, 1.9], icons=['coin', 'clock', 'calendar', 'person'], note=f'Averages per customer; your own run differs by up to about 5 percent. Share of spend is out of {n(F["spend_total"])} UGX.',
                  notes=(f'Here are the segments in real units, as averages per customer. The best customers are {pr[0]["share_customers"]:.0f} percent of customers and {pr[0]["share_spend"]:.0f} percent of all spend: {n(pr[0]["spend"])} shillings each, {pr[0]["orders"]:.1f} orders, last seen {pr[0]["recency"]:.0f} days ago. '
                         f'The drifting regulars are the biggest group, {n(pr[1]["customers"])} customers, with {pr[1]["share_spend"]:.0f} percent of spend, but they last ordered {pr[1]["recency"]:.0f} days ago. '
                         f'The recent regulars ordered {pr[2]["recency"]:.0f} days ago on average. The lapsed low spenders have only {pr[3]["orders"]:.1f} orders and {pr[3]["share_spend"]:.0f} percent of spend. '
                         'A table like this is what you take into a meeting. Which row would you worry about first?')))

    # ------------------------------------------------------------------ 15 actions
    S.append(dict(kind='table', title='A segment is only useful if each name comes with an action',
                  headers=['Segment name', 'Who they are', 'What we would do'],
                  rows=[[NAMES[k], f'{n(pr[k]["customers"])} customers; last order {pr[k]["recency"]:.0f} days ago; {pr[k]["orders"]:.1f} orders', ACTIONS[k]] for k in range(4)],
                  widths=[2.7, 4.7, 4.6], icons=['coin', 'clock', 'calendar', 'person'],
                  notes=('A segment is only useful if the name leads to an action. For the best customers we protect them with early access and a named contact. For the drifting regulars, who are the largest group and are slipping away, a reminder offer in the next month. '
                         'For the recent regulars we try to grow the basket with higher-value products. And for the lapsed low spenders we send a low-cost message and do not spend heavily. '
                         'These actions are our proposals. The test of a segmentation is whether the manager can act on it on Monday. Which action would cost the least to try?')))

    # ------------------------------------------------------------------ 16 instability
    S.append(dict(kind='table', title=f'Re-running k-means moves segment sizes by up to {spread_max} customers: do not quote a size to the last customer',
                  headers=['Segment, by size', 'Smallest over 60 starts', 'Largest over 60 starts'], rows=[[lab, n(a), n(b)] for lab, (a, b) in zip(['Smallest', 'Second smallest', 'Second largest', 'Largest'], sizes_rng)],
                  widths=[4.0, 4.0, 4.0], icons=['person', 'person', 'person', 'person'],
                  note=f'60 runs with different random starts. The inertia stays between {n(F["k4_inertia_min60"])} and {n(F["k4_inertia_max60"])}.',
                  notes=(f'k-means starts from random centroids, so different starts can end in slightly different answers. We ran it sixty times. The inertia stays between {n(F["k4_inertia_min60"])} and {n(F["k4_inertia_max60"])}, so all the answers are about equally good. '
                         f'But the segment sizes move: the largest segment is between {n(sizes_rng[3][0])} and {n(sizes_rng[3][1])} customers, and the third segment varies by {sizes_rng[2][1] - sizes_rng[2][0]}. '
                         'That is what we expect when the clouds touch. Fix the random state so your result is reproducible, and do not quote a segment size to the last customer. '
                         'Always say these are useful groupings, with soft edges. How would you tell a manager that?')))

    # ------------------------------------------------------------------ 17 PCA picture
    S.append(dict(kind='wide', title=f'PCA squeezes three variables into two principal components that keep about {sum(ratio[:2]) * 100:.0f} percent of the variance',
                  visual=dict(kind='ds_i_pca', scores=pca['scores'], seg=F['scatter']['seg'], ratio=ratio),
                  caption='Dimensionality reduction: fewer variables, same customers. Colours are the k-means segments.',
                  notes=(f'Three variables cannot be drawn on a flat page, so we use principal component analysis, or PCA. It is a dimensionality reduction method. It builds new variables, called principal components, each a weighted mix of the originals. '
                         f'The first component is the direction in which the customers vary most. It carries {ratio[0] * 100:.0f} percent of the variance. The second carries {ratio[1] * 100:.0f} percent, and the third {ratio[2] * 100:.0f}. '
                         f'The first two together keep {sum(ratio[:2]) * 100:.0f} percent, so a flat picture loses little. The colours are the segments from k-means. They overlap in the middle, because the clouds touch and the segments are slices of one cloud. The picture is for drawing and checking. '
                         'We use PCA to draw and to check, and k-means ran on all three variables. What does explained variance tell you?')))

    # ------------------------------------------------------------------ 18 loadings
    S.append(dict(kind='table', title='Each principal component is a weighted mix of recency, frequency and spend',
                  headers=['Variable', 'PC1 weight', 'PC2 weight', 'PC3 weight'],
                  rows=[[v, f'{comps[0][i]:+.2f}', f'{comps[1][i]:+.2f}', f'{comps[2][i]:+.2f}'] for i, v in enumerate(['Recency', 'Frequency', 'Monetary value'])] + [['Explained variance', f'{ratio[0] * 100:.1f}%', f'{ratio[1] * 100:.1f}%', f'{ratio[2] * 100:.1f}%']],
                  widths=[3.6, 2.8, 2.8, 2.8], icons=['clock', 'receipt', 'coin', 'chart'],
                  note='The sign of a component is arbitrary: flipping every sign gives the same picture. Components are listed from most to least variance.',
                  notes=(f'This table shows the recipe for each principal component. The first component gives frequency and spend large weights of the same sign, {comps[0][1]:+.2f} and {comps[0][2]:+.2f}, and recency the opposite sign, {comps[0][0]:+.2f}. '
                         'So it reads as overall engagement: frequent, big-spending, recent customers at one end and the reverse at the other. '
                         f'The second component is mostly recency, with a weight of {comps[1][0]:+.2f}. The last row shows the explained variance. The sign of a component is arbitrary, so your notebook may show the picture flipped. '
                         'The components are ordered by how much variance they carry. Which original variable does the second component follow?')))

    # ------------------------------------------------------------------ 19 percentile rule
    S.append(dict(kind='stat', title='Anomaly detection, rule one: flag orders above the 99th percentile (the percentile rule)', big='1%',
                  text=f'{n(rule["n"])} of {n(F["orders"])} orders are above the 99th percentile, {n(rule["p99"])} UGX. Median of flagged: {n(rule["median_big"])} UGX. Median of all orders: {n(rule["median_all"])} UGX.', waffle_label='orders in every 100 are flagged',
                  notes=(f'The second half of today is anomaly detection: finding records that look very different from the rest, also called outlier detection. The simplest tool is the percentile rule. Sort all the orders by value and flag those above the 99th percentile, which is {n(rule["p99"])} shillings. '
                         f'That flags {n(rule["n"])} of {n(F["orders"])} orders, about one in a hundred. The median of the flagged orders is {n(rule["median_big"])} shillings, against {n(rule["median_all"])} for all orders. '
                         f'{rule["walkin"]} of the flagged orders are walk-ins. The rule is simple and transparent, and it always flags exactly one percent whether or not anything is wrong. '
                         'It also looks at one variable at a time. What might it miss?')))

    # ------------------------------------------------------------------ 20 isolation demo
    S.append(dict(kind='wide', title='An isolation forest isolates an odd record with few random cuts, and a typical record needs many',
                  visual=dict(kind='ds_i_isodemo', points=demo['points'], panels=[dict(title='An odd customer', sub='recency high, spend very low', sub2=f'isolated after {len(demo["odd_cuts"])} cuts in this run', cuts=demo['odd_cuts'], target=demo['odd']),
                                                                                    dict(title='A typical customer', sub='near the middle of the cloud', sub2=f'isolated after {len(demo["typ_cuts"])} cuts in this run', cuts=demo['typ_cuts'], target=demo['typical'])]),
                  caption=f'Mean of {demo["reps"]} runs: {demo["odd_mean"]:.1f} and {demo["typ_mean"]:.1f} cuts. The real forest uses 100 trees on 256 customers each.',
                  notes=(f'IsolationForest works on a different idea. Cut the data with random lines, each one across a random variable at a random value, until a record sits alone. An odd record, far from the cloud, is isolated after very few cuts. '
                         f'A typical record, deep inside the cloud, needs many. In this run the odd customer is alone after {len(demo["odd_cuts"])} cuts and the typical one needs {len(demo["typ_cuts"])}. Averaged over {demo["reps"]} runs, it is {demo["odd_mean"]:.1f} cuts and {demo["typ_mean"]:.1f}. '
                         'The forest repeats this with many random trees and turns the average number of cuts into an anomaly score. A short path means a high score. The picture uses forty customers and two variables to keep it readable. '
                         'Why does this idea need no answer column?')))

    # ------------------------------------------------------------------ 21 isolation result
    S.append(dict(kind='table', title=f'An isolation forest flags {iso["n"]} unusual customers: lapsed low spenders and extreme spenders',
                  headers=['Customer', 'Recency (days)', 'Orders', 'Spend (UGX)'],
                  rows=[[cid, str(r_[0]), str(r_[1]), n(r_[2])] for cid, r_ in zip(iso['top_ids'], iso['top_rows'])] + [['Median of the 25 flagged', f'{iso["med_rec"]:.0f}', f'{iso["med_freq"]:.0f}', n(iso['med_spend'])],
                                                                                                                          ['Median of all customers', f'{st["recency"]["median"]:.0f}', f'{st["frequency"]["median"]:.0f}', n(st['spend']['median'])]],
                  widths=[4.2, 2.6, 2.2, 3.0], icons=['person', 'person', 'person', 'magnifier', 'people'],
                  note=f'Of the {iso["n"]} flagged: {lapsed} are long-lapsed with low spend, {heavy} spent over 800,000 UGX, {other} are other. Our NumPy isolation forest: scikit-learn will differ a little.',
                  notes=(f'We ran an isolation forest on the {n(F["n_cust"])} customers, using the three scaled variables, and flagged the most isolated one percent, which is {iso["n"]} customers. The top three are shown, with the median of all the flagged and of all customers. '
                         f'Of the {iso["n"]} flagged, {lapsed} are customers who have been away a long time and spent little, {heavy} spent more than eight hundred thousand shillings, and {other} are mixed. '
                         f'This is our own NumPy version of the algorithm. Run with a different random seed, it flags a list that overlaps ours on {iso["overlap_other_seed"]} of {iso["n"]}, and scikit-learn will differ a little too. '
                         'Anomaly detection is a way to choose what to look at. Which of these would you check first?')))

    # ------------------------------------------------------------------ 22 what to do
    S.append(dict(kind='statement', title='An anomaly is a record to review, and the review decides what happens', lead='Flagging is the start of the work.',
                  points=['Check for an error: a typing slip, a duplicate or a test order.', 'Check for a real and important case: a wholesale buyer or a fraud.', 'Record the decision and the reason.'], icons=['magnifier', 'people', 'doc'],
                  notes=('What do you do with a flagged record? You review it. First check for an error: a typing slip, a duplicate or a test order. If it is an error, correct it or exclude it, and write down why. '
                         'Second, check whether it is real and important. A very large order might be a wholesale buyer you want to look after, or a fraud you want to stop. A customer who stopped ordering might be about to leave for a competitor. '
                         'Third, record your decision and the reason. Never delete an anomaly just because an algorithm flagged it. Who would review flagged records in your organisation?')))

    # ------------------------------------------------------------------ 23 use at work
    S.append(dict(kind='table', title='Where you will use this at work: group records, then act on the groups',
                  headers=['Your job', 'The records you meet', 'What today lets you do'],
                  rows=[['Marketing analyst at a supermarket chain, using pandas and scikit-learn', 'Till orders with a loyalty id.', 'Build RFM, run k-means, name four segments and attach an action to each.'],
                        ['Manager of a mobile money agent network', 'Transactions per agent per month.', 'Segment agents by recency, frequency and value, and find the agents who are drifting away.'],
                        ['Member services officer at a SACCO, using Excel', 'Savings deposits and balances per member.', 'Export the segment table as CSV for Power BI or Excel, with each segment named and sized.'],
                        ['Internal auditor or finance controller', 'Payments and expense claims.', 'Flag the top one percent with the percentile rule, and an isolation forest for the odd combinations.']],
                  widths=[3.6, 3.7, 4.7], icons=['bag', 'phone', 'people', 'shield'],
                  notes=('Where will you use this on Monday? Four examples. A marketing analyst at a supermarket chain, with till orders and a loyalty id, can build RFM, run k-means, and name four segments with an action for each. '
                         'The manager of a mobile money agent network can segment agents by recency, frequency and value, and find the agents who are drifting away. '
                         'A member services officer at a SACCO can hand a segment table to the committee, with each segment named and sized. '
                         'And an internal auditor can flag the top one percent of payments with the percentile rule, and use an isolation forest for odd combinations. Which one is closest to your job?')))

    # ------------------------------------------------------------------ 24 bridge
    S.append(dict(kind='code', title='Read the recipe before the lab: log, scale, cluster, profile',
                  code='X = StandardScaler().fit_transform(np.log1p(rfm))\nkmeans = KMeans(n_clusters=4, n_init=10,\n                random_state=42)\nrfm["segment"] = kmeans.fit_predict(X)\nprint(kmeans.inertia_)\nrfm.groupby("segment")[["recency",\n    "frequency", "spend"]].mean().round(0)',
                  reads=['Line 1 takes the log of each variable, then scales it to a z-score.', 'Line 2 sets k = 4, 10 random starts, and fixes the random state.', 'Line 3 fits k-means and stores each customer\'s segment number.',
                         'Line 4 prints the inertia.', 'Line 5 profiles each segment in real units.'],
                  notes=('Before the lab, read the recipe. Line one takes the log of each of the three RFM variables with log one p, then scales them with StandardScaler. Line two creates the KMeans model with four clusters, ten random starts, and a fixed random state so you can repeat it. '
                         'Line three fits it and stores each customer\'s segment number as a new column. Line four prints the inertia, the number we use for the elbow. Line five groups by segment and takes the mean of each variable, which is the profile we name. '
                         'The segment numbers zero to three are only labels, and they can change from run to run. Why do the labels have no meaning on their own?')))

    # ------------------------------------------------------------------ 25 divider
    S.append(dict(kind='divider', title='Part 2: the Python lab', lead='Close the slides. Open the notebook.', section='Lab',
                  notes=('That is the end of the ideas. Everything you need is on the slides you have just seen, and the notebook repeats each step in plain words. '
                         'Open Google Colab and open the notebook for Session 18. Run the first cell to load the data, then the second cell to load the check helper. '
                         'In every step, predict first, run second, read third, and change one thing last. I will walk around. If you get stuck for more than three minutes, call me.')))

    # ------------------------------------------------------------------ 26 lab map
    S.append(dict(kind='steps', title='The lab has six parts, and you keep a segment file with names and actions',
                  steps=[dict(head='1 RFM', text='Loyalty orders, then recency, frequency, spend', icon='receipt'), dict(head='2 Log, scale', text='log1p and z-scores', icon='calculator'), dict(head='3 k-means', text='Four clusters and the elbow', icon='chart'),
                         dict(head='4 PCA', text='Explained variance', icon='magnifier'), dict(head='5 Name', text='Profile, names, actions', icon='people'), dict(head='6 Flag, keep', text='Percentile rule, isolation forest, save', icon='folder')], highlight=None,
                  caption='Six parts, eight tasks in 45 minutes. In each task, predict first, run second, read what the output tells you, then change one thing.',
                  notes=('Here is the map of the lab. Step one, keep the loyalty orders and build recency, frequency and spend. Step two, take the log and standardise. Step three, run k-means with four clusters and draw the elbow chart. '
                         'Step four, run PCA and read the explained variance. Step five, profile each segment, then name it and give it an action. Step six, flag the unusual orders and customers, and save your segment file. '
                         'In every task, predict first, run second, read, then change one thing. Please do not skip the predictions.')))

    # ------------------------------------------------------------------ 27 check numbers
    S.append(dict(kind='table', title='Check your numbers before you move on', headers=['What you compute', 'You should get'],
                  rows=[['Loyalty orders, and customers', f'{n(F["loyal_orders"])} and {n(F["n_cust"])}'], ['RFM of customer C0001', f'{F["rfm_head"][0][1]} days, {F["rfm_head"][0][2]} orders, {n(F["rfm_head"][0][3])} UGX'],
                        ['Skewness of spend, raw and logged', f'{st["spend"]["skew"]:.2f} and {F["skew_log"]["spend"]:.2f}'], ['Inertia for k = 1, and for k = 4', f'{n(inert[1])}, and about {n(inert[4])} (within 5)'],
                        ['Segment sizes, k = 4, smallest to largest', f'about {sizes_rng[0][0]}-{sizes_rng[0][1]}, {sizes_rng[1][0]}-{sizes_rng[1][1]}, {sizes_rng[2][0]}-{sizes_rng[2][1]}, {sizes_rng[3][0]}-{sizes_rng[3][1]}'],
                        ['Explained variance of PC1, PC2, PC3', f'{ratio[0]:.3f}, {ratio[1]:.3f}, {ratio[2]:.3f}'], ['99th percentile of order value, and orders above it', f'{n(rule["p99"])} UGX, {rule["n"]} orders'],
                        ['Customers flagged by IsolationForest (contamination 0.01)', f'about {iso["n"]}']],
                  widths=[6.0, 6.0], icons=['receipt', 'person', 'calculator', 'chart', 'people', 'magnifier', 'coin', 'shield'], note='k-means uses random starts, so segment sizes vary a little between runs. The notebook checks allow for that.',
                  notes=('Use this table as your own self-check. Nobody marks it. The counts, the RFM numbers, the skewness and the PCA variances should match exactly. The inertia for k equal to one is exact, and for k equal to four it should be within five. '
                         'The segment sizes depend on the random starts, so accept the ranges shown. If a number is far off, stop and call me, because later tasks use the earlier ones. '
                         'Do not change a number to make it match. Find out why it is different. What would make the inertia for k equal to one different from three times the number of customers?')))

    # ------------------------------------------------------------------ 28 error cards
    S.append(dict(kind='table', title='Five likely mistakes in the lab and how to fix them', headers=['What you see', 'What it means', 'What to do'],
                  rows=[[f'{n(F["orders"])} customers instead of {n(F["n_cust"])}', 'The walk-in orders (blank customer_id) are still in.', 'Drop the blank customer_id values first, with dropna on customer_id.'],
                        ['Recency is negative or huge', 'The end date came from today\'s date.', 'Use the last order_date in the file as the end date.'],
                        ['Segment 0 is different from the slide', 'The segment numbers are only labels.', 'Match segments by their averages.'],
                        ['Spend dominates the clusters', 'The variables were not scaled.', 'Apply log1p and StandardScaler before KMeans.'],
                        ['Inertia for k = 1 is not 7,497', 'The data were not standardised, or a row was dropped.', f'Three standardised variables over {n(F["n_cust"])} customers give {n(inert[1])}.']],
                  widths=[3.6, 4.2, 4.2], icons=['cross', 'cross', 'check', 'cross', 'calculator'],
                  notes=('Five situations you may meet. If you get more customers than expected, the walk-in orders are still in, so drop the blank customer ids first. If recency looks wrong, you used today\'s date, so use the last order date in the file instead. '
                         'If your segment zero looks different from the slide, that is fine, because the numbers are only labels, so match the segments by their averages. If spend dominates, you forgot to scale. '
                         'And the inertia for k equal to one should be seven thousand four hundred and ninety seven: three standardised variables times the number of customers. Which of these would you have guessed?')))

    # ------------------------------------------------------------------ 29 exit check
    S.append(dict(kind='table', title='Exit check: three questions, then compare with the short answers', headers=['Question', 'Short answer'],
                  rows=[['Why do we take the log of spend and then standardise before k-means?', f'The log squeezes the long tail (skewness {st["spend"]["skew"]:.2f} to {F["skew_log"]["spend"]:.2f}). Standardising gives the three variables one scale, so none dominates the distance.'],
                        ['The elbow chart bends gently between k = 3 and k = 5. How do you choose k?', 'Treat the elbow as a hint. Choose the k whose segments you can name and act on, and say it is a judgement.'],
                        [f'An isolation forest flags {iso["n"]} customers. What do you do next?', 'Review each one: an error, or a real and important case. Record the decision. Never delete them automatically.']],
                  widths=[5.6, 6.4], icons=['calculator', 'chart', 'magnifier'],
                  notes=('Last, the exit check. Three questions. Write your answers in your notes before you look at mine. One, why do we take the log of spend and then standardise before k-means? '
                         'Two, the elbow chart bends gently between three and five. How do you choose k? Three, an isolation forest flags twenty five customers. What do you do next? '
                         'The short answers are on the slide. If you got all three, you are ready for Session 19. If one surprised you, look at that part of your notebook again tonight.')))

    # ------------------------------------------------------------------ facilitator
    sess['facilitator'] = dict(
        prep=['Open the deck and the notebook for Session 18 in Colab before anyone arrives, and run the whole notebook once on the free Colab runtime to confirm the check numbers. The slide numbers were computed in NumPy, because scikit-learn is not installed in the build environment.',
              'Upload data.zip to your own Colab session first, so you can show where the file goes.', 'Write the check table (slide 27) on the board before the lab.', 'Concepts run with laptops closed. Ask learners to open Colab only after the Part 2 divider.',
              'Tell learners in advance that segment numbers and segment sizes will differ a little from the slides.'],
        misconceptions=[('k-means finds the true groups in the data', f'It cuts a continuous cloud into k slices. Sixty random starts give segment sizes that differ by up to {spread_max} customers.'),
                        ('The elbow tells you the right k', 'The elbow is a hint. Here the bend is gentle, and the final choice rests on whether the segments can be named and used.'),
                        ('Segment 0 is always the best customers', 'The numbers are only labels and change between runs. Read the averages.'),
                        ('Scaling is optional', f'Without scaling, spend (standard deviation {n(F["raw_sd"]["spend"])} UGX) decides nearly every distance.'),
                        ('An anomaly is an error, so delete it', 'An anomaly is a record to review. It can be an error or a real and important case.')],
        probes=[('What is the difference between supervised and unsupervised learning?', 'Supervised has an answer column to learn and score against. Unsupervised has none.'),
                ('What do R, F and M stand for?', 'Recency, frequency and monetary value.'),
                ('What are the two moves that k-means repeats?', 'Assign each record to the nearest centroid, then update each centroid to the mean of its cluster.'),
                ('What is inertia, and why does it always fall as k grows?', 'The sum of squared distances to the centroids. More clusters can only get closer to the records.'),
                ('Why does PCA help you draw the customers?', 'It builds two principal components that keep most of the variance, so three variables fit on a flat chart.'),
                ('What does the percentile rule always do?', 'It flags exactly the chosen share of records, whether or not any is odd.'),
                ('How does an isolation forest score a record?', 'By how few random cuts it takes to isolate it. Fewer cuts means more anomalous.')],
        lab_steps=[('Task 1: loyalty orders', f'{n(F["loyal_orders"])} loyalty orders and {n(F["n_cust"])} customers. {n(F["walkin"])} walk-in orders out.'),
                   ('Task 2: RFM', f'C0001: {F["rfm_head"][0][1]} days, {F["rfm_head"][0][2]} orders, {n(F["rfm_head"][0][3])} UGX. Watch for today\'s date used as the end date.'),
                   ('Task 3: log and scale', f'Skewness of spend {st["spend"]["skew"]:.2f} to {F["skew_log"]["spend"]:.2f}. Use ddof=0 to match StandardScaler.'),
                   ('Task 4: k-means', f'Inertia about {n(inert[4])}, sizes inside the ranges on the check slide.'),
                   ('Task 5: elbow', f'k = 1 gives {n(inert[1])} exactly. The bend is gentle.'),
                   ('Task 6: PCA', f'{ratio[0]:.3f}, {ratio[1]:.3f}, {ratio[2]:.3f}. The signs of the components may flip.'),
                   ('Task 7: profile and names', 'Four segments with a name and an action each, matched by averages, not by number.'),
                   ('Task 8: anomalies', f'p99 {n(rule["p99"])} UGX, {rule["n"]} orders. IsolationForest flags about {iso["n"]} customers.')],
        rescue=['If the concepts run over, shorten the PCA slides (slides 17 and 18) and the isolation demo (slide 20); the lab covers both.', 'If only 30 minutes of lab remain, do tasks 1, 2, 3, 4, 7 and 8 and set the rest as homework.',
                'If a learner cannot upload data.zip, the first cell explains how to use a link from the tutor.', 'If a learner has no laptop, pair them with a neighbour: one types, one predicts aloud.'],
        after=['Share the deck and the solution notebook again for learners who were absent.', 'Ask each learner to save customer_segments.csv and bring one question about forecasting to Session 19.', 'Note any question you could not answer and open the next session with it.'],
        lab_answer_key=[['Task 1 PREDICT: how many customers will the loyalty orders cover?', f'{n(F["n_cust"])}. The customers file lists {n(F["customers_file"])}, and one never ordered.'],
                        ['Task 2 READ: why is the mean spend above the median?', 'A few large spenders pull the mean up: a right-skewed variable.'],
                        ['Task 3 READ: what did the log do to the skewness of spend?', f'It fell from {st["spend"]["skew"]:.2f} to {F["skew_log"]["spend"]:.2f}.'],
                        ['Task 4 CHANGE: change random_state to 7. What moves?', f'The segment numbers and the sizes move by a few customers (up to about {spread_max}). The inertia stays near {n(inert[4])}.'],
                        ['Task 5 READ: where is the elbow, and is it sharp?', 'Around k = 3 to 5. It is gentle, so the choice of 4 is a judgement.'],
                        ['Task 6 READ: how much variance do two components keep?', f'{sum(ratio[:2]) * 100:.1f} percent.'],
                        ['Task 7 READ: which segment holds the most spend?', f'The best customers: {pr[0]["share_customers"]:.0f} percent of customers, {pr[0]["share_spend"]:.0f} percent of spend.'],
                        ['Task 8 CHANGE: set contamination to 0.05. What happens?', 'About 125 customers are flagged (5 percent of 2,499). The rule always flags the share you ask for.']])
    return sess
