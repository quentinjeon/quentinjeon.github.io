---
permalink: /ax/
title: "AX Insight"
excerpt: "도메인별로 정리한 AX 설계 노트. 챗봇을 만드는 이야기가 아니라, 업무 흐름을 Find에서 Act까지 잇는 구조에 대한 글입니다."
layout: single
author_profile: true
---

AX는 도메인마다 다르게 생겼습니다.
건설사의 "과거 판례를 찾아줘"와 커머스의 "이 리뷰에 답을 달아줘"는 같은 기술을 쓰지만 **전혀 다른 문제**입니다.

그래서 글을 도메인별로 나눠 정리합니다. 각 도메인에서 반복되는 질문과, 그 질문에 답하는 시스템 구조를 다룹니다.

[프로젝트에서 실제 구현 보기 →](/work/){: .btn .btn--inverse}

---

{% for d in site.data.domains.ax %}
{% assign posts = site.categories[d.slug] %}
## {{ d.icon }} {{ d.name }}

{{ d.tagline }}

{% if posts and posts.size > 0 %}<p><strong>{{ posts.size }}편</strong></p>

{% for post in posts %}
### [{{ post.title }}]({{ post.url }})

<p style="color:#79808a;font-size:.85em;margin:-.6em 0 .6em">{{ post.date | date: "%Y년 %m월 %d일" }}{% if post.tags.size > 0 %} · {% for t in post.tags limit:4 %}{{ t }}{% unless forloop.last %} · {% endunless %}{% endfor %}{% endif %}</p>

{{ post.excerpt | markdownify | strip_html | truncate: 180 }}

[읽기 →]({{ post.url }}){: .btn .btn--primary .btn--small}

{% endfor %}
{% endif %}

---
{% endfor %}

## 전체 글

도메인으로 나누기 전의 글과 초기 하드웨어 기록까지 포함한 전체 목록입니다.

[전체 글 보기 →](/posts/){: .btn .btn--inverse} [태그로 찾기 →](/tags/){: .btn .btn--inverse}
