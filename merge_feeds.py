import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEEDS = [
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCCRThPy0M9pfhk1Jhl5wV0w",  # 보험왕 초특급
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC1oBpjjwMp0WGBfdg-0a5qQ",  # 보험명의 정닥터
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCKlXPhUwfYFZ8S7y-wpwZ2w",  # 보험조각가
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC6wE7rHspfyVlE5CvXzsgvw",  # 김도형의 보험보상TV
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCvDigULicg0iGXgALkLzGZw",  # 금융상품연구소
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCzEDsOXNyRDe5Wxr8HnrhXA",  # 보험탈출구
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCZVkwvVRbMaNNPoLcCwWrjw",  # 보험e채널
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCn8SUGb1J3qIXpOKJAEjEkw",  # 팀보틀
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCa5I7YP-IxUIYqm3cIgIYGw",  # 보험인사이트
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCYK08O6Y5-tnpn8ngybZCoQ",  # 보험컴퍼니 (구 탑스터)
]

items = []
NS = {"atom": "http://www.w3.org/2005/Atom"}

for url in FEEDS:
    try:
        r = requests.get(url, timeout=10)
        root = ET.fromstring(r.content)
        for entry in root.findall("atom:entry", NS):
            title = entry.findtext("atom:title", "", NS)
            link_el = entry.find("atom:link", NS)
            link = link_el.get("href", "") if link_el is not None else ""
            updated = entry.findtext("atom:updated", "", NS)
            author = entry.findtext("atom:author/atom:name", "", NS)
            items.append({"title": title, "link": link, "updated": updated, "author": author})
    except Exception as e:
        print(f"Error: {url} - {e}")

items.sort(key=lambda x: x["updated"], reverse=True)
items = items[:50]

rss = '<?xml version="1.0" encoding="UTF-8"?>\n'
rss += '<rss version="2.0"><channel>\n'
rss += '<title>보험 유튜브 통합 피드</title>\n'
rss += '<link>https://github.com</link>\n'
rss += f'<description>Updated: {datetime.now(timezone.utc).isoformat()}</description>\n'

for i in items:
    rss += "<item>\n"
    rss += f"  <title><![CDATA[{i['title']}]]></title>\n"
    rss += f"  <link>{i['link']}</link>\n"
    rss += f"  <author>{i['author']}</author>\n"
    rss += f"  <pubDate>{i['updated']}</pubDate>\n"
    rss += "</item>\n"

rss += "</channel></rss>"

with open("docs/feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print("Done:", len(items), "items")
