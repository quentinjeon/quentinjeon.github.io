---
permalink: /labs/reading/
title: "리딩 리스트 — 외부 논문"
excerpt: "에이전트·RAG·평가·거버넌스 4트랙 16편. 전부 제3자 저작물이며 저자·발표연도를 함께 적었습니다."
layout: single
author_profile: true
toc: true
toc_sticky: true
toc_label: "트랙"
---

<span class="badge badge--external">외부 논문</span> **아래는 전부 제3자 저작물입니다.** 제가 쓴 글이 아니며, 지금 하는 작업과 직접 맞물리는 것만 골랐습니다. 각 항목에 저자·발표연도를 함께 적었습니다.

{% for t in site.data.reading %}
## {{ t.track }}

<p style="color:#6b7280;font-size:.9em;margin:-.3em 0 1.1em">{{ t.why }}</p>

{% for p in t.papers %}<div class="readitem">
  <div class="readitem__title"><a href="https://www.semanticscholar.org/search?q={{ p.title | uri_escape }}" target="_blank" rel="noopener">{{ p.title }}</a> <span class="badge badge--external">외부 논문</span></div>
  <div class="readitem__authors">{{ p.authors }} · {{ p.year }}</div>
  <div class="readitem__why">{{ p.note }}</div>
</div>
{% endfor %}
{% endfor %}

<p style="font-size:.85em;color:#8b939c">링크는 제목 검색으로 연결됩니다. 식별자 오기입으로 다른 논문을 가리키는 일을 막기 위한 선택입니다.</p>

---

[← Scholar Labs](/labs/){: .btn .btn--inverse}
