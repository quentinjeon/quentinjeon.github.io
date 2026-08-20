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

{% for d in site.data.domains.ax %}
{% assign posts = site.categories[d.slug] %}
## {{ d.icon }} {{ d.name }} <span style="font-size:.6em;font-weight:400;color:#8b939c">{{ posts.size | default: 0 }}편</span>

<p style="color:#6b7280;font-size:.9em;margin:-.4em 0 1em">{{ d.tagline }}</p>

{% for post in posts %}{% include post-row.html post=post %}{% endfor %}

<p style="margin:.9em 0 2em"><a href="/ax/{{ d.slug }}/" class="btn btn--inverse btn--small">{{ d.name }} 글 전체 보기 →</a></p>
{% endfor %}

---

초기 하드웨어 기록을 포함한 전체 목록은 [전체 글](/posts/)에서 볼 수 있습니다. [태그로 찾기 →](/tags/)
