---
permalink: /work/openclaw/
title: "OpenClaw — 멀티에이전트 자동매매"
layout: single
author_profile: true
toc: true
toc_sticky: true
---

[![OpenClaw 대시보드](/assets/images/cards/openclaw.jpg)](/assets/images/cards/openclaw.jpg)

`Python + Next.js` · [저장소](https://github.com/quentinjeon/openclaw-trade)

5개 전문 에이전트가 파이프라인으로 협력: `MarketAnalyzer → Strategy → RiskManager → Execution → Portfolio`

**문제**: 자동매매 봇은 **왜 그 주문을 냈는지 설명하지 못한다.**

- 단계별 산출물이 타입을 가짐 — `MarketSignal → TradingSignal → ApprovedOrder → TradeResult`
- `RiskManagerAgent`가 단일 게이트: 최대 포지션 크기·동시 포지션 수·일일 손실 한도·연속 손실 횟수
- WebSocket 실시간 대시보드로 에이전트 의사결정 로그 스트림 노출
- 페이퍼트레이딩 모드 우선

### 금융·투자 도구

| 프로젝트 | 한 줄 | 스택 |
|---|---|---|
| **DART 재무정보 분석** | DART API + 네이버 금융으로 3개년 시계열 재무비율(ROE·영업이익률·부채비율·PER) 자동 산출 | Python |

---

---

[← 프로젝트 전체](/work/){: .btn .btn--inverse}
