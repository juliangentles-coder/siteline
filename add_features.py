#!/usr/bin/env python3
"""
add_features.py — adds three trust/conversion features to SITELINE's index.html:
  1. a "How it works" 3-step strip (capture -> analyze -> report)
  2. a "Download the sample report" link (put SITELINE_sample_report.pdf next to index.html)
  3. a "Privacy & legality" FAQ section, right before the footer

Idempotent: safe to run more than once, and safe to run whether or not
upgrade_ui.py / patch_site.py have already been run on this file.

Run:  python3 ~/siteline/add_features.py
Then: open ~/siteline/index.html
"""
from pathlib import Path

p = Path.home() / "siteline" / "index.html"
s = p.read_text()
done = []

# ---------------------------------------------------------------- 1. how it works + sample report link
block1 = """
  <!-- ===== HOW IT WORKS ===== -->
  <div class="shead"><h2>How it works</h2><span class="hint">three steps, one deliverable</span></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px;">
    <div style="background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:16px 18px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.15em;
        text-transform:uppercase;color:var(--amber);margin-bottom:8px;">01 · Capture</div>
      <div style="font-size:13px;color:#C6D2DB;line-height:1.65;">Aerial and rooftop footage of your
        site, framed specifically for measurement — not a flyover reel.</div>
    </div>
    <div style="background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:16px 18px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.15em;
        text-transform:uppercase;color:var(--teal);margin-bottom:8px;">02 · Analyze</div>
      <div style="font-size:13px;color:#C6D2DB;line-height:1.65;">Computer-vision detection tracks
        every vehicle and person frame-to-frame, counted once as it crosses a fixed line.</div>
    </div>
    <div style="background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:16px 18px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.15em;
        text-transform:uppercase;color:var(--amber);margin-bottom:8px;">03 · Report</div>
      <div style="font-size:13px;color:#C6D2DB;line-height:1.65;">A decision-ready PDF and this
        dashboard, with the annotated footage behind every number.</div>
    </div>
  </div>

  <div style="margin:0 0 40px;">
    <a href="SITELINE_sample_report.pdf" target="_blank" rel="noopener"
      style="display:inline-flex;align-items:center;gap:9px;background:var(--panel2);
      border:1px solid var(--rule);border-radius:8px;padding:10px 16px;text-decoration:none;
      color:var(--ink);font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.04em;">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
      </svg>
      Download the sample report (PDF)
    </a>
  </div>
"""
if 'HOW IT WORKS' not in s:
    s = s.replace('<div class="totals">', block1 + '\n  <div class="totals">', 1)
    done.append("how-it-works + sample report link")

# ---------------------------------------------------------------- 2. privacy & legality FAQ
block2 = """
  <!-- ===== PRIVACY & LEGALITY ===== -->
  <section class="method" style="margin-top:24px;">
    <h2>Privacy &amp; legality</h2>
    <ul>
      <li><b>No identification, ever.</b> Footage is framed and altitude-set for counting, not
        recognition — faces and plates are not resolvable in the source video, and only aggregate
        counts leave the pipeline.</li>
      <li><b>Public rights-of-way only.</b> Capture happens over public streets and from rooftop
        vantage points, not inside private units or through windows.</li>
      <li><b>Drone flights follow Transport Canada's RPAS rules</b> for the applicable operating
        category; rooftop-tripod holds require no flight at all.</li>
      <li><b>Your footage, on request.</b> The annotated clip behind every count is available to the
        client — nothing is packaged or resold without the site owner's knowledge.</li>
    </ul>
  </section>
"""
if 'PRIVACY &amp; LEGALITY' not in s and 'Privacy &amp; legality' not in s:
    s = s.replace('<footer>', block2 + '\n  <footer>', 1)
    done.append("privacy & legality FAQ")

p.write_text(s)
print("Applied:", ", ".join(done) if done else "nothing new (already added)")
print("Reminder: copy SITELINE_sample_report.pdf into ~/siteline/ so the download link works.")
