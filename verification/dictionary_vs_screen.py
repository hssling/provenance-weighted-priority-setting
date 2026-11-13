"""Compare the screen's verdicts (outputs/d2_variable_screen.csv) with the labels in WHO's
data dictionary, and re-examine the one financial variable the dictionary does not label.
Reads only data/ and outputs/. Run: python verification/dictionary_vs_screen.py"""
import csv, collections, re, statistics
from math import comb
M = {'budget': 'Budget', 'expenditure': 'Expenditure and utilisation', 'notifications': 'Notification',
     'outcomes': 'Outcomes', 'laboratory': 'Laboratory and diagnostic services',
     'contact_tpt': 'Contacts and preventive treatment'}
F = {'budget': 'TB_budget_2026-11-12.csv', 'expenditure': 'TB_expenditure_utilisation_2026-08-25.csv',
     'notifications': 'TB_notifications_2026-08-25.csv', 'outcomes': 'TB_outcomes_2026-08-25.csv',
     'laboratory': 'TB_laboratory_diagnostic_services_2026-08-25.csv', 'contact_tpt': 'TB_contact_tpt_2026-08-25.csv'}
dic = {(r['dataset'], r['variable_name']): r['definition']
       for r in csv.DictReader(open('data/TB_dictionary_2026-08-25.csv', encoding='cp1252'))}
scr = list(csv.DictReader(open('outputs/d2_variable_screen.csv')))
# a dictionary "label" = the definition says the quantity is estimated or typical
lab = lambda d: bool(re.search(r'estimat|typical', d, re.I))
for r in scr: r['def'] = dic[(M[r['dataset']], r['column'])]; r['lab'] = lab(r['def'])
print('screened variables', len(scr), 'unmatched in dictionary', 0)
ct = collections.Counter((r['lab'], r['verdict']) for r in scr)
for k in sorted(ct): print('labelled' if k[0] else 'unlabelled', k[1], ct[k])
labelled = [r for r in scr if r['lab']]
for r in labelled: print('  ', r['column'], r['verdict'], r['def'][:60])
cont = [r for r in scr if r['verdict'] in ('measurement-like', 'mixed', 'estimate-like')]
non = sum(r['verdict'] != 'measurement-like' for r in cont)
print('continuous', len(cont), 'non-measurement-like', non,
      'P(all 6 labelled land non-measurement-like | random) = %.4f' % (comb(non, 6) / comb(len(cont), 6)))
# what is the modal value of each estimate-like variable?
cache = {}
def vals(ds, c):
    if ds not in cache: cache[ds] = list(csv.DictReader(open('data/' + F[ds], encoding='utf-8-sig', errors='replace')))
    out = []
    for r in cache[ds]:
        try: out.append(float(r[c]))
        except (ValueError, KeyError): pass
    return out
zero = collections.Counter()
for r in scr:
    if r['verdict'] == 'estimate-like':
        v = vals(r['dataset'], r['column']); mode = collections.Counter(v).most_common(1)[0][0]
        zero[(r['lab'], mode == 0)] += 1
print('estimate-like by (labelled, modal value is zero):', dict(zero))
# cf_tot_usaid versus the other expected-funding sources
rows = list(csv.DictReader(open('data/' + F['budget'], encoding='utf-8-sig')))
def rep(col):
    by = collections.defaultdict(dict)
    for r in rows:
        try: by[r['iso3']][int(r['year'])] = float(r[col])
        except ValueError: pass
    allp = same = nz = nzs = 0; n = z = 0
    for d in by.values():
        n += len(d); z += sum(x == 0 for x in d.values())
        for a, b in zip(sorted(d), sorted(d)[1:]):
            if b - a == 1:
                allp += 1; same += d[a] == d[b]
                if d[a] != 0 or d[b] != 0: nz += 1; nzs += d[a] == d[b]
    return dict(n=n, share_zero=round(z / n, 3), pairs=allp, rep_all=round(same / allp, 3), pairs_nonzero=nz,
                rep_nonzero=round(nzs / nz, 3))
for c in ('cf_tot_usaid', 'cf_tot_gf', 'cf_tot_grnt', 'cf_tot_domestic', 'cf_tot'): print(c, rep(c))
