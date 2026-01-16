import requests
import time
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

REQUEST_DELAY = 0.3

HEADERS = {
    "User-Agent": "pilotedge-audio-fetcher/1.0 (personal archival use)"
}

pt = ZoneInfo("America/Los_Angeles")
now_pt = datetime.now(pt)
target_date = now_pt - timedelta(days=1)
year = target_date.year
month = target_date.month
day = target_date.day

controllers = {
    "ZLA": 17510,
    "Western": 14010,
}

out_dir_base = Path(f"/media/pe-audio/{year}_{month:02d}_{day:02d}")

def main():
    out_dir_base.mkdir(parents=True, exist_ok=True)

    for controller_id in controllers:
        for hour in range(7, 24):

            url = (
                f"https://audio.pilotedge.net/"
                f"{year}/{month}/"
                f"{year}-{month}-{day}_{hour}_{controllers[controller_id]}.mp3"
            )

            download(url, controller_id, hour)


def download(url: str, controller_id: str, hour: int):
    out_file = out_dir_base / controller_id / f"{year}-{month:02d}-{day:02d}-{hour:02d}.mp3"

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)

        if r.status_code == 200:
            out_file.parent.mkdir(parents=True, exist_ok=True)

            with open(out_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        elif r.status_code == 404:
            print(f"File not found: {url}")

        else:
            print(f"{r.status_code}: {url}")

    except requests.RequestException as e:
        print(f"Error: {e}")

    finally: 
        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    main()
