#!/bin/sh
set -e

echo "Starting PilotEdge audio fetch"
python /app/fetch.py
echo "Fetch complete"

DAY_DIR=$(ls /work)
OUTPUT_BASE="/media/pe-audio/$DAY_DIR"

mkdir -p "$OUTPUT_BASE"

for CONTROLLER in ZLA Western; do
  SRC="/work/$DAY_DIR/$CONTROLLER"
  OUT="$OUTPUT_BASE/${CONTROLLER}.mp3"

  echo "Concatenating $CONTROLLER"

  ls "$SRC"/*.mp3 | sort |
    sed "s|^|file '|; s|$|'|" \
      >/tmp/concat.txt

  ffmpeg -f concat -safe 0 -i /tmp/concat.txt -c copy "$OUT"
done

echo "Job complete"
