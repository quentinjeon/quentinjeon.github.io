---
layout: single
title: "에이전트는 어느 수준에서 행동해야 하는가 (4/4) — 구현과 검증"
excerpt: "Typed Handoff로 계약을 넘기고 Compiler·Router·Runtime·Verifier를 연결한 뒤, MVP와 시뮬레이터·벤치마크·통계까지 실험 패키지로 마무리한다."
series: agent-level-20steps
part: 4
categories:
  - labs
tags:
  - Agent 학습 로드맵
  - Typed Handoff
  - MVP
  - Benchmark
  - Evaluation
  - Experiment Design
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/agent-level-p4.jpg
---

{% include series-nav.html %}

> **16~20단계 · 구현과 검증**
> 이 구간의 질문: **정책을 보존하며 구현하고 실험으로 검증할 수 있는가**

[1편에서](/labs/agent-level-problem-and-foundations/) 행동 수준을 왜 따로 골라야 하는지 정리했습니다. 이번 편은 그다음 구간입니다.

---

## 16단계. Typed Handoff와 전환 계약 구현하기

[![16단계. Typed Handoff와 전환 계약 구현하기](/assets/images/agent-level-step-16-typed-handoff-contract.png)](/assets/images/agent-level-step-16-typed-handoff-contract.png)
*16단계. Typed Handoff와 전환 계약 구현하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

Skill·Delegation·Human처럼 실행 경계가 바뀌면 자연어 한 문장 대신 Governance Transition Contract를 전달한다.

$$
\Gamma_\omega=\langle G_\omega,C_\omega,A_\omega,B_\omega,P_\omega\rangle
$$

```yaml
handoff:
  parent_actor: SalesAgent
  child_actor: QualityAgent
  goal:
    root: "Resolve overdue orders safely"
    child: "Verify certificate for order 4821"
    completion_evidence:
      - certificate_status
      - verification_source
  constraints:
    binding:
      - id: C-01
        rule: "Do not release shipment without certificate"
        status: unresolved
  authority:
    allow:
      - resource: quality_document_db
        operations: [read]
        scope: [order_4821]
    deny: [update, send_external]
  budget:
    max_tool_calls: 10
    max_tokens: 12000
    timeout_seconds: 120
  provenance:
    policy_version: P-12
    trace_id: tr_001
```

Typed Handoff의 목적은 문장을 길게 만드는 것이 아니다. Runtime이 `unresolved`, `allow/deny`, 완료 증거, 범위, 만료를 기계적으로 검사하게 만드는 것이다.

**실습 산출물:** 자연어·요약·제약 반복·Typed Handoff를 깊이 1~4에서 비교한 실험.  
**통과 기준:** Goal, Constraint, Authority, Budget, Provenance를 빠짐없이 계약으로 작성할 수 있어야 한다.

## 17단계. Compiler·Router·Runtime·Verifier를 실행 논리로 연결하기

[![17단계. Compiler·Router·Runtime·Verifier 연결하기](/assets/images/agent-level-step-17-compiler-router-runtime-verifier.png)](/assets/images/agent-level-step-17-compiler-router-runtime-verifier.png)
*17단계. Compiler·Router·Runtime·Verifier 연결하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

전체 알고리즘은 다음 루프로 정리할 수 있다.

1. 사용자 목표와 초기 환경으로 구조화 상태 생성
2. 새로운 관찰로 Fast-Mutable 상태 갱신
3. 보호 목표·필수 제약·권한 훼손 여부 확인
4. Compiler가 허용 후보 생성
5. 후보가 없으면 안전 실패 또는 Human 에스컬레이션
6. 후보를 다섯 추상화 수준으로 그룹화
7. Router가 수준 선택
8. 수준 안에서 구체 행동 선택
9. Skill·Delegation이면 전환 계약과 불변조건 검사
10. Runtime이 최신 신뢰 상태로 재검사 후 실행
11. Verifier가 사후조건 확인
12. 출처·비용·판정 이유를 Trace에 기록
13. 실패면 Recovery State 추가 후 재계획
14. 종료조건 충족 시 결과 확정

Runtime 재검사는 선택 시점과 사용 시점 사이 상태가 바뀌는 TOCTOU 문제를 줄인다. 승인 토큰이 만료되거나, 주문이 수정되거나, 예산이 소진될 수 있기 때문이다.

**실습 산출물:** `compile_action`, `select_level`, `execute_protected`, `verify_result` 의사코드와 end-to-end Trace.  
**통과 기준:** 각각의 실패가 Compiler, Router, Runtime, Verifier 중 어디에서 방지·복구돼야 하는지 분류할 수 있어야 한다.

## 18단계. 작은 MVP와 시뮬레이터 만들기

[![18단계. 작은 MVP와 시뮬레이터 만들기](/assets/images/agent-level-step-18-mvp-simulator.png)](/assets/images/agent-level-step-18-mvp-simulator.png)
*18단계. 작은 MVP와 시뮬레이터 만들기 — 클릭하면 원본 크기로 볼 수 있습니다.*

첫 MVP는 모든 기업 업무를 다루지 않는다. 제조·품질의 **지연 주문 출하 가능성 판단** 하나로 범위를 좁힌다. 이 시나리오는 반복 조회, 검증된 Skill, 전문 Agent, 관리자 승인, 정책 blocker, 동적 수준 전환을 한 흐름에 담을 수 있다.

| 요소 | 권장 규모 |
|---|---:|
| 업무 | 1개 |
| Tool | 12~20개 |
| Skill | 3~5개 |
| Agent | 2개 |
| Human 행동 | 2종 |
| Policy | 8~12개 |
| Pilot Task | 20~30개 |

시뮬레이터에는 Order DB, Policy Engine, Human Simulator, Tool Failure Injector, Cost Model, Oracle, Trace Store가 필요하다. 실제 ERP를 완벽히 복제하는 것이 아니라, 실패·지연·권한·비용을 통제해 인과적 차이를 측정하는 실험 장치다.

**실습 산출물:** Primitive, Skill, Delegation, Human, Dynamic, Governance, Handoff, Over-Delegation 유형의 Pilot Task.  
**통과 기준:** 모든 Task를 같은 초기 상태와 seed에서 재현하고, 금지 효과와 실패 원인을 Trace로 분석할 수 있어야 한다.

## 19단계. Benchmark와 평가 지표 설계하기

[![19단계. Benchmark와 평가 지표 설계하기](/assets/images/agent-level-step-19-benchmark-metrics.png)](/assets/images/agent-level-step-19-benchmark-metrics.png)
*19단계. Benchmark와 평가 지표 설계하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

성공률 하나로 Agent 품질을 평가하면 왜곡이 생긴다. 모든 업무를 비싼 전문 Agent에게 넘겨도 성공률은 높을 수 있고, 모든 요청을 거절하면 정책 위반은 0이 될 수 있다.

| 지표 | 측정하는 것 | 좋은 방향 |
|---|---|---|
| Task Success Rate | 업무를 완료했는가 | 높을수록 좋음 |
| Safe Completion Rate | 위반 없이 성공했는가 | 높을수록 좋음 |
| Abstraction Accuracy | 올바른 수준을 골랐는가 | 높을수록 좋음 |
| Abstraction Regret | 잘못된 수준으로 잃은 효용 | 낮을수록 좋음 |
| CPR | Handoff에서 미해결 제약을 모두 보존했는가 | 높을수록 좋음 |
| AER | 최소 필요 권한 대비 노출 권한 | 1에 가까울수록 좋음 |
| Human Precision / Recall | 필요한 때만, 필요할 때 사람을 불렀는가 | 둘 다 높아야 함 |
| Cost / Latency | 토큰·API·호출·대기 비용 | 낮을수록 좋음 |

주요 수식은 다음과 같다.

$$
TSR=\frac{successful\ tasks}{total\ tasks}
$$

$$
SCR=\frac{successful\ tasks\ with\ zero\ violation}{total\ tasks}
$$

$$
CPR=\frac{handoffs\ preserving\ all\ unresolved\ hard\ constraints}{total\ handoffs}
$$

**실습 산출물:** Task별 Oracle, decision-level Trace, 다차원 평가표.  
**통과 기준:** “정책 위반 0”과 “좋은 Agent”가 동의어가 아닌 이유를 설명할 수 있어야 한다.

## 20단계. Baseline·실험·통계·발표까지 완성하기

[![20단계. Baseline·실험·통계·발표 완성하기](/assets/images/agent-level-step-20-baselines-experiments-statistics.png)](/assets/images/agent-level-step-20-baselines-experiments-statistics.png)
*20단계. Baseline·실험·통계·발표 완성하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

최종 단계에서는 제안 구조가 단순한 구성요소 조합을 넘어 독립적인 효과를 만드는지 검증한다.

### 반드시 포함할 Baseline

- Flat-All
- ReAct
- Semantic Top-k
- State Filter
- Causal Tool Filter
- Risk-Aware Gate
- Skill Hierarchy
- Agent-as-Tool
- Post-hoc Policy Guard
- Proposed Method

### 중심 실험

1. Flat selection과 Level-first selection 비교
2. Task Horizon 증가 실험
3. Registry Size 증가 실험
4. 상태 전이마다 수준이 바뀌는 Dynamic Switching
5. Prune-only와 Prune-and-Rewrite 비교
6. 자연어 Handoff와 Typed Handoff 비교
7. Delegation Depth 증가 실험
8. 조직 그래프 기반 delegable authority 실험
9. Ablation Study
10. `Hierarchy × State × Authority × Typed Handoff` Factorial Experiment
11. 보지 못한 Tool·Skill·역할·정책 조합 일반화
12. 효용 가중치 민감도 분석

### 통계 계획

- 이진 성공 비교: paired bootstrap, McNemar test
- 비용·Regret 비교: paired bootstrap, Wilcoxon signed-rank
- Horizon·Registry Size·Delegation Depth 상호작용: mixed-effects regression
- 모든 결과: 효과크기, 신뢰구간, 실제 비용 차이 함께 보고

**실습 산출물:** 연구 질문, 가설, 반증 조건, preregistration, 코드, Task spec, 정책, 결과표, 실패 분석, 5분·20분 발표자료.  
**통과 기준:** “RBAC, Tool Retrieval, Workflow Engine, Policy Monitor를 조합한 것 아닌가?”라는 반론에 실험 설계로 답할 수 있어야 한다.

---

---

## 이 연구가 실제로 강해지려면 무엇을 증명해야 하는가

프레임워크의 이름보다 다음 상호작용 효과가 핵심이다.

1. 행동 공간과 업무 길이가 커질수록 Level-first routing의 이점이 커지는가?
2. 금지 후보를 삭제만 하는 것보다 합법적 대안을 재구성하는 방식이 False Blocking을 줄이는가?
3. 최초 요청에서 한 번만 판단하는 것보다 상태 전이마다 재컴파일하는 방식이 Dynamic Task에서 유리한가?
4. Typed Handoff가 위임 깊이가 증가해도 자연어 Handoff보다 제약을 더 잘 보존하는가?
5. 정책 위반 0이 모든 업무 차단의 결과가 아니라 Safe Completion과 Human Burden 측면에서도 유효한가?

반대로 Flat selection이나 단순 Top-k가 같은 결과를 내고, Typed Handoff의 이점이 없으며, 보지 못한 과제에서 효과가 사라진다면 연구 가설은 약해진다. 이러한 반증 조건을 결과를 보기 전에 고정해야 한다.

## 10주 학습 일정으로 압축하기

| 주차 | 단계 | 핵심 산출물 |
|---|---|---|
| 1주 | 1~2 | 한 문장 논제, 행동 수준 분류표 |
| 2주 | 3~4 | 전체 구조도, 불변조건 사례 |
| 3주 | 5~6 | 행동 집합, F/A/C/V 진리표 |
| 4주 | 7~8 | 효용표, 조직 그래프, 통계 기초 |
| 5주 | 9~10 | 상태기계, Tool 계약 12개 |
| 6주 | 11~12 | 실행 방식 비교표, Agent 계보 |
| 7주 | 13~14 | GH-SMDP 설명서, 권한·정책표 |
| 8주 | 15~16 | State Schema, Typed Handoff |
| 9주 | 17~18 | End-to-end MVP, Pilot Task |
| 10주 | 19~20 | 평가·실험·발표 연구 패키지 |

하루 90분을 쓴다면 `15분 회상 → 25분 개념 → 30분 손 실습 → 10분 논문 연결 → 10분 반례와 질문 작성`으로 운영하는 것이 효율적이다. 이해의 기준은 읽었을 때 익숙한지가 아니라, 자료 없이 설명하고 구현·실험에 적용할 수 있는지다.

## 자주 묻는 질문

## Tool과 Skill의 가장 큰 차이는 무엇인가?

Tool은 한 번의 제한된 환경 연산이다. Skill은 여러 Tool과 판단을 내부 절차로 묶어 하나의 시간적으로 확장된 행동처럼 제공한다. 따라서 Skill은 Planner의 의사결정 단계를 압축하지만, 절차 버전과 내부 부작용을 관리해야 한다.

## RAG가 정책 문서를 찾으면 실행 권한도 생기는가?

아니다. RAG가 찾은 문장은 정보다. 실제 실행 권한은 신뢰된 권한 저장소, 승인 이벤트, Capability, Runtime 검증에서 나온다.

## Human 호출은 Agent의 실패인가?

항상 그렇지 않다. 목표가 모호하거나, 정보가 사람에게만 있거나, 비위임 승인 권한이 필요한 경우 Human은 정답에 가까운 행동 수준이다. 중요한 것은 불필요한 호출과 필요한 호출 누락을 함께 측정하는 것이다.

## 왜 일반 MDP보다 SMDP가 적합한가?

Skill, Delegation, Human 승인 대기는 한 번의 선택이 여러 원시 단계와 가변 시간을 포함한다. SMDP는 행동 지속시간과 누적 결과를 반영할 수 있어 이런 이질적 행동 수준을 표현하기 쉽다.

## 모델에게 금지 Tool을 숨기면 보안이 완성되는가?

아니다. 후보를 숨기는 것은 오선택을 줄이는 의사결정 인터페이스다. 실제 보안 경계는 Runtime이 최신 권한·정책·상태를 확인하고 효과 있는 행동을 강제하는 지점이다.

## 가장 현실적인 첫 MVP는 무엇인가?

제조·품질의 지연 주문 대응이 적합하다. 주문 조회, 일괄 Skill, 인증서 전문 판단, 관리자 승인, 외부 발송, 재시도와 검증을 하나의 흐름에 넣을 수 있기 때문이다.

## 마무리

Agent가 사용할 수 있는 수단이 Tool을 넘어 Skill, 다른 Agent, Human, Control로 확장될수록 “다음 API는 무엇인가?”만으로는 충분하지 않다. 시스템은 먼저 현재 상태에서 **정당한 행동 범위**를 만들고, 그 안에서 **적절한 시간적·조직적 추상화 수준**을 선택해야 한다. 실행 경계가 바뀌더라도 목표, 필수 제약, 권한, 예산, 출처가 유지돼야 하며, 실제 외부 효과는 Runtime과 Verifier가 검증해야 한다.

결국 좋은 Agent는 가능한 행동 중 그럴듯한 하나를 고르는 시스템이 아니라, **현재 상태에서 허용 가능한 선택면을 구성하고, 그 안에서 적절한 수준을 선택하며, 경계 전환에서도 정책을 보존하는 통제된 의사결정 시스템**이다.

---

## 기반 자료

- *At What Level Should an Agent Act?*
- 부제: *Policy-Preserving Hierarchical Abstraction Selection over Tools, Skills, Delegation, and Human Intervention*
- 학습서: *논문 이해를 위한 고등학교 기초부터 연구·구현까지의 단계별 학습서*

> 이미지 경로는 `./images/` 기준이다. 블로그 또는 정적 사이트에 게시할 때 이 Markdown 파일과 `images` 폴더를 함께 업로드해야 한다.
