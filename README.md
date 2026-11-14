# MTD for Income Tax deadlines (2026-27 to 2028-29)

A machine-readable list of every Making Tax Digital for Income Tax deadline from the 2026-27 to the 2028-29 tax year: the quarterly update deadlines (for both standard and calendar update periods), the tax return deadline, and the Self Assessment payment dates. Each date carries a GOV.UK source.

| File | What it is |
|---|---|
| [`deadlines.json`](deadlines.json) | All 24 dates with periods, who they apply to, notes and a source URL |
| [`deadlines.csv`](deadlines.csv) | The same as a spreadsheet |
| [`mtd-income-tax-deadlines.ics`](mtd-income-tax-deadlines.ics) | All-day calendar events for Google Calendar, Outlook or Apple Calendar |
| [`build.py`](build.py) | Regenerates the three files (Python 3, no dependencies) |

**Subscribe in your calendar app:** add a calendar "from URL" with
`https://raw.githubusercontent.com/Smallwright/mtd-quarterly-deadlines/main/mtd-income-tax-deadlines.ics`

## Quarterly update deadlines

The deadlines are the same whichever update periods you use. GOV.UK says: *"The deadlines for your quarterly updates are the same for both."*

| Quarter | Standard period | Calendar period | Deadline |
|---|---|---|---|
| Q1 | 6 Apr – 5 Jul | 1 Apr – 30 Jun | 7 August |
| Q2 | 6 Jul – 5 Oct | 1 Jul – 30 Sep | 7 November |
| Q3 | 6 Oct – 5 Jan | 1 Oct – 31 Dec | 7 February |
| Q4 | 6 Jan – 5 Apr | 1 Jan – 31 Mar | 7 May |

GOV.UK describes the periods as cumulative (Q2 covers 6 Apr to 5 Oct). The table shows the three months that each update adds. Standard periods are the default in software. Use calendar periods if your accounting period is 1 April to 31 March.

## Every date, 2026-27 to 2028-29

| Tax year | Q1 | Q2 | Q3 | Q4 | Tax return (online) |
|---|---|---|---|---|---|
| 2026-27 | Fri 7 Aug 2026 | Sat 7 Nov 2026 | Sun 7 Feb 2027 | Fri 7 May 2027 | Mon 31 Jan 2028 |
| 2027-28 | Sat 7 Aug 2027 | Sun 7 Nov 2027 | Mon 7 Feb 2028 | Sun 7 May 2028 | Wed 31 Jan 2029 |
| 2028-29 | Mon 7 Aug 2028 | Tue 7 Nov 2028 | Wed 7 Feb 2029 | Mon 7 May 2029 | Thu 31 Jan 2030 |

**Payments are unchanged by MTD.** For tax year 2026-27, payments on account are due 31 Jan 2027 and 31 Jul 2027, and the balancing payment is due 31 Jan 2028. Each later year follows the same pattern, one year on. All of these are in the files.

Several deadlines fall on a weekend. GOV.UK guidance doesn't say they move, and you can send an update "up to and including the day of the update deadline", so the files list the dates exactly as published, with the weekday, so you can plan to file before the weekend.

## Who has to use MTD for Income Tax, and when

The test is qualifying income: self-employment plus property income, **before expenses**.

| If your qualifying income was over… | in tax year | you must use MTD from |
|---|---|---|
| £50,000 | 2024-25 | 6 April 2026 |
| £30,000 | 2025-26 | 6 April 2027 |
| £20,000 | 2026-27 | 6 April 2028 |

Some income doesn't count towards qualifying income: your share of partnership profits, employment income, dividends, pensions, and income from REITs or PAIFs. For jointly owned property, only your share counts. The full rules are in GOV.UK's [qualifying income guidance](https://www.gov.uk/guidance/work-out-your-qualifying-income-for-making-tax-digital-for-income-tax).

## Penalties

- **2026-27:** "HMRC will not apply penalty points for late quarterly updates during the 2026 to 2027 tax year." Late tax returns still earn points.
- **From 2027-28:** each late quarterly update earns a penalty point, and "if you reach 4 points, you'll get a £200 penalty". After that, there's a further £200 for each missed deadline. You get only one point per deadline, even if you have several businesses. Late tax returns also earn points.
- **Volunteers:** late quarterly updates aren't penalised while you're volunteering. "Penalty points still apply for late tax returns. If you reach 2 points, you'll get a £200 penalty."

## Sources (checked 14 November 2026)

- [Send quarterly updates](https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/send-quarterly-updates) (GOV.UK, updated 16 Oct 2026): periods, deadlines, penalties.
- [Find out if and when you need to use MTD for Income Tax](https://www.gov.uk/guidance/find-out-if-and-when-you-need-to-use-making-tax-digital-for-income-tax) (GOV.UK): thresholds and start dates.
- [Work out your qualifying income](https://www.gov.uk/guidance/work-out-your-qualifying-income-for-making-tax-digital-for-income-tax) (GOV.UK, updated 11 Sep 2026).
- [Penalties for MTD for Income Tax](https://www.gov.uk/guidance/penalties-for-making-tax-digital-for-income-tax) (GOV.UK).
- [Self Assessment tax returns: deadlines](https://www.gov.uk/self-assessment-tax-returns/deadlines) (GOV.UK): the 31 January online return and payment deadline.
- [Payments on account](https://www.gov.uk/understand-self-assessment-bill/payments-on-account) (GOV.UK): the 31 January and 31 July dates.

This is a convenience copy of published dates, not tax advice. If GOV.UK changes, GOV.UK wins: please open an issue and we'll update the files.

## JSON shape

```json
{
  "id": "2026-27-Q3",
  "tax_year": "2026-27",
  "type": "quarterly_update",
  "quarter": 3,
  "deadline": "2027-02-07",
  "weekday": "Sunday",
  "title": "MTD quarterly update 2026-27 Q3 due",
  "standard_period_start": "2026-10-06", "standard_period_end": "2027-01-05",
  "calendar_period_start": "2026-10-01", "calendar_period_end": "2026-12-31",
  "who": "People in MTD for Income Tax that year: qualifying income over £50,000 in 2024-25",
  "note": "No penalty points for late quarterly updates in 2026-27 (HMRC).",
  "source": "https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/send-quarterly-updates"
}
```
`type` is `quarterly_update`, `tax_return` or `payment`.

---
Made by Smallwright (MIT licence). If you're a bookkeeper chasing clients for their records before each of these dates, [MTD Chase](https://mtd-chase.smallwright.com/) sends the reminders for you.
