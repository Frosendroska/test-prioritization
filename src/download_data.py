import json
import os
import time
from tqdm import tqdm
from pathlib import Path

from dotenv import load_dotenv
import requests

DATA_DIRECTORY = Path("..") / Path("data")
URL_BASE = "https://teamcity.jetbrains.com"
API_BASE = URL_BASE + "/app/rest/"
BUILDS_URL = API_BASE + "builds/"
TEST_OCCURRENCES_URL = API_BASE + "testOccurrences/"
BUILDS_MULTIPLE_URL = BUILDS_URL + "multiple/"
headers = {"Accept": "application/json"}


def load_token():
    load_dotenv()
    if os.environ.get("TOKEN") is None:
        raise KeyError("TOKEN environment variable is not exist")
    headers["Authorization"] = "Bearer " + os.environ.get("TOKEN")


def pretty_print_json(obj):
    print(json.dumps(obj, indent=2))


def get_test_occurrences(build_id):
    locator = f"?locator=count:-1,build:(id:{build_id})"
    tests_fields = "&fields=testOccurrence(name,status),nextHref"
    url = TEST_OCCURRENCES_URL + locator + tests_fields

    response = requests.get(url, headers=headers).json()
    testOccurrences = response["testOccurrence"]
    if testOccurrences is None:
        return None

    while "nextHref" in response:
        response = requests.get(URL_BASE + response["nextHref"], headers=headers).json()
        testOccurrences += response["testOccurrence"]

    return testOccurrences


def get_build(build_id):
    locator = f"id:{build_id}"
    build_fields = "?fields=id,number,branchName,status"

    url = BUILDS_URL + locator + build_fields
    return requests.get(url, headers=headers).json()


def get_build_ids(project, all_branches=False):
    locator = f"count:-1,buildType:{project}"
    if all_branches:
        locator += ",branch:(default:any)"

    info_fields = "?fields=build(id),nextHref"
    url = BUILDS_MULTIPLE_URL + locator + info_fields

    response = requests.get(url, headers=headers).json()
    build_ids = response["build"]
    while "nextHref" in response:
        response = requests.get(URL_BASE + response["nextHref"], headers=headers).json()
        build_ids += response["build"]

    return list(map(lambda b: b["id"], build_ids))


def write_json_to_file(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_data_from_project(project, max_builds=None, all_branches=False):
    project_dir = DATA_DIRECTORY / Path(f"{project}")
    builds_dir = project_dir / "builds"
    tests_dir = project_dir / "testOccurrences"
    builds_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)

    build_ids = get_build_ids(project, all_branches)
    if max_builds is not None:
        build_ids = build_ids[:max_builds]

    write_json_to_file(build_ids, project_dir / "builds_info.json")
    for build_id in tqdm(build_ids):
        write_json_to_file(get_build(build_id), builds_dir / f"{build_id}.json")
        write_json_to_file(get_test_occurrences(build_id), tests_dir / f"{build_id}.json")


def main():
    load_token()
    projects = []
    for project in projects:
        print(project + " in progress...")
        start_time = time.time()
        save_data_from_project(project)
        print(project + " done in %.2f seconds." % (time.time() - start_time))


if __name__ == "__main__":
    main()
