---
permalink: /labs/
title: "Scholar Labs"
excerpt: "논문을 읽고 시스템으로 옮기는 기록. 직접 만든 것과 외부 저작물을 섞지 않습니다."
layout: single
author_profile: true
classes: wide
---

논문을 읽고, 현장에서 원칙을 도출하고, 가르친 기록입니다.
**직접 만든 것과 외부 저작물을 섞지 않습니다** — <span class="badge badge--original">직접 제작</span> 은 제가 쓰거나 만든 것, <span class="badge badge--external">외부 논문</span> 은 제3자 저작물입니다.

[리딩 리스트 →](/labs/reading/){: .btn .btn--inverse .btn--small}
[설계 원칙 →](/labs/principles/){: .btn .btn--inverse .btn--small}
[교재 · 커리큘럼 →](/labs/teaching/){: .btn .btn--inverse .btn--small}
[Threads 팔로우 →](https://www.threads.com/@cu.agent){: .btn .btn--primary .btn--small}

{% assign labs = site.categories.labs | sort: "part" %}
## 📖 논문 스터디 <span style="font-size:.55em;font-weight:400;color:#8b939c">{{ labs.size }}편</span>

<p style="color:#6b7280;font-size:14px;line-height:1.6;margin:-.6em 0 .4em">원논문은 제3자 저작물이고, 아래 글은 그것을 이해하기 위해 제가 재구성한 학습 노트입니다.</p>

{% for post in labs %}{% include post-row.html post=post %}{% endfor %}

## 🔬 Original — 직접 제작

<p style="color:#6b7280;font-size:14px;line-height:1.6;margin:-.6em 0 .8em">논문이 아니라 현장에서 도출한 것들입니다.</p>

<div class="cardgrid">
  <article class="card">
    <a class="card__link" href="/labs/principles/">
      <div class="card__media card__media--text"><span>설계 원칙 P1~P6</span></div>
      <div class="card__body">
        <div class="card__meta"><span class="card__domain">🔬 직접 제작</span><span class="card__tag">#현장도출</span></div>
        <h3 class="card__title">설계 원칙 P1~P6</h3>
        <p class="card__desc">여러 도메인에서 시스템을 만들며 반복해서 내린 판단 6가지. LLM은 후보만 만들고, 판정은 코드가, 확정은 사람이.</p>
      </div>
    </a>
  </article>
  <article class="card">
    <a class="card__link" href="/labs/teaching/">
      <div class="card__media card__media--text"><span>교재 · 커리큘럼</span></div>
      <div class="card__body">
        <div class="card__meta"><span class="card__domain">🔬 직접 제작</span><span class="card__tag">#36챕터</span></div>
        <h3 class="card__title">교재 · 커리큘럼</h3>
        <p class="card__desc">AI 논문을 위한 확률·수학 인터랙티브 교재 36챕터와, 만드는 법을 가르친 바이브코딩 커리큘럼.</p>
      </div>
    </a>
  </article>
</div>

## 📚 Reading — 외부 논문

<p style="color:#6b7280;font-size:14px;line-height:1.6;margin:-.6em 0 .8em">지금 하는 작업과 직접 맞물리는 것만 골랐습니다. 전부 제3자 저작물이며 저자·발표연도를 함께 적었습니다.</p>

{% assign total = 0 %}{% for t in site.data.reading %}{% assign total = total | plus: t.papers.size %}{% endfor %}
<div class="cardgrid">
{% for t in site.data.reading %}
  <article class="card">
    <a class="card__link" href="/labs/reading/">
      <div class="card__body">
        <div class="card__meta"><span class="card__domain">📚 외부 논문</span><span class="card__tag">#{{ t.papers.size }}편</span></div>
        <h3 class="card__title">{{ t.track }}</h3>
        <p class="card__desc">{{ t.why }}</p>
      </div>
    </a>
  </article>
{% endfor %}
</div>

<p style="font-size:.85em;color:#8b939c">4트랙 {{ total }}편 — <a href="/labs/reading/">리딩 리스트 전체 보기 →</a></p>
