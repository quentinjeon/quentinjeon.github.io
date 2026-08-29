---
layout: single
title: "에이전트는 어느 수준에서 행동해야 하는가 (3/4) — Agent·강화학습·거버넌스"
excerpt: "Workflow와 Skill의 경계, RAG와 ReAct, MDP에서 SMDP와 GH-SMDP로 가는 이유, 그리고 권한 모델과 구조화된 상태 설계."
series: agent-level-20steps
part: 3
categories:
  - labs
tags:
  - Agent 학습 로드맵
  - SMDP
  - Options
  - RAG
  - ReAct
  - Agent Governance
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/agent-level-p3.jpg
---

{% include series-nav.html %}

> **11~15단계 · Agent·강화학습·거버넌스**
> 이 구간의 질문: **시간·조직·권한 경계를 어떻게 모델링할 것인가**

[1편에서](/labs/agent-level-problem-and-foundations/) 행동 수준을 왜 따로 골라야 하는지 정리했습니다. 이번 편은 그다음 구간입니다.

---

## 11단계. Workflow·Skill·Delegation·Human·Control 구분하기

[![11단계. Workflow·Skill·Delegation·Human·Control 구분하기](/assets/images/agent-level-step-11-workflow-skill-delegation-human-control.png)](/assets/images/agent-level-step-11-workflow-skill-delegation-human-control.png)
*11단계. Workflow·Skill·Delegation·Human·Control 구분하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

- **Workflow**는 작업의 순서·분기·반복·예외 처리를 정의한다.
- **Skill**은 Workflow를 재사용 가능한 상위 행동으로 포장한다.
- **Delegation**은 다른 판단 주체에게 하위 목표와 제한된 권한을 넘긴다.
- **Human**은 질문·승인·예외·책임 판단을 요청한다.
- **Control**은 Retry, Replan, Rollback, Wait, Abort, Finish로 실행 흐름을 바꾼다.

Skill은 비교적 정의된 내부 절차를 실행한다. Delegated Agent는 관찰에 따라 자체 계획을 바꿀 수 있다. 이 차이 때문에 Delegation은 더 유연하지만 목표 드리프트, 권한 노출, 비용과 인수인계 손실이 커질 수 있다.

**실습 산출물:** 같은 출하 업무를 Tool 체인, Skill, Delegation 세 방식으로 표현한 실행 궤적.  
**통과 기준:** Skill과 Delegated Agent의 자율성·책임·위험 차이를 설명할 수 있어야 한다.

## 12단계. LLM·RAG·ReAct·Function Calling 이해하기

[![12단계. LLM·RAG·ReAct·Function Calling 이해하기](/assets/images/agent-level-step-12-llm-rag-react-function-calling.png)](/assets/images/agent-level-step-12-llm-rag-react-function-calling.png)
*12단계. LLM·RAG·ReAct·Function Calling 이해하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

| 방식 | 주된 목적 | 외부 상태 변경 |
|---|---|---|
| 일반 LLM | 언어 생성 | 없음 |
| RAG | 외부 문서로 답변 근거 보강 | 보통 없음 |
| Tool Agent | 환경 조회·변경 | 가능 |
| Governed Agent | 정책·권한 아래 수준 선택과 실행 | 통제된 방식으로 가능 |

Function Calling은 구조화된 함수 이름과 인자를 출력하는 인터페이스다. 그러나 구조화된 호출을 만들었다고 실제 권한이 생기는 것은 아니다. RAG가 “본부장 승인이 필요하다”는 문장을 찾았다고 해서 승인 이벤트가 생성된 것도 아니다.

ReAct형 Agent Loop는 관찰→상태 갱신→행동→새 관찰의 반복을 제공한다. 다만 이 반복 구조만으로 정책 보존, 권한 증거, 하위 Agent 인수인계, 실제 효과 검증이 자동 해결되지는 않는다.

**실습 산출물:** 같은 업무를 일반 LLM, RAG, ReAct, Tool Retrieval, Agent-as-Tool, Level-first 방식으로 비교한 표.  
**통과 기준:** 검색 근거, 모델 제안, 실행 권한, 실제 효과를 분리할 수 있어야 한다.

## 13단계. MDP·SMDP·Options·GH-SMDP 이해하기

[![13단계. MDP·SMDP·Options·GH-SMDP 이해하기](/assets/images/agent-level-step-13-mdp-smdp-options-gh-smdp.png)](/assets/images/agent-level-step-13-mdp-smdp-options-gh-smdp.png)
*13단계. MDP·SMDP·Options·GH-SMDP 이해하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

MDP는 상태에 따라 행동을 선택하고 보상과 다음 상태를 얻는 순차적 의사결정 모델이다.

$$
\mathcal{M}=\langle S,A,P,R,\gamma\rangle
$$

Tool은 비교적 한 스텝 행동에 가깝지만, Skill·Delegation·Human 대기는 여러 원시 단계와 가변 시간을 포함한다. 그래서 행동 지속시간을 명시적으로 다루는 SMDP가 더 적합하다.

Option은 다음 세 요소로 표현된다.

$$
\omega=(I_\omega,\pi_\omega,\beta_\omega)
$$

- $I_\omega$: 시작 가능한 상태 집합
- $\pi_\omega$: 내부 실행 정책
- $\beta_\omega$: 종료 조건

제안 모델인 GH-SMDP는 여기에 조직 정책과 조직·권한 구조, 거버넌스 전환 계약을 추가한다.

**실습 산출물:** 원시 Tool 5단계와 Skill 1단계가 같은 목표를 달성하는 작은 시뮬레이션.  
**통과 기준:** Skill의 시간적 확장과 Delegation의 조직적 확장을 SMDP 관점에서 설명할 수 있어야 한다.

## 14단계. 거버넌스와 권한 모델 이해하기

[![14단계. 거버넌스와 권한 모델 이해하기](/assets/images/agent-level-step-14-governance-authority.png)](/assets/images/agent-level-step-14-governance-authority.png)
*14단계. 거버넌스와 권한 모델 이해하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

거버넌스는 “무엇을 할 수 있는가”뿐 아니라 “누가 어떤 목적과 책임 아래 결정하고 승인하며 기록하는가”를 정한다.

- **Authentication:** 주체가 누구인지 확인
- **Authorization:** 그 주체가 특정 행동을 할 수 있는지 판단
- **RBAC:** 역할에 권한을 묶음
- **ABAC:** 주체·자원·행동·환경 속성으로 판단
- **Capability:** 특정 자원·연산을 실행할 수 있다는 제한된 권한 증거
- **Least Privilege:** 필요한 최소 범위와 시간만 권한 부여
- **Reference Monitor:** 모든 보호 자원 접근을 우회 없이 중재
- **Separation of Duties:** 작성·승인·실행 책임 분리

가장 중요한 구분은 다음이다.

> **Candidate Visibility ≠ Execution Authority**  
> 모델에게 보이는 후보 목록은 의사결정 인터페이스다. 실제 실행 권한은 Runtime이 검증하는 Capability와 신뢰 상태에서 나온다.

**실습 산출물:** 역할 5개, 자원 8개, 행동 12개의 RBAC 표와 ABAC 정책, Capability 예시, 위협모델.  
**통과 기준:** 모델의 “나는 관리자다”라는 문장이 권한 증거가 될 수 없는 이유를 설명할 수 있어야 한다.

## 15단계. 구조화된 상태와 변경 등급 설계하기

[![15단계. 구조화된 상태와 변경 등급 설계하기](/assets/images/agent-level-step-15-structured-state-mutability.png)](/assets/images/agent-level-step-15-structured-state-mutability.png)
*15단계. 구조화된 상태와 변경 등급 설계하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

런타임 상태는 일곱 필드로 분리한다.

$$
s_t=(e_t,\tau_t,g_t,C_t,\Lambda_t,\rho_t,m_t)
$$

| 필드 | 의미 | 주문 예 |
|---|---|---|
| Environment | 외부 환경 상태 | 생산 완료, 인증서 레코드 손상 |
| Task Progress | 업무 진행 | 250건 중 180건 확인 |
| Goal Stack | 목표와 하위 목표 | 지연 원인 규명 → 안내 Draft |
| Constraints | 미해결 필수 제약 | 인증서 없이는 출하 금지 |
| Authority | 활성 권한 범위 | 품질 읽기, 외부 발송 불가 |
| Provenance / Org | 출처와 조직 맥락 | SalesAgent, 정책 v12 |
| Memory | 임시 작업 정보 | 이미 확인한 주문 목록 |

모든 상태는 같은 방식으로 바뀌면 안 된다.

| 변경 등급 | 포함 항목 | 변경 규칙 |
|---|---|---|
| Fast-Mutable | 관찰, 진행률, 임시 메모리 | 행동·관찰마다 갱신 |
| Controlled-Mutable | 계획, 하위 목표, Skill 선택 | 명시적 재계획으로 변경 |
| Protected | 루트 목표, 하드 제약, 권한, 보안 정책 | 신뢰된 정책·승인 없이는 변경 불가 |

**실습 산출물:** `state.json`과 각 필드의 신뢰 출처·변경 API.  
**통과 기준:** Agent가 계획은 바꿀 수 있지만 루트 목표와 하드 제약을 임의로 수정해서는 안 되는 이유를 설명할 수 있어야 한다.
