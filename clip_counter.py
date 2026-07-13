#!/usr/bin/env python3
"""
SITELINE — Urban Object Counter (v2: live progress + fast-test option)

Modes:
  preview     save first frame with a coordinate grid
  flow        count objects crossing a line   (traffic, foot traffic)
  occupancy   count objects inside a region    (parking, crowds)

New in v2:
  --max-seconds N   only process the first N seconds (great for quick tests)
  live progress readout so you can SEE it working
"""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

CLASS_NAMES = {0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
VEHICLE_IDS = [1, 2, 3, 5, 7]
PERSON_IDS = [0]
ALL_IDS = VEHICLE_IDS + PERSON_IDS

OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)


def resolve_classes(group):
    return {"vehicles": VEHICLE_IDS, "people": PERSON_IDS, "all": ALL_IDS}[group]


def side_of_line(pt, p1, p2):
    return np.sign((p2[0] - p1[0]) * (pt[1] - p1[1]) - (p2[1] - p1[1]) * (pt[0] - p1[0]))


def video_fps(source):
    cap = cv2.VideoCapture(str(source))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.release()
    return fps


def cmd_preview(args):
    cap = cv2.VideoCapture(str(args.source))
    ok, frame = cap.read()
    cap.release()
    if not ok:
        raise SystemExit(f"Could not read a frame from {args.source}")
    h, w = frame.shape[:2]
    for x in range(0, w, 100):
        cv2.line(frame, (x, 0), (x, h), (0, 255, 0), 1)
        cv2.putText(frame, str(x), (x + 2, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    for y in range(0, h, 100):
        cv2.line(frame, (0, y), (w, y), (0, 255, 0), 1)
        cv2.putText(frame, str(y), (2, y + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    out = OUT_DIR / "preview_frame.jpg"
    cv2.imwrite(str(out), frame)
    print(f"Frame size: {w} x {h}")
    print(f"Saved {out}  — open it, read the x,y of your line/region points off the grid.")


def cmd_flow(args):
    line = ((args.line[0], args.line[1]), (args.line[2], args.line[3]))
    classes = resolve_classes(args.group)
    print(f"Loading model {args.model} …")
    model = YOLO(args.model)

    fps = video_fps(args.source)
    cap = cv2.VideoCapture(str(args.source))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    cap.release()
    limit_frames = int(args.max_seconds * fps) if args.max_seconds else total_frames
    print(f"Video: {total_frames} frames @ {fps:.0f}fps.  Processing "
          f"{'first ' + str(args.max_seconds) + 's' if args.max_seconds else 'all'} "
          f"(~{limit_frames} frames). Working…")

    last_side, counts = {}, defaultdict(int)
    conf_sum, conf_n, processed = 0.0, 0, 0
    writer = None

    results = model.track(
        source=str(args.source), persist=True, tracker="bytetrack.yaml",
        classes=classes, conf=args.conf, imgsz=args.imgsz, device=args.device,
        stream=True, verbose=False,
    )
    for r in results:
        processed += 1
        if args.max_seconds and processed > limit_frames:
            break

        if args.save_video:
            frame = r.plot()
            cv2.line(frame, line[0], line[1], (0, 0, 255), 3)
            if writer is None:
                h, w = frame.shape[:2]
                writer = cv2.VideoWriter(str(OUT_DIR / "flow_annotated.mp4"),
                                         cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
            writer.write(frame)

        if r.boxes is not None and r.boxes.id is not None:
            for xyxy, tid, cid, cf in zip(r.boxes.xyxy, r.boxes.id, r.boxes.cls, r.boxes.conf):
                tid, cid = int(tid), int(cid)
                conf_sum += float(cf); conf_n += 1
                cx = float((xyxy[0] + xyxy[2]) / 2); cy = float((xyxy[1] + xyxy[3]) / 2)
                now = side_of_line((cx, cy), line[0], line[1])
                prev = last_side.get(tid)
                last_side[tid] = now
                if prev is not None and prev != 0 and now != 0 and prev != now:
                    counts[CLASS_NAMES.get(cid, str(cid))] += 1

        if processed % 20 == 0:
            pct = f"{100*processed/limit_frames:.0f}%" if limit_frames else "?"
            print(f"\r  {pct}  ·  {processed} frames  ·  crossings so far: {sum(counts.values())}   ",
                  end="", flush=True)
    print()
    if writer:
        writer.release()

    total = sum(counts.values())
    avg_conf = (conf_sum / conf_n) if conf_n else 0.0
    with open(OUT_DIR / "flow_counts.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["class", "crossings"])
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            wr.writerow([k, v])
        wr.writerow(["TOTAL", total])
        wr.writerow(["avg_detection_confidence", round(avg_conf, 3)])

    print("\n=== FLOW RESULTS ===")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k:12s} {v}")
    print(f"  {'TOTAL':12s} {total}")
    print(f"\nAvg detection confidence: {avg_conf:.2f}  "
          f"({'usable' if avg_conf >= 0.5 else 'LOW — footage likely shot too high/oblique'})")
    print(f"CSV -> {OUT_DIR/'flow_counts.csv'}")


def cmd_occupancy(args):
    pts = args.region
    if len(pts) < 6 or len(pts) % 2 != 0:
        raise SystemExit("--region needs an even list of x y pairs, >= 3 points")
    region = np.array([[pts[i], pts[i + 1]] for i in range(0, len(pts), 2)], dtype=np.int32)
    classes = resolve_classes(args.group)
    print(f"Loading model {args.model} …")
    model = YOLO(args.model)

    fps = video_fps(args.source)
    sample_every = max(1, int(fps * args.sample_seconds))
    samples, conf_sum, conf_n, processed = [], 0.0, 0, 0
    limit_frames = int(args.max_seconds * fps) if args.max_seconds else None
    writer = None

    results = model.predict(
        source=str(args.source), classes=classes, conf=args.conf,
        imgsz=args.imgsz, device=args.device, stream=True, verbose=False,
    )
    for r in results:
        processed += 1
        if limit_frames and processed > limit_frames:
            break
        count = 0
        if r.boxes is not None:
            for xyxy, cf in zip(r.boxes.xyxy, r.boxes.conf):
                conf_sum += float(cf); conf_n += 1
                cx = float((xyxy[0] + xyxy[2]) / 2); cy = float((xyxy[1] + xyxy[3]) / 2)
                if cv2.pointPolygonTest(region, (cx, cy), False) >= 0:
                    count += 1
        if (processed - 1) % sample_every == 0:
            samples.append((round(processed / fps, 1), count))
        if args.save_video:
            frame = r.plot()
            cv2.polylines(frame, [region], True, (0, 0, 255), 3)
            cv2.putText(frame, f"in-region: {count}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            if writer is None:
                h, w = frame.shape[:2]
                writer = cv2.VideoWriter(str(OUT_DIR / "occupancy_annotated.mp4"),
                                         cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
            writer.write(frame)
        if processed % 20 == 0:
            print(f"\r  {processed} frames  ·  latest in-region: {count}   ", end="", flush=True)
    print()
    if writer:
        writer.release()

    vals = [c for _, c in samples] or [0]
    avg_conf = (conf_sum / conf_n) if conf_n else 0.0
    with open(OUT_DIR / "occupancy_samples.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["timestamp_s", "count_in_region"])
        wr.writerows(samples)
    print("\n=== OCCUPANCY RESULTS ===")
    print(f"  samples: {len(samples)}")
    print(f"  min / avg / max in region: {min(vals)} / {sum(vals)/len(vals):.1f} / {max(vals)}")
    print(f"\nAvg detection confidence: {avg_conf:.2f}")
    print(f"CSV -> {OUT_DIR/'occupancy_samples.csv'}")


def build_parser():
    p = argparse.ArgumentParser(description="SITELINE — Urban Object Counter (v2)")
    sub = p.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--source", required=True)
    common.add_argument("--model", default="yolo11m.pt")
    common.add_argument("--group", default="all", choices=["vehicles", "people", "all"])
    common.add_argument("--conf", type=float, default=0.25)
    common.add_argument("--imgsz", type=int, default=1280)
    common.add_argument("--device", default="mps")
    common.add_argument("--save-video", action="store_true")
    common.add_argument("--max-seconds", type=float, default=None,
                        help="only process the first N seconds (fast testing)")

    pv = sub.add_parser("preview")
    pv.add_argument("--source", required=True)
    pv.set_defaults(func=cmd_preview)

    fl = sub.add_parser("flow", parents=[common])
    fl.add_argument("--line", nargs=4, type=int, required=True, metavar=("x1", "y1", "x2", "y2"))
    fl.set_defaults(func=cmd_flow)

    oc = sub.add_parser("occupancy", parents=[common])
    oc.add_argument("--region", nargs="+", type=int, required=True)
    oc.add_argument("--sample-seconds", type=float, default=5.0)
    oc.set_defaults(func=cmd_occupancy)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
