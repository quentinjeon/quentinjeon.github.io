---
permalink: /posts/
title: "전체 글"
layout: single
author_profile: true
description: "발행일 순으로 정렬한 전체 글 목록입니다. AX 설계 기록, 논문 스터디, 프로젝트 회고를 모두 포함합니다."
---

발행일 순으로 모아 본 전체 글입니다. 주제별로 보시려면 아래에서 고르세요.

[AX 인사이트 →](/ax/){: .btn .btn--inverse .btn--small}
[Scholar Labs →](/labs/){: .btn .btn--inverse .btn--small}
[프로젝트 →](/work/){: .btn .btn--inverse .btn--small}

{% assign posts = site.posts %}
{% assign years = posts | group_by_exp: "p", "p.date | date: '%Y'" %}

{% for year in years %}
## {{ year.name }} <span style="font-size:.55em;font-weight:400;color:#8b939c">{{ year.items.size }}편</span>

{% for post in year.items %}{% include post-row.html post=post %}{% endfor %}
{% endfor %}
