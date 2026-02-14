import os
import argparse
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdown import markdown as md_to_html
import bleach

from app import create_app, db
from app.models import User, Post, Category, Tag
from app.models.post import now_utc


DEFAULT_URLS = [
    "https://flask.palletsprojects.com/en/latest/quickstart/",
    "https://flask.palletsprojects.com/en/latest/patterns/packages/",
    "https://docs.python.org/3/tutorial/introduction.html",
    "https://docs.python.org/3/tutorial/modules.html",
    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Introduction",
    "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction",
    "https://vuejs.org/guide/quick-start.html",
    "https://vuejs.org/guide/essentials/reactivity-fundamentals.html",
    "https://fastapi.tiangolo.com/tutorial/first-steps/",
    "https://www.sqlalchemy.org/library.html",
]


def get_or_create_author():
    u = User.query.filter_by(username="admin").first()
    if not u:
        u = User(username="admin", email="admin@example.com", is_admin=True)
        u.set_password("Admin@123456")
        db.session.add(u)
        db.session.commit()
    return u


def get_or_create_category(name="技术文档"):
    c = Category.query.filter_by(name=name).first()
    if not c:
        c = Category(name=name, description="外部技术文档收录")
        db.session.add(c)
        db.session.commit()
    return c


def get_or_create_tag(name="转载"):
    t = Tag.query.filter_by(name=name).first()
    if not t:
        t = Tag(name=name)
        db.session.add(t)
        db.session.commit()
    return t


def extract_title_and_content(url: str):
    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 (BlogCrawler)"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    title = None
    if soup.title and soup.title.text:
        title = soup.title.text.strip()
        for sep in ["|", "—", "-", "·", "·", "—"]:
            if sep in title:
                title = title.split(sep)[0].strip()
                break
    main = (
        soup.find("article")
        or soup.find("main")
        or soup.find("div", {"id": "content"})
        or soup.find("div", {"role": "main"})
        or soup.find("div", {"class": lambda c: c and "content" in c})
        or soup.body
    )
    paras = []
    for pre in main.find_all("pre"):
        code_text = pre.get_text("\n").strip()
        if code_text:
            paras.append(f"```\n{code_text}\n```")
        pre.decompose()
    for p in main.find_all(["p", "h2", "h3", "h4", "li"]):
        text = p.get_text(" ", strip=True)
        if text:
            if p.name.startswith("h"):
                level = int(p.name[1])
                level = min(max(level, 2), 4)
                paras.append("#" * level + " " + text)
            else:
                paras.append(text)
    content_md = "\n\n".join(paras).strip()
    host = urlparse(url).netloc
    src = f"\n\n> 来源：[{host}]({url})"
    content_md = (content_md + src).strip()
    allowed_tags = ['p', 'br', 'strong', 'em', 'h1', 'h2', 'h3', 'h4',
                    'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a']
    allowed_attrs = {'a': ['href', 'title']}
    content_html = bleach.clean(md_to_html(content_md, extensions=['extra', 'codehilite']),
                                tags=allowed_tags, attributes=allowed_attrs)
    return title or host, content_md, content_html


def create_post(author, category, tags, title, content_md, content_html, publish=True):
    p = Post(
        title=title,
        summary=content_md.split("\n\n")[0][:200],
        content=content_md,
        content_html=content_html,
        user_id=author.id,
        category_id=category.id,
        is_published=publish,
    )
    if publish:
        p.published_at = now_utc()
    db.session.add(p)
    db.session.flush()
    for t in tags:
        p.tags.append(t)
    db.session.commit()
    return p.id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--urls", nargs="*", default=None)
    args = parser.parse_args()

    app = create_app(os.getenv("FLASK_CONFIG", "development"))
    with app.app_context():
        author = get_or_create_author()
        category = get_or_create_category()
        tag_repost = get_or_create_tag("转载")
        urls = args.urls or DEFAULT_URLS
        created = 0
        for url in urls[: args.limit]:
            try:
                title, content_md, content_html = extract_title_and_content(url)
                if Post.query.filter_by(title=title).first():
                    continue
                pid = create_post(author, category, [tag_repost], title, content_md, content_html, publish=True)
                created += 1
                print(f"✅ created post {pid}: {title}")
            except Exception as e:
                print(f"⚠️  skip {url}: {e}")
        print(f"Done. created={created}")


if __name__ == "__main__":
    main()
