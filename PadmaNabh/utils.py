import json

import requests
from bs4 import BeautifulSoup

from pysondb import db


database = db.getDb("db.json")

url = "https://bb-api.bohubrihi.com/public/graphql"


def get_first_layer(id):
    response = requests.post(
        url,
        json={
            "operationName": "GetBBListLesson",
            "variables": {"module_id": f"{id}"},
            "query": 'query GetBBListLesson($module_id: String = "") {\n  listLesson(module_id: $module_id) {\n    batch_id\n    content_id\n    description\n    id\n    is_active\n    is_free\n    module_id\n    serial\n    title\n    type\n    exam {\n      id\n      title\n      type\n      __typename\n    }\n    assignment {\n      end_date\n      id\n      start_date\n      title\n      type\n      __typename\n    }\n    video {\n      id\n      playback_url\n      thumbnail_urls\n      title\n      type\n      __typename\n    }\n    __typename\n  }\n}',
        },
    )
    return response.json()


def getdata(slug):
    # full-stack-web-development-with-mern
    response = requests.get(f"https://bohubrihi.com/track/{slug}")
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    script_tag = soup.find("script", id="__NEXT_DATA__")

    script_content = json.dumps(json.loads(script_tag.text), indent=4)

    # print(script_content)
    content = json.loads(script_content)

    fullcourse = {
        "name": content.get("props")
        .get("pageProps")
        .get("courseDetails")
        .get("name_en"),
        "routine": content.get("props")
        .get("pageProps")
        .get("courseDetails")
        .get("routine_download_url"),
    }

    fullcourse["modules"] = {}

    modules = content.get("props").get("pageProps").get("courseDetails").get("modules")
    for module in modules:
        fullcourse["modules"][module.get("id")] = {
            "id": module.get("id"),
            "name": module.get("name_en"),
        }
        fraction = fullcourse["modules"][module.get("id")]["fraction"] = {}
        for category in module.get("children"):
            fraction[category.get("id")] = {
                "id": category.get("id"),
                "name": category.get("name_en"),
                "videos": {},
            }
            videos = fraction[category.get("id")]["videos"]
            for video in (
                get_first_layer(category.get("id")).get("data").get("listLesson")
            ):
                if video.get("video"):
                    videos[video.get("id")] = {
                        "name": video.get("title"),
                        "description": video.get("description"),
                        "playback_url": video.get("video").get("playback_url"),
                    }
    return {"slug": slug, "data": fullcourse}


def get_cached_data(slug):
    if database.getByQuery({"slug": slug}):
        return database.getByQuery({"slug": slug})
    else:
        print("hehe")
        database.add(getdata(slug))
        print("Cached Data")
        get_cached_data(slug)


#print(get_cached_data("full-stack-web-development"))
