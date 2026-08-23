---
permalink: /ax/
title: "AX Insight"
excerpt: "도메인별로 정리한 AX 설계 노트. 챗봇을 만드는 이야기가 아니라, 업무 흐름을 Find에서 Act까지 잇는 구조에 대한 글입니다."
layout: single
author_profile: true
classes: wide
---

AX는 도메인마다 다르게 생겼습니다. 건설사의 "과거 판례를 찾아줘"와 커머스의 "이 리뷰에 답을 달아줘"는
같은 기술을 쓰지만 **전혀 다른 문제**입니다. 그래서 도메인별로 나눠 정리합니다.

[프로젝트에서 실제 구현 보기 →](/work/){: .btn .btn--inverse .btn--small}
[전체 글 →](/posts/){: .btn .btn--inverse .btn--small}
[Threads 팔로우 →](https://www.threads.com/@cu.agent){: .btn .btn--primary .btn--small}

{% for d in site.data.domains.ax %}
{% assign posts = site.categories[d.slug] %}
## {{ d.icon }} {{ d.name }} <span style="font-size:.55em;font-weight:400;color:#8b939c">{{ posts.size | default: 0 }}편 · <a href="/ax/{{ d.slug }}/">모아보기</a></span>

<p style="color:#6b7280;font-size:14px;line-height:1.6;margin:-.6em 0 .4em">{{ d.tagline }}</p>

{% for post in posts %}{% include post-row.html post=post %}{% endfor %}
{% endfor %}
