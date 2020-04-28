from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, redirect, request

app = Flask("NaverScrape")


@app.route("/")
def home():
    url = "https://comic.naver.com/webtoon/creation.nhn"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    db = []

    titleInput = input("제목?")

    result = soup.find("div", "all_list all_image").find_all("div", "section")

    for i in result:
        li = i.find("ul").find_all("li")
        for q in li:
            group = {}
            title = q.find("a")["title"]
            titleId = q.find("a")["href"].strip("/webtoon/list.nhn?titleId=")
            group = {"Title": title, "Id": titleId}
            db.append(group)

    try:
        outcome = next(
            (item for item in db if item["Title"] == titleInput), False)['Id']
        url = "https://comic.naver.com/webtoon/list.nhn?titleId="+outcome
        print(url)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        last = soup.find("table", "viewList").find_all("tr")
        lastPage = int(last[3].find("a")["onclick"][-5:-1].strip("'"))
        print(lastPage)
        comicUrl = "https://comic.naver.com/webtoon/detail.nhn?titleId=662774&no=183&weekday=wed"
        r = requests.get(comicUrl, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        pic = soup.find("div", "wt_viewer").find_all("img")
        # print(pic)
        pictures = []
        for i in pic:
            picture = i["src"]
            pictures.append(picture)

    except:
        print("Not Here!!")

    return render_template("home.html", pictures=pictures, count=lastPage)


app.run(host="0.0.0.0")
# https://comic.naver.com/
# /webtoon/detail.nhn?titleId=662774&no=183&weekday=wed
# wt_viewer
