from bs4 import BeautifulSoup
import datetime
import requests
import csv
import sys
import urllib
import time

def get_date(date, subdate=None):
    if subdate is not None:
        date = date - subdate
    return (str(date.month) + "m" + str(date.day) + "d")


def add_csv_rows(writer, category, keyword, date_from, date_to):
    keyword = urllib.parse.quote(keyword)
    r = requests.get("https://jmty.jp/all/" + category + "?keyword=" + keyword)
    # HTMLソースを取得
    soup = BeautifulSoup(r.text, "html")

    # ソース内の"li"をすべて取得
    lis = soup.find_all(class_="p-articles-list-item")

    # もし、更新日がdate_toであれば、その投稿のタイトル、URL、更新日を取得
    for li in lis:
        div = li.find("div", class_="p-item-additional-info").find("div", class_="u-margin-xs-b")
        post_date = div.text
        try:
            if date_to in post_date or date_from in post_date:
                h2 = li.find("h2", class_="p-item-title")
                title = h2.find("a")
                url = title.get("href")
                writer.writerow([title.text, url, post_date])

        except:
            print(li, "この要素はエラーです。")
            pass

def export_csv(args):
    # コマンド例： python zimoti_scraping.py 2(n日前から)
    from_days = 1 if len(args) < 2 else int(args[1])
    date_from = get_date(datetime.date.today(), datetime.timedelta(days=from_days))

    # 現在の日付を取得
    date_to = get_date(datetime.date.today())
    # csvをセット
    csv_path = 'csv/' + date_to + ".csv"
    categories = ["com", "coop"]
    # keywords = "プログラミング,Laravel,php,python,パソコン"
    keywords = "html,css,javascript,プログラミング,Laravel,php,python,PHP,Python"
    with open(csv_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["タイトル", "url", "更新日"])
        for category in categories:
            for keyword in keywords.split(","):
                add_csv_rows(writer, category, keyword, date_from, date_to)
                time.sleep(1)



