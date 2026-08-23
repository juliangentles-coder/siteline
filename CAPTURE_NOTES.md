# SITELINE — Rooftop footage assessment & capture spec

Analysed 23 Aug 2026. Three clips reviewed frame-by-frame at 2 fps.

---

## Verdict per clip

| Clip | Date | Roof-facing | Sharpness | Camera travel | Use for stills | Use for orthomosaic |
|---|---|---|---|---|---|---|
| `DJI_20251214…0040_D` (A) | 14 Dec 2025 | ~6 s of 13 s | crisp | 0.64 frame-widths | **No** — snow cover | **No** |
| `dji_fly_20260714_123240_0006` (B) | 14 Jul 2026 | ~94 s of 124 s | crisp | 1.84 frame-widths | **Yes — best clip** | **No** — hover |
| `dji_fly_20260714_123718_0007` (C, Stackt) | 14 Jul 2026 | ~82 s of 94 s | crisp | 4.57 frame-widths | **Yes** | Partial — single strip only |

### A — winter clip
Snow covers the membrane on every roof in frame. Roof condition work needs the surface visible;
snow hides ponding, blistering, seam separation, and granule loss — the whole point of the capture.
Also only ~6 s before the drone tilts up into a cinematic horizon shot. **Not usable. Do not send.**

### B — parking lot + adjacent roofs
The strongest imagery of the three. ~94 s of true nadir at roughly 2 cm/pixel ground sample
distance. At 100% crop you can resolve exhaust fan housings, roof drains, a skylight curb,
ductwork runs, membrane texture, and dark staining across the field. This is real inspection-grade
imagery.

The limitation: **62% of frames show under 2 px of motion.** It's a hover, not a survey. Total
ground travel is 1.84 frame-widths across 84 seconds. Excellent for stills, useless for 3D.

### C — Stackt Market
~82 s nadir, comparable sharpness, and genuine translation (4.57 frame-widths). Corrugated
container roofs, seams and rooftop conduit all resolve. This is the closest to a survey pass, but
it's a single strip — one line of travel with no adjacent parallel lines, so there's no sidelap.
You could reconstruct a narrow ribbon, not the whole site.

---

## What an orthomosaic actually requires

An orthomosaic is not a filter applied to footage. It is a 3D reconstruction: software finds the
same physical point across many photos taken from **different positions**, solves camera pose by
triangulation, builds a dense point cloud, meshes it, then reprojects imagery onto that surface so
every pixel is viewed as if from straight above. Only then are distances measurable anywhere in the
image — which is what makes area takeoffs possible.

Two consequences that kill the current footage:

1. **Parallax is mandatory.** A hover gives thousands of near-identical images from one point. No
   baseline, no triangulation, no reconstruction. B fails on this outright.
2. **Coverage must be two-dimensional.** A single flight line gives overlap along the strip but
   nothing sideways. C fails on this.

### Capture spec for the reshoot

| Parameter | Setting | Why |
|---|---|---|
| Capture mode | **Interval stills, not video** | Video frames are inter-frame compressed, rolling-shutter skewed, and carry no per-frame GPS EXIF. Photogrammetry software needs discrete full-res stills with EXIF. |
| Gimbal | −90° (true nadir), locked | Consistent geometry across the grid |
| Pattern | Lawnmower grid — parallel lines, then a second pass rotated 90° | Two-axis coverage; the cross-grid dramatically improves solve quality |
| Frontlap | 75–80% | Overlap along each line |
| Sidelap | 65–70% | Overlap between adjacent lines — the part you're currently missing |
| Altitude | Constant, ~30–40 m AGL | ~1–1.5 cm/px at 12 MP. Do not vary altitude mid-grid. |
| Interval | 2 s | At walking-pace flight this lands in the overlap window |
| Light | Overcast, or within 2 h of solar noon | Long shadows create false features and holes in the solve |
| Scale reference | Lay a tape or a 1 m marked target on the roof, photograph it in the grid | **Critical.** Sub-250 g airframes have no RTK; GPS is ±1–3 m. Without a measured ground distance your areas are unscaled and worthless for costing. |
| Obliques | One orbit at 45° after the nadir grid | Captures parapets and vertical faces the nadir grid misses |

A roof of Stackt's footprint is roughly 15–25 minutes of flying under this spec. Budget two
batteries.

### Software

- **WebODM / OpenDroneMap** — free, self-hosted, handles the full pipeline through to GeoTIFF
  orthomosaic and DSM. Start here.
- **Pix4Dmapper / DroneDeploy** — paid, faster, better reporting. Worth it once billing.

Area takeoff comes after: load the GeoTIFF into QGIS (free), scale against the ground reference,
draw polygons per roof section, read areas off the attribute table.

---

## What is sendable today

The annotated still (`SAMPLE_roof_capture.jpg`) from clip B. It is honest, it is real work, and it
demonstrates resolution — which is the only question an engineer actually has about a new capture
vendor.

**Do not offer orthomosaics or area takeoffs until one has been produced end to end.** Sell what
exists: nadir stills at ~2 cm/px, same-week turnaround. Add measured areas to the pitch once the
grid has been flown and the workflow proven on a building you have permission for.

---

## Scope discipline

Every deliverable carries: *asset locations and imagery only — no condition rating, remaining
service life, or engineering opinion.* Reserve fund studies and building condition assessments in
Ontario must be prepared by a qualified person under O. Reg. 48/01. SITELINE supplies imagery to
that person; it does not substitute for them.
