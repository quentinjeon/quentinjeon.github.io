---
layout: splash
permalink: /
title: "회사의 AX는 암묵지를 형식지로 바꾸는 것부터 시작합니다"
excerpt: "업무를 꺼내고, 현장을 이해해서 자연스럽게 **형식지화하는 일**.<br>AI를 우리 일에 녹이는 일을 전문으로 합니다."
description: "회사의 AX는 암묵지를 형식지로 바꾸는 것부터 시작합니다. 업무를 꺼내고 현장을 이해해 형식지화하고, AI를 실제 업무에 녹이는 일을 합니다."
header:
  overlay_color: "#12263f"
  actions:
    - label: "프로젝트 보기"
      url: "/work/"
feature_row:
  - image_path: /assets/images/work/haccp-01-main.jpg
    alt: "HACCP FLOW 생산일지 완성센터"
    title: "HACCP FLOW"
    excerpt: "식품 제조 현장의 **말과 클릭을 HACCP 공식 기록으로** 바꾸는 시스템. 빈칸 하나가 인증취소로 이어지는 환경에서, 시스템이 어느 칸이 왜 비었는지를 항상 알고 있게 만들었습니다."
    url: /work/haccp-flow/
    btn_label: "케이스 읽기"
    btn_class: "btn--primary"
  - image_path: /assets/images/work/margin-01-dashboard.jpg
    alt: "온라인몰 수익률 대시보드"
    title: "온라인몰 수익률 관리"
    excerpt: "**총매출은 다들 압니다. 이익을 모릅니다.** 엑셀 3장을 넣으면 채널별 수수료·원가·물류비를 반영한 기여이익과 적자 딜을 즉시 드러냅니다."
    url: /work/margin-system/
    btn_label: "케이스 읽기"
    btn_class: "btn--primary"
---

## 대표 케이스

{% include feature_row %}

---

## 반복되는 판단

프로젝트가 달라도 같은 판단이 반복됩니다. 이 6가지가 제 작업의 실제 내용입니다.

| | 원칙 |
|---|---|
| **P1** | LLM은 후보만 만들고, 판정은 코드가, **확정은 사람이** |
| **P2** | 빈칸은 "없는 행"이 아니라 **상태를 가진 행**이다 |
| **P3** | 원본은 불변, 정정은 **이력으로** 남는다 |
| **P4** | 상태 전이는 **단일 게이트웨이**를 통과한다 |
| **P5** | 해석하지 않고 **컴파일**한다 |
| **P6** | 기존 자산을 갈아엎지 않고 **Layer만 추가**한다 |

[설계 원칙 자세히 보기 →](/labs/#설계-원칙){: .btn .btn--inverse}

---

## 글

업무 구조를 시스템으로 옮기는 방법에 대해 씁니다.

{% assign recent = site.posts | slice: 0, 3 %}
<div class="grid__wrapper">
{% for post in recent %}
  {% include archive-single.html type="grid" %}
{% endfor %}
</div>

[전체 글 보기 →](/posts/){: .btn .btn--inverse}
