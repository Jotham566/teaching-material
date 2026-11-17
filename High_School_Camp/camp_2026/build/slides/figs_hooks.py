"""Illustrations for the 'Where this is used' slide: three pictograms in a column joined by arrows, each with a short label.
HOOK_NODES maps a deck id to its three (icon, label) pairs. Labels are 16 characters or fewer."""
import figkit

HOOK_NODES = {
    'DA01': [('shop', 'Shop till'), ('laptop', 'Python'), ('magnifier', 'First look')],
    'DA02': [('tag', 'Name: text'), ('coin', 'Price: number'), ('calendar', 'Date')],
    'DA03': [('coin', 'Price'), ('calculator', 'Units x price'), ('receipt', 'Revenue')],
    'DA04': [('bag', 'An order'), ('gear', 'if or else'), ('tag', 'Big or small')],
    'DA05': [('ball', 'Many matches'), ('gear', 'Loop'), ('bars', 'Total')],
    'DA06': [('calculator', 'A function'), ('check', 'Known answer'), ('lock', 'Safe to trust')],
    'DA07': [('receipt', 'Till export'), ('folder', 'CSV file'), ('laptop', 'Table')],
    'DA08': [('shop', 'All sales'), ('magnifier', 'Pick rows'), ('coin', 'Revenue column')],
    'DA09': [('shop', 'Branches'), ('bars', 'Group totals'), ('pin', 'Best branch')],
    'DA10': [('receipt', 'Raw export'), ('magnifier', 'Find problems'), ('check', 'Clean log')],
    'DA11': [('receipt', 'Numbers'), ('bars', 'A chart'), ('person', 'One clear point')],
    'DA12': [('notebook', 'Table'), ('bars', 'One chart'), ('person', 'Your reader')],
    'DA13': [('calendar', 'Daily counts'), ('bars', 'Spread'), ('magnifier', 'Odd days')],
    'DA14': [('shop', 'Three shops'), ('bars', 'Box plots'), ('magnifier', 'Compare')],
    'DA15': [('rain', 'Rain'), ('bars', 'Pattern'), ('shop', 'Customers')],
    'DA16': [('receipt', 'Raw export'), ('gear', 'Clean function'), ('folder', 'Clean table')],
    'DA17': [('folder', 'Two tables'), ('gear', 'Merge'), ('check', 'Total checked')],
    'DA18': [('receipt', 'Cleaned total'), ('calculator', 'Compare'), ('magnifier', 'Explain the gap')],
    'DA19': [('person', 'You'), ('notebook', 'The plan'), ('check', 'Approved')],
    'DA20': [('notebook', 'Your log'), ('calculator', 'Two checks'), ('person', 'A partner')],
    'DA21': [('bars', 'Charts'), ('pen', 'Labels'), ('person', 'Reader alone')],
    'DA22': [('laptop', 'Restart'), ('check', 'Run all'), ('folder', 'Handover')],
    'DA23': [('bars', 'Findings'), ('pen', 'Plain words'), ('person', 'A parent')],
    'DA24': [('laptop', 'Demo'), ('person', 'Family'), ('check', 'Questions')],
    'ML01': [('home', 'A home'), ('gear', 'The model'), ('coin', 'Rent guess')],
    'ML02': [('phone', 'Phone number'), ('coin', 'Amount'), ('calendar', 'Date')],
    'ML03': [('pen', 'Typed text'), ('gear', 'Convert'), ('calculator', 'A number')],
    'ML04': [('flower', 'Petals'), ('gear', 'Three-line rule'), ('tag', 'Flower name')],
    'ML05': [('ball', 'Many matches'), ('gear', 'Loop'), ('bars', 'League table')],
    'ML06': [('calculator', 'Fee function'), ('check', 'Known answer'), ('phone', 'Used on all')],
    'ML07': [('receipt', 'Till'), ('folder', 'CSV file'), ('laptop', 'Python')],
    'ML08': [('shop', 'Sales'), ('magnifier', 'Filter'), ('coin', 'Revenue')],
    'ML09': [('bike', 'Boda fares'), ('bars', 'Mean, median'), ('magnifier', 'Odd ones')],
    'ML10': [('clinic', 'Register'), ('magnifier', 'Find errors'), ('check', 'Clean table')],
    'ML11': [('receipt', 'Numbers'), ('bars', 'A chart'), ('person', 'One point')],
    'ML12': [('notebook', 'A table'), ('bars', 'First chart'), ('person', 'Your question')],
    'ML13': [('sun', 'Today'), ('gear', 'Plain guess'), ('cloud', 'Tomorrow')],
    'ML14': [('pin', 'Distance'), ('gear', 'A line'), ('coin', 'Fare estimate')],
    'ML15': [('home', 'New home'), ('gear', 'The model'), ('check', 'Error checked')],
    'ML16': [('plant', 'Leaf'), ('gear', 'Questions'), ('check', 'Healthy or sick')],
    'ML17': [('phone', 'Payment'), ('lock', 'Fraud alert'), ('cross', 'Count mistakes')],
    'ML18': [('notebook', 'Practice'), ('gear', 'Pick depth'), ('ball', 'Unseen match')],
    'ML19': [('notebook', 'The plan'), ('lock', 'Leak check'), ('check', 'Approved')],
    'ML20': [('plant', 'Last price'), ('gear', 'Plain guess'), ('coin', 'Next price')],
    'ML21': [('person', 'Applicant'), ('gear', 'The model'), ('magnifier', 'Why?')],
    'ML22': [('gear', 'Frozen model'), ('folder', 'Project folder'), ('laptop', 'Rerun')],
    'ML23': [('laptop', 'Your model'), ('pen', 'Plain words'), ('person', 'A parent')],
    'ML24': [('laptop', 'Demo'), ('person', 'Family'), ('check', 'Questions')],
    'F01': [('notebook', 'Paper guess'), ('gear', 'Run it'), ('check', 'Match?')],
    'F02': [('sun', 'Daily readings'), ('folder', 'Fixed order'), ('bars', 'An array')],
    'F03': [('cloud', 'Forecast'), ('bars', 'Spread'), ('clinic', 'Shares')],
    'F04': [('home', 'Size, rooms'), ('gear', 'Weights'), ('coin', 'Rent')],
    'ML25': [('phone', 'Voice'), ('gear', 'Neural network'), ('pen', 'Words')],
}


def draw_nodes(s, w, h, nodes):
    ys = [h - 0.65, h / 2, 0.65]
    for k, (icon, label) in enumerate(nodes):
        s.icon(icon, 0.8, ys[k], 0.95, **({'text': ''} if icon == 'coin' else {}))
        s.text(1.55, ys[k], label, size=20, weight='bold', ha='left')
        if k < 2:
            s.arrow(0.8, ys[k] - 0.5, 0.8, ys[k + 1] + 0.5, lw=2.2, head=14)


def draw_strip(s, w, h, session=None, lab_after=None, label=''):
    """24 dots in eight groups of three. Earlier sessions black, the current one gold, later ones empty.
    lab_after: a gold diamond sits after that session, with room of its own, so a lab shows between its neighbours."""
    cy = h / 2
    pitch, gap, r, lab_room = 0.3, 0.17, 0.115, 0.34
    total = 24 * pitch + 7 * gap + (lab_room if lab_after else 0)
    x = w - total + pitch / 2 - 0.1
    s.text(0.0, cy, label, size=20, weight='bold', ha='left')
    for i in range(1, 25):
        done = (session is not None and i < session) or (lab_after is not None and i <= lab_after)
        cur = session == i
        s.circle(x, cy, r * (1.22 if cur else 1), fill=figkit.GOLD if cur else (figkit.INK if done else figkit.PAPER), edge=figkit.INK, lw=2.2 if cur else 1.6, z=3)
        x += pitch + (gap if i % 3 == 0 else 0)
        if lab_after == i:
            nx = x - pitch / 2 + lab_room / 2 - (gap if i % 3 == 0 else 0) / 2 + (0.0)
            s.poly([(nx, cy + 0.2), (nx + 0.13, cy), (nx, cy - 0.2), (nx - 0.13, cy)], fill=figkit.GOLD, edge=figkit.INK, lw=1.8, z=4)
            x += lab_room
