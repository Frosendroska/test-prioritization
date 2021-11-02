import json
import requests
import os
from dotenv import load_dotenv
from shutil import rmtree
from pathlib import Path

URL_BASE = "https://teamcity.jetbrains.com"
API_BASE = URL_BASE + "/app/rest/"
BUILDS_URL = API_BASE + "builds/"
TEST_OCCURRENCES_URL = API_BASE + "testOccurrences/"
BUILDS_MULTIPLE_URL = BUILDS_URL + "multiple/"
headers = {"Accept": "application/json"}


def load_token():
    load_dotenv()
    headers["Authorization"] = "Bearer " + os.environ.get("TOKEN")


def pretty_print_json(obj):
    print(json.dumps(obj, indent=2))


def clear_all_data():
    for file in os.listdir("data/"):
        rmtree("data/" + file)


def get_testOccurrences(build_id):
    locator = "?locator=build:(id:" + str(build_id) + ")"
    url = TEST_OCCURRENCES_URL + locator
    response = requests.get(url, headers=headers).json()
    testOccurrences = response.get("testOccurrence")
    if testOccurrences is None:
        return None

    while "nextHref" in response:
        response = requests.get(URL_BASE + response["nextHref"], headers=headers).json()
        testOccurrences += response.get("testOccurrence")

    return testOccurrences


def get_build(build_id):
    locator = "id:" + str(build_id)
    url = BUILDS_URL + locator
    return requests.get(url, headers=headers).json()


def get_build_list(project, all_branches=False):
    locator = ["buildType:" + project]
    if all_branches:
        locator.append("branch:(default:any)")

    url = BUILDS_MULTIPLE_URL + ",".join(locator)
    return requests.get(url, headers=headers).json()


def write_json_to_file(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_data_from_project(project, all_branches=False):
    project_dir = "data/" + project + "/"
    builds_dir = project_dir + "builds/"
    tests_dir = project_dir + "testOccurrences/"
    Path(builds_dir).mkdir(parents=True, exist_ok=True)
    Path(tests_dir).mkdir(parents=True, exist_ok=True)

    builds = get_build_list(project, all_branches)
    write_json_to_file(builds, project_dir + "builds_info.json")
    for build in builds["build"]:
        write_json_to_file(get_build(build["id"]), builds_dir + str(build["id"]) + ".json")
        write_json_to_file(get_testOccurrences(build["id"]), tests_dir + str(build["id"]) + ".json")


def main():
    load_token()
    # clear_all_data()
    projects = ["KotlinTools_Ktor_BuildGradle"]
    for project in projects:
        save_data_from_project(project)


if __name__ == "__main__":
    main()
