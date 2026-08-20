---
permalink: /work/agent-wallet/
title: "agent-wallet — 자율 사고·글쓰기 에이전트"
layout: single
author_profile: true
toc: true
toc_sticky: true
---

`Python 3.12` · 비공개

공시 클러스터링·분봉 임팩트 시그널을 받아 스스로 판단해 글을 쓰고 3채널에 발행하는 에이전트.

**문제**: LLM이 글을 쓰는 건 쉽다. 자율로 돌리면서 **사고를 안 내는 게** 어렵다.

- 프롬프트 1회 호출 → `observe → filter → think → draft → review → act → learn` **7단계 trace**. `trace_id` 하나로 글 한 편의 일대기를 재현
- 가드레일 3종: `kill_switch` · `publish_limit` · `balance_floor`
- self-review 5체크 + 1회 retry, `review_fail_streak 5회 시 자동 kill-switch`
- 트랜잭션은 SQLite, 의미 회상은 LanceDB 벡터 검색으로 저장소 역할 분리
- 테스트 96건, structlog JSON 로그 전 단계 표준화

---

[← 프로젝트 전체](/work/){: .btn .btn--inverse}
