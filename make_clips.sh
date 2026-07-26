#!/bin/bash
DUR=20
WIDTH=1280
SRC=~/siteline/output
OUT=~/siteline/clips
mkdir -p "$OUT"

CLIPS=(
  "spadinafortyork_vehicles:20"
  "spadinafortyork_people:20"
  "spadinabluejay_vehicles:15"
  "spadinabluejay_people:15"
  "kingportland_vehicles:20"
  "kingportland_people:20"
  "entrance1_vehicles:20"
  "entrance1_people:20"
  "spadina1_vehicles:20"
  "spadina1_people:20"
  "wellnoon_vehicles:20"
  "wellnoon_people:20"
)

echo "Making ${DUR}s proof clips -> $OUT"
echo "---------------------------------------------"

for entry in "${CLIPS[@]}"; do
  NAME="${entry%%:*}"
  START="${entry##*:}"
  IN="$SRC/$NAME.mp4"
  if [ ! -f "$IN" ]; then
    echo "  SKIP  $NAME  (not found)"
    continue
  fi
  ffmpeg -y -loglevel error -ss "$START" -i "$IN" -t "$DUR" \
    -vf "scale=${WIDTH}:-2" \
    -c:v libx264 -crf 28 -preset veryfast -pix_fmt yuv420p \
    -an -movflags +faststart "$OUT/$NAME.mp4"
  SIZE=$(du -h "$OUT/$NAME.mp4" | cut -f1)
  echo "  OK    $NAME.mp4  ($SIZE, from ${START}s)"
done

echo "---------------------------------------------"
du -sh "$OUT"
