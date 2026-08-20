---
permalink: /work/
title: "프로젝트"
excerpt: "식품 제조 · 커머스 · 금융·투자 · 공공 도메인에서 만든 운영 시스템과 AI 에이전트."
layout: single
author_profile: true
classes: wide
---

도메인은 식품 제조 · 커머스 · 금융·투자 · 공공으로 다르지만, 관통하는 작업은 하나입니다.
**사람이 규칙을 머릿속에 들고 하던 업무를, 시스템이 규칙을 들고 있는 구조로 옮기는 것.**

[도메인별 AX 설계 노트 →](/ax/){: .btn .btn--inverse} [설계 원칙 6가지 →](/labs/#설계-원칙){: .btn .btn--inverse}

{% for d in site.data.domains.work %}
{% assign items = site.data.projects | where: "domain", d.slug %}
{% if items.size > 0 %}
## {{ d.icon }} {{ d.name }}

{% include project-cards.html items=items %}
{% endif %}
{% endfor %}

---

# 도구 · 실험

한 번에 한 문제만 푸는 작은 도구들입니다.

## 커머스

| 프로젝트 | 한 줄 | 스택 |
|---|---|---|
| **Banafit AI Studio** | 패션 이커머스 이미지 워크플로우. 업로드 → 조건 → 프롬프트 레이어 스택 → 배치 생성 → 반복 정제 **6단계 상태 머신** | Gemini 2.5 Flash Image |
| **DeepRe** | 고객 리뷰에 3가지 스타일(감사·정중·문제해결) 답변 자동 생성. 웹훅 URL을 화면에서 실시간 변경 | Next.js 14 + n8n |
| **쿠팡 크롤링 시스템** | 랜덤 간격(균등/정규/지수 분포) + 인간 행동 시뮬레이션 + 워커 풀 + 실패 자동 복구 | Node.js + Chrome Extension |
| **스마트스토어 AI 스크래퍼** | AI 에이전트가 브라우저를 직접 제어해 동적 페이지 스크래핑 | browser-use |

## 금융·투자

| 프로젝트 | 한 줄 | 스택 |
|---|---|---|
| **DART 재무정보 분석** | DART API + 네이버 금융으로 3개년 시계열 재무비율(ROE·영업이익률·부채비율·PER) 자동 산출 | Python |

## 도메인 공통

| 프로젝트 | 한 줄 | 스택 |
|---|---|---|
| **promptfoo 평가 프로토타입** | CSV 업로드 → 프롬프트 평가 → 결과 다운로드를 30분 내에. 의도 분류 11개 카테고리에서 모델 성능 비교 | FastAPI + Promptfoo CLI |
| **LangChain RAG 챗봇** | PDF 업로드 → Pinecone 벡터 검색 → 응답. MongoDB 세션 관리, Docker Compose 배포 | Next.js + FastAPI |
| **심층 웹 리서치 보고서 생성기** | Firecrawl 웹 수집 + PDF/DOCX 업로드 → 보고서 → DOCX/PDF 출력 | Streamlit |
| **Gemini Live Talking Head** | 사진 업로드 → 립싱크 아바타 + 실시간 양방향 음성 대화 + 라이브 전사 | Gemini Live API |
| **AI Mindful Assistant** | 음성 우선 명상 코치. 감정 점수(1~10) 추적 + 시계열 리포트 | React 19 |
| **Audio → Script** | 영어 학습 오디오를 Whisper로 전사. 모델 5종 크기별 정확도/속도 트레이드오프 정리 | Streamlit + Whisper |
| **Duplicate Image Finder** | 해시 기반 정확 중복 + ViT 기반 유사 중복(임계값 조절) + 차이점 설명 | Streamlit + ViT |

---

교재·커리큘럼 등 가르친 기록은 [Scholar Labs](/labs/)로 옮겼습니다.
