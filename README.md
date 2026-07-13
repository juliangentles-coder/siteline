# SITELINE

**Aerial site intelligence for Toronto.** Capture footage from above → software counts what's in it → a branded dashboard + report turns the counts into decisions a client pays for.

This README is the map. Open this first; everything else slots underneath it.

---

## The one-sentence business
Film from above → count → package → sell. Four steps, one company.

## What lives where

```
siteline/
├── README.md                  ← you are here (the map)
├── engine/
│   └── pipeline_a_counter.py  ← the counter. You RUN it, never edit it.
├── dashboard/
│   └── index.html             ← the client-facing dashboard (your premium layer)
├── report/
│   └── well_report_template.md
├── site/
│   └── carrd_copy.md          ← public landing page copy
├── footage/                   ← clips go here (NOT pushed to GitHub — too big)
└── output/                    ← CSVs the engine writes (auto-created)
```

Only ONE file is code (`engine/pipeline_a_counter.py`). The rest are documents and one webpage. You do not need to know Python — you copy-paste commands.

---

## Execution path — two milestones

### Milestone 1 — Prove the loop with footage you ALREADY have
Goal: watch real numbers travel from clip → CSV → dashboard. This is the moment the whole thing becomes real.

1. Put a clip from your **Downtown Toronto** folder in `footage/`.
2. Run the engine (see `engine/` guide): `preview`, then `flow` on a street.
3. It writes `output/flow_counts.csv` and prints an avg-confidence read.
4. The dashboard gets wired to that CSV → first real end-to-end deliverable.

✅ Done when: the dashboard shows numbers that came out of your own footage.

### Milestone 2 — The flagship
Goal: a real, sellable product for one site.

1. Shoot **The Well** properly (three near-nadir holds — see the execution guide).
2. Run the engine on each hold → real counts.
3. Fill `report/` + the dashboard → branded PDF **and** a live link.
4. Pitch it: developer/leasing, retail brokers, solar installers.

✅ Done when: you have one link + one PDF you can put in front of a buyer.

---

## Two upgrades in flight (both need Milestone-1 numbers first)
- **Better video out of the engine** — annotated export with live tally + trajectory trails (the DataFromSky look) on real footage.
- **Dashboard wired to real counts** — reads `output/*.csv` automatically so each site is a 5-minute generate, not a rebuild.

Neither is speculative — both plug into the CSV that Milestone 1 produces.

---

## Make it live
```bash
cd siteline
git init && git add . && git commit -m "SITELINE home"
# create the empty repo on github.com first, then:
git remote add origin https://github.com/juliangentles-coder/siteline.git
git push -u origin main
```
Then deploy `dashboard/` to **GitHub Pages** (free) or **Render** (you already use it) → that URL is the live link you send clients.

> Keep `footage/` out of git — add a `.gitignore` line for `footage/` and `output/`.

---

## Your next action (15 minutes)
Run the engine on ONE Downtown Toronto clip. That's it. Everything downstream keys off seeing the first real count appear.
