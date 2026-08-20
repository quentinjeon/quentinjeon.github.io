---
permalink: /work/graphrag/
title: "GraphRAG 워크플로우"
layout: single
author_profile: true
toc: true
toc_sticky: true
---

`Node.js + Airflow` · [저장소](https://github.com/quentinjeon/dag.graph.rag.airflow)

Weaviate(벡터) + Neo4j(그래프)를 결합하고 Airflow DAG로 자동화한 질의응답 파이프라인.

**문제**: 순수 벡터 RAG는 "관련 문서"는 찾지만 **"개념 간 관계"는 못 찾는다.**

벡터 검색 + 질문에서 엔티티 추출 + Neo4j 관계 탐색 → 통합 컨텍스트 → 응답 생성. 응답에 `type: vector` / `type: graph`로 **소스를 구분해 반환**. 6단계 Airflow DAG로 재현 가능하게 스케줄링.

### 공통 도구 · 실험

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

---

[← 프로젝트 전체](/work/){: .btn .btn--inverse}
