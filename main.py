import requests
import os
import base64
import datetime
import json
from github import Github, GithubException
import re
import sys

MEDIUM_API = "https://api.rss2json.com/v1/api.json"
# MEDIUM_HANDLER = "@wathsara"
START_COMMENT = '<!--START_SECTION:medium-->'
END_COMMENT = '<!--END_SECTION:medium-->'
listReg = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"
repository = os.getenv('INPUT_REPOSITORY')
ghtoken = os.getenv('INPUT_GH_TOKEN')
MEDIUM_HANDLER = os.getenv("INPUT_MEDIUM_HANDLER")
DAYS = os.getenv("INPUT_DAYS")
start_day = datetime.datetime.today()
last_day = datetime.datetime.today()-datetime.timedelta(days=int(DAYS))
def this_month():
    '''Returns a month streak'''
    print("Month header created")
    return f"Month: {start_day.strftime('%d %B, %Y')} - {last_day.strftime('%d %B, %Y')}"

def print_output(title_list, header,links_list):
    stats = ""
    print(header)
    print("===" * 20)
    if(len(title_list)>0):
        for i in range(0,len(title_list)):
            stats +="""\n > :memo: {number}. ![{title}]("{link}")            
""".format(title=title_list[i], link=links_list[i],number=i+1)
            print("["+title_list[i]+"]("+links_list[i]+")")
    else:
        print("No blogs In this month")
    print("===" * 20)
    return stats

def fetch_titles(story_json):
    titles = list()
    for item in story_json["items"]:
        if(datetime.datetime.strptime(item["pubDate"], '%Y-%m-%d %H:%M:%S')>last_day):
            titles.append(item["title"])             
    return titles

def fetch_links(story_json):
    links = list()
    for item in story_json["items"]:
        if(datetime.datetime.strptime(item["pubDate"], '%Y-%m-%d %H:%M:%S')>last_day):
            links.append(item["link"])    
    return links

def decode_readme(data: str) -> str:
    '''Decode the contents of readme'''
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, 'utf-8')


def generate_new_readme(stats: str, readme: str) -> str:
    '''Generate a Readme.md'''
    stats_in_readme = f"{START_COMMENT}\n{stats}\n{END_COMMENT}"
    return re.sub(listReg, stats_in_readme, readme)

if __name__ == "__main__":
    github = Github(ghtoken)
    try:
        repo = github.get_repo(repository)
    except GithubException:
        print("Authentication Error")
        sys.exit(1)
    rss_uri = "https://medium.com/feed/{}".format(MEDIUM_HANDLER)
    response = requests.get(url=MEDIUM_API, params={"rss_url": rss_uri},)
    json_response = json.loads(response.text)
    returned_titles = fetch_titles(json_response)
    returned_links = fetch_links(json_response)
    blogs = print_output(returned_titles, "Titles", returned_links)
    print(this_month())
    contents = repo.get_readme()
    readme = decode_readme(contents.content)
    new_readme = generate_new_readme(stats=blogs, readme=readme)
    if new_readme != readme:
        repo.update_file(path=contents.path, message="updated the Readme",
                         content=new_readme, sha=contents.sha, branch='master')
