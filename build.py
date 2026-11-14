#!/usr/bin/env python3
"""Builds deadlines.json, deadlines.csv and mtd-income-tax-deadlines.ics for the tax years below. Python 3, no dependencies.
Rules (GOV.UK, checked 2026-11-14; see README): quarterly update deadlines are 7 Aug, 7 Nov, 7 Feb and 7 May, the same
for standard (6 Apr-5 Apr) and calendar (1 Apr-31 Mar) update periods; the online tax return is due 31 January after
the tax year; payments on account are due 31 January and 31 July in the tax year's second half, and the balancing
payment 31 January after it."""
import csv, datetime as dt, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
YEARS = [2026, 2027, 2028]  # tax years 2026-27 to 2028-29 (the year each starts on 6 April)
SRC_Q = 'https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/send-quarterly-updates'
SRC_SA = 'https://www.gov.uk/self-assessment-tax-returns/deadlines'
SRC_PEN = 'https://www.gov.uk/guidance/penalties-for-making-tax-digital-for-income-tax'
SRC_POA = 'https://www.gov.uk/understand-self-assessment-bill/payments-on-account'
SRC_ELIG = 'https://www.gov.uk/guidance/find-out-if-and-when-you-need-to-use-making-tax-digital-for-income-tax'
# Who must use MTD for Income Tax in each tax year (qualifying income = self-employment + property income before expenses)
MANDATED = {2026: 'qualifying income over £50,000 in 2024-25',
            2027: 'qualifying income over £30,000 in 2025-26 (plus everyone already in)',
            2028: 'qualifying income over £20,000 in 2026-27 (plus everyone already in)'}
D = dt.date

def rows():
    out = []
    for y in YEARS:
        ty = f'{y}-{str(y + 1)[2:]}'
        std = [(D(y, 4, 6), D(y, 7, 5)), (D(y, 7, 6), D(y, 10, 5)), (D(y, 10, 6), D(y + 1, 1, 5)), (D(y + 1, 1, 6), D(y + 1, 4, 5))]
        cal = [(D(y, 4, 1), D(y, 6, 30)), (D(y, 7, 1), D(y, 9, 30)), (D(y, 10, 1), D(y, 12, 31)), (D(y + 1, 1, 1), D(y + 1, 3, 31))]
        due = [D(y, 8, 7), D(y, 11, 7), D(y + 1, 2, 7), D(y + 1, 5, 7)]
        for q in range(4):
            out.append(dict(id=f'{ty}-Q{q + 1}', tax_year=ty, type='quarterly_update', quarter=q + 1, deadline=due[q].isoformat(),
                title=f'MTD quarterly update {ty} Q{q + 1} due',
                standard_period_start=std[q][0].isoformat(), standard_period_end=std[q][1].isoformat(),
                calendar_period_start=cal[q][0].isoformat(), calendar_period_end=cal[q][1].isoformat(),
                note=('No penalty points for late quarterly updates in 2026-27 (HMRC).' if y == 2026 else 'A late quarterly update earns a penalty point (one per deadline, even with several businesses); at 4 points a £200 penalty, then £200 for each further missed deadline. Volunteers: no points for late quarterly updates.'),
                source=SRC_Q))
        out.append(dict(id=f'{ty}-return', tax_year=ty, type='tax_return', quarter=None, deadline=D(y + 2, 1, 31).isoformat(),
            title=f'Tax return for {ty} due (online, 11:59pm)', standard_period_start=None, standard_period_end=None,
            calendar_period_start=None, calendar_period_end=None,
            note='Submitted through MTD-compatible software for anyone in MTD that year. Penalty points apply to late returns.', source=SRC_SA))
        none = dict(quarter=None, standard_period_start=None, standard_period_end=None, calendar_period_start=None, calendar_period_end=None)
        out.append(dict(id=f'{ty}-first-payment-on-account', tax_year=ty, type='payment', deadline=D(y + 1, 1, 31).isoformat(),
            title=f'First payment on account for {ty} due (if you make payments on account)', **none,
            note='Usually half of the previous year\'s bill; not needed if that bill was under £1,000 or over 80% was collected another way. MTD does not change payment dates.', source=SRC_POA))
        out.append(dict(id=f'{ty}-second-payment-on-account', tax_year=ty, type='payment', deadline=D(y + 1, 7, 31).isoformat(),
            title=f'Second payment on account for {ty} due (if you make payments on account)', **none,
            note='MTD does not change payment dates.', source=SRC_POA))
        out.append(dict(id=f'{ty}-balancing-payment', tax_year=ty, type='payment', deadline=D(y + 2, 1, 31).isoformat(),
            title=f'Balancing payment for {ty} due (tax owed after any payments on account)', **none,
            note='MTD does not change payment dates.', source=SRC_SA))
    for r in out:
        d = D.fromisoformat(r['deadline']); r['weekday'] = d.strftime('%A')
        r['who'] = {'quarterly_update': 'People in MTD for Income Tax that year: ' + MANDATED[int(r['tax_year'][:4])],
                    'tax_return': 'Everyone who files a Self Assessment return (through MTD software if in MTD that year)',
                    'payment': 'Self Assessment taxpayers who owe tax'}[r['type']]
    return sorted(out, key=lambda r: (r['deadline'], r['type']))

def ics(rs):
    stamp = '20261114T000000Z'
    esc = lambda s: s.replace('\\', '\\\\').replace(',', '\\,').replace(';', '\\;')
    def fold(line):
        b = line.encode(); parts = []
        while len(b) > 75:
            cut = 75 if not parts else 74
            while (b[cut] & 0xC0) == 0x80: cut -= 1
            parts.append(b[:cut].decode()); b = b[cut:]
        parts.append(b.decode()); return '\r\n '.join(parts)
    L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Smallwright//mtd-quarterly-deadlines//EN', 'CALSCALE:GREGORIAN',
         'X-WR-CALNAME:MTD for Income Tax deadlines', 'X-WR-TIMEZONE:Europe/London']
    for r in rs:
        d = D.fromisoformat(r['deadline'])
        desc = r['title'] + '.'
        if r['type'] == 'quarterly_update':
            desc += f" Covers {r['standard_period_start']} to {r['standard_period_end']} (standard) or {r['calendar_period_start']} to {r['calendar_period_end']} (calendar)."
        desc += f" Who: {r['who']}. {r['note']} Source: {r['source']}"
        L += ['BEGIN:VEVENT', f"UID:{r['id']}@mtd-quarterly-deadlines.smallwright", f'DTSTAMP:{stamp}',
              f'DTSTART;VALUE=DATE:{d:%Y%m%d}', f'DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}',
              fold('SUMMARY:' + esc(r['title'])), fold('DESCRIPTION:' + esc(desc)), fold('URL:' + r['source']), 'TRANSP:TRANSPARENT', 'END:VEVENT']
    L.append('END:VCALENDAR')
    return '\r\n'.join(L) + '\r\n'

def main():
    rs = rows()
    meta = {'name': 'MTD for Income Tax deadlines', 'tax_years': [f'{y}-{str(y + 1)[2:]}' for y in YEARS], 'checked': '2026-11-14',
            'sources': [SRC_Q, SRC_PEN, SRC_SA, SRC_POA, SRC_ELIG], 'licence': 'MIT', 'repository': 'https://github.com/Smallwright/mtd-quarterly-deadlines',
            'notes': 'Dates are as GOV.UK publishes them. GOV.UK guidance does not say a deadline moves when it falls on a weekend.'}
    (HERE / 'deadlines.json').write_text(json.dumps({**meta, 'deadlines': rs}, indent=2, ensure_ascii=False) + '\n')
    cols = ['id', 'tax_year', 'type', 'quarter', 'deadline', 'weekday', 'title', 'standard_period_start', 'standard_period_end',
            'calendar_period_start', 'calendar_period_end', 'who', 'note', 'source']
    with open(HERE / 'deadlines.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rs)
    (HERE / 'mtd-income-tax-deadlines.ics').write_bytes(ics(rs).encode())
    for r in rs: print(r['deadline'], r['weekday'][:3], r['id'])

if __name__ == '__main__':
    main()
