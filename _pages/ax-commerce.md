---
permalink: /ax/commerce/
title: "AX Insight · 커머스·광고"
layout: single
author_profile: true
classes: wide
domain: commerce
description: "검색·쇼핑·피드·커뮤니티로 흩어진 고객 접점을 하나의 최적화 단위로 묶는 커머스·광고 AX 기록."
---

{% assign d = "" %}{% for x in site.data.domains.ax %}{% if x.slug == page.domain %}{% assign d = x %}{% endif %}{% endfor %}
<p style="color:#6b7280;font-size:.95em">{{ d.tagline }}</p>

{% assign posts = site.categories[page.domain] %}
{% if posts and posts.size > 0 %}{% for post in posts %}{% include post-row.html post=post %}{% endfor %}
{% else %}<p>아직 이 도메인에 발행한 글이 없습니다.</p>{% endif %}

<p style="margin-top:2em"><a href="/ax/" class="btn btn--inverse">← AX Insight 전체 도메인</a></p>
