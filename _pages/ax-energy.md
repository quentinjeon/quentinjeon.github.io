---
permalink: /ax/energy/
title: "AX Insight · 에너지"
layout: single
author_profile: true
classes: wide
domain: energy
---

{% assign d = "" %}{% for x in site.data.domains.ax %}{% if x.slug == page.domain %}{% assign d = x %}{% endif %}{% endfor %}
<p style="color:#6b7280;font-size:.95em">{{ d.tagline }}</p>

{% assign posts = site.categories[page.domain] %}
{% if posts and posts.size > 0 %}{% for post in posts %}{% include post-row.html post=post %}{% endfor %}
{% else %}<p>아직 이 도메인에 발행한 글이 없습니다.</p>{% endif %}

<p style="margin-top:2em"><a href="/ax/" class="btn btn--inverse">← AX Insight 전체 도메인</a></p>
