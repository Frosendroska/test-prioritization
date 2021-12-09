import os

from dotenv import load_dotenv
import requests
from tqdm import tqdm

URL_BASE = "https://teamcity.jetbrains.com"
API_BASE = URL_BASE + "/app/rest/"
BUILDS_MULTIPLE_URL = API_BASE + "builds/multiple/"
headers = {"Accept": "application/json"}
load_dotenv()
headers["Authorization"] = "Bearer " + os.environ.get("TOKEN")

url = "https://teamcity.jetbrains.com/app/rest/buildTypes"
response = requests.get(url, headers=headers).json()
buildTypes = response.get("buildType")
counts = []
bad = 0

for buildType in tqdm(buildTypes):
    build_id = buildType["id"]
    url = BUILDS_MULTIPLE_URL + f"buildType:{build_id},count:-1,branch:(default:any)?fields=count"
    try:
        response = requests.get(url, headers=headers).json()
    except Exception:
        bad += 1
        continue
    count = response["count"]

    while "nextHref" in response:
        response = requests.get(URL_BASE + response["nextHref"], headers=headers).json()
        count += response["count"]

    counts.append((count, build_id))

print(bad)
print(sorted(counts, key=lambda cc: cc[0]))
