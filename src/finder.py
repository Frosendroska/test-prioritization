import json
import os

from dotenv import load_dotenv
import requests

URL_BASE = "https://teamcity.jetbrains.com"
headers = {"Accept": "application/json"}
load_dotenv()
headers["Authorization"] = "Bearer " + os.environ.get("TOKEN")


def pretty_print_json(obj):
    print(json.dumps(obj, indent=2))


url = "https://teamcity.jetbrains.com/app/rest/buildTypes"
response = requests.get(url, headers=headers).json()
buildTypes = response.get("buildType")
counts = []
bad = 0

for buildType in buildTypes:
    build_id = buildType["id"]
    url = "https://teamcity.jetbrains.com/app/rest/builds?locator=buildType:" + build_id
    url += "&fields=count,nextHref"
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
