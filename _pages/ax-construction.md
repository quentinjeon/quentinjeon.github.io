---
permalink: /ax/construction/
title: "AX Insight · 건설"
layout: single
author_profile: true
classes: wide
domain: construction
description: "건설사 업무를 Find에서 Act까지 잇는 AX 구조. 지식허브·법무·시공기준·고객여정·입찰 Risk 다섯 영역의 에이전트 설계 기록."
---

{% assign d = "" %}{% for x in site.data.domains.ax %}{% if x.slug == page.domain %}{% assign d = x %}{% endif %}{% endfor %}
<p style="color:#6b7280;font-size:.95em">{{ d.tagline }}</p>

{% assign posts = site.categories[page.domain] %}
{% if posts and posts.size > 0 %}{% for post in posts %}{% include post-row.html post=post %}{% endfor %}
{% else %}<p>아직 이 도메인에 발행한 글이 없습니다.</p>{% endif %}

<p style="margin-top:2em"><a href="/ax/" class="btn btn--inverse">← AX Insight 전체 도메인</a></p>
