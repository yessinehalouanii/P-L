# STEPS Performance Intelligence OS — Full-Stack Meeting Demo

A full-stack hospitality performance intelligence prototype tailored to STEPS Hospitality Consultants.

## What this version adds

- Real FastAPI backend + SQLite persistence.
- Data Center for 13 hotel data sources.
- CSV/XLSX uploads with automatic header mapping.
- Manual data entry for every source.
- P&L Intelligence with Actual vs Budget vs Prior Year, departmental profit, GOP and variance drivers.
- Revenue, Labour, Guest, Employee, Operations, Asset/Capital and Sales intelligence pages.
- Evidence-backed recommendation engine.
- Consultant approval workflow.
- SMART action register with owner, target, due date and guest/service guardrail.
- Mystery Shop / Operational Audit evidence workflow.
- Quick Step one-day diagnostic workspace.
- STEPS 8-Step Advisory map.
- Owner brief CSV export.

## Hotel data sources supported

1. P&L / Accounting
2. PMS
3. RMS / Revenue System
4. STR / CoStar
5. F&B POS
6. Payroll / Scheduling
7. HR System
8. Guest Feedback
9. Maintenance / CMMS
10. Utility / BMS
11. CRM / Sales
12. Website / GA4 / Booking Engine
13. STEPS Consultant / Mystery Shop

Every source has a field catalogue visible in the Data Center.

## Run on Windows

1. Extract the ZIP.
2. Double-click `start_windows.bat`.
3. Wait until the console says Uvicorn is running.
4. Open: http://127.0.0.1:8088

The first run installs four small Python packages: FastAPI, Uvicorn, python-multipart and openpyxl.

## Run manually

```bash
python -m pip install -r backend/requirements.txt
python run.py
```

Then open http://127.0.0.1:8088

## Best meeting flow

1. Executive Command — show one connected picture across profit, demand, labour and guest experience.
2. P&L Intelligence — show Actual/Budget/Prior Year, department profit and variance drivers.
3. Data Center — show that each hotel can upload exports from its existing systems rather than replacing them.
4. Labour Optimization — explain demand → staffing → hours → payroll → profitability with guest guardrails.
5. Operational Efficiency — explain how F&B combines P&L + POS + payroll; housekeeping combines PMS + payroll; engineering combines P&L + CMMS + utilities.
6. Mystery Shop — show qualitative STEPS evidence alongside the numeric KPIs.
7. Recommendations & Actions — show evidence → recommendation → consultant approval → SMART action.
8. Quick Step 360 — position it as the one-day diagnostic workflow.

## Important demo note

The included Harbour Crest Resort data is synthetic demonstration data. The architecture is designed for real hotel exports, but the prototype does not claim live integrations with OPERA, Mews, Cloudbeds, IDeaS, CoStar/STR, Simphony, ADP, UKG, GA4 or other commercial systems.
