import re
from pathlib import Path

p = Path.home() / "siteline" / "index.html"
s = p.read_text()
done = []

# ---------- type scale + breathing room ----------
if 'UI UPGRADE OVERRIDES' not in s:
    css = """
  /* ===== UI UPGRADE OVERRIDES ===== */
  .wrap{max-width:1080px;padding:44px 24px 88px}
  section, .profile, .method{margin-bottom:64px !important}
  .shead{margin-bottom:10px}
  .shead h2{font-size:13px;letter-spacing:.16em;color:var(--dim);font-weight:600}
  .sub{font-size:14px;line-height:1.65;margin-bottom:28px;color:#93A0AC}
  .site{padding:26px !important;margin-bottom:20px !important;gap:26px !important;border-radius:14px}
  .sitehead{margin-bottom:20px;padding-bottom:16px}
  .sitehead h3{font-size:19px}
  .metrics{gap:24px}
  .lead{font-size:15px;line-height:1.7;max-width:none}
  .totals{margin-bottom:56px;border-radius:14px}
  .tot{padding:20px 22px}
  .profile{padding:28px 26px;border-radius:14px}
  .prow{margin-bottom:20px}
  .method{padding:30px 28px;border-radius:14px}
  .raw{font-size:18px}
  .cap,.classes,.when,.conf{font-size:10px}
  @media (max-width:760px){.wrap{padding:28px 16px 60px} .site{padding:18px !important}}
"""
    s = s.replace("</style>", css + "\n</style>", 1)
    done.append("type scale + whitespace")

# ---------- use-case band ----------
band = """
  <!-- ===== USE-CASE BAND ===== -->
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);
    border:1px solid var(--rule);border-radius:14px;overflow:hidden;margin:8px 0 56px;">
    <div style="background:var(--panel);padding:22px 20px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.16em;
        text-transform:uppercase;color:var(--amber);margin-bottom:9px;">For leasing brokers</div>
      <div style="font-size:13.5px;color:#C6D2DB;line-height:1.6;">Hard footfall and vehicle
        numbers to market a vacant unit and close faster.</div>
    </div>
    <div style="background:var(--panel);padding:22px 20px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.16em;
        text-transform:uppercase;color:var(--teal);margin-bottom:9px;">For developers</div>
      <div style="font-size:13.5px;color:#C6D2DB;line-height:1.6;">Ground-truth traffic on a site
        before you commit &mdash; measured, not modelled.</div>
    </div>
    <div style="background:var(--panel);padding:22px 20px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.16em;
        text-transform:uppercase;color:var(--amber);margin-bottom:9px;">For retailers</div>
      <div style="font-size:13.5px;color:#C6D2DB;line-height:1.6;">Know how busy a corner really is
        at the hours that matter, before you sign.</div>
    </div>
  </div>
"""
if 'USE-CASE BAND' not in s:
    s = s.replace('<div class="totals">', band + '\n  <div class="totals">', 1)
    done.append("use-case band")

# ---------- large hero clip ----------
hero = """
  <!-- ===== HERO ===== -->
  <div style="margin:30px 0 40px;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:27px;line-height:1.25;
      font-weight:600;color:var(--ink);max-width:18ch;margin-bottom:22px;">
      Watch the count happen.</div>
    <div style="border:1px solid var(--rule);border-radius:14px;overflow:hidden;background:#000;
      position:relative;">
      <video autoplay muted loop playsinline preload="metadata"
        style="display:block;width:100%;max-height:440px;object-fit:cover;">
        <source src="clips/kingportland_people.mp4" type="video/mp4">
      </video>
      <div style="position:absolute;left:16px;bottom:14px;background:rgba(11,15,20,.74);
        border:1px solid var(--rule);border-radius:7px;padding:8px 13px;
        font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.05em;color:var(--ink);">
        <span style="color:var(--teal)">119 people</span> counted &middot; King &amp; Portland &middot; 3.2 min
      </div>
    </div>
  </div>
"""
if 'Watch the count happen' not in s:
    s = re.sub(r'<div style="margin:26px 0 4px;border:1px solid var\(--rule\);border-radius:10px;overflow:hidden;background:#000;position:relative;">.*?</div>\s*</div>',
               '', s, count=1, flags=re.DOTALL)
    s = s.replace('</header>', '</header>\n' + hero, 1)
    done.append("large hero clip")

p.write_text(s)
print("Applied:", ", ".join(done) if done else "nothing new (already upgraded)")
