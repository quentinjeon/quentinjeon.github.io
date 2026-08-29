---
layout: single
title: "에이전트는 어느 수준에서 행동해야 하는가 (2/4) — 허용 판정과 시스템 기초"
excerpt: "F/A/C/V 진리표로 '지금 이 행동이 허용되는가'를 판정하고, 효용·argmax·그래프·상태기계·Tool 계약까지 시스템 기초를 세운다."
series: agent-level-20steps
part: 2
categories:
  - labs
tags:
  - Agent 학습 로드맵
  - Admissibility
  - Utility
  - State Machine
  - Tool Contract
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/agent-level-p2.jpg
---

{% include series-nav.html %}

> **6~10단계 · 허용 판정과 시스템 기초**
> 이 구간의 질문: **현재 상태에서 어떤 행동이 합법적·실행 가능한가**

[1편에서](/labs/agent-level-problem-and-foundations/) 행동 수준을 왜 따로 골라야 하는지 정리했습니다. 이번 편은 그다음 구간입니다.

---

## 6단계. 논리식과 F/A/C/V 판정 이해하기

[![6단계. 논리식과 F/A/C/V 판정 이해하기](/assets/images/agent-level-step-06-facv-admissibility.png)](/assets/images/agent-level-step-06-facv-admissibility.png)
*6단계. 논리식과 F/A/C/V 판정 이해하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

행동의 허용 여부는 네 조건의 논리곱으로 표현할 수 있다.

$$
M_t(\omega)=F_t(\omega)\land A_t(\omega)\land C_t(\omega)\land V_t(\omega)
$$

| 기호 | 의미 | 질문 | 실패 예 |
|---|---|---|---|
| F | Feasibility | 선행조건이 충족됐는가 | 주문 ID 없음 |
| A | Authority | 권한이 있는가 | 외부 발송 권한 없음 |
| C | Constraint | 필수 제약이 허용하는가 | 인증서 누락 상태에서 출하 |
| V | Availability | 필요한 자원과 Runtime이 있는가 | 품질 DB 연결 끊김 |

네 조건 중 하나라도 거짓이면 해당 행동은 허용 후보에서 제외된다. 예를 들어 관리자 승인은 외부 발송의 필요조건일 수 있지만, 수신자 검증·민감정보 검사·발송 권한이 추가로 필요하다면 승인 하나만으로 충분조건은 아니다.

**실습 산출물:** `SEND_CUSTOMER_EMAIL` 진리표와 불허 이유별 합법적 다음 행동.  
**통과 기준:** 필요조건과 충분조건을 실제 정책 문장으로 구분할 수 있어야 한다.

## 7단계. 확률·효용·가중치·argmax 이해하기

[![7단계. 확률·효용·가중치·argmax 이해하기](/assets/images/agent-level-step-07-utility-argmax.png)](/assets/images/agent-level-step-07-utility-argmax.png)
*7단계. 확률·효용·가중치·argmax 이해하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

성공 확률이 가장 높은 행동이 항상 최적은 아니다. 비용, 위험, 인수인계 부담, 권한 노출, 불확실성을 함께 봐야 한다.

$$
\begin{aligned}
U(\omega|s_t) ={}& P_{succ}(\omega|s_t,g_t)V_g \\
&-\lambda_c Cost-\lambda_r Risk-\lambda_h Handoff \\
&-\lambda_a AuthorityExposure-\lambda_u Uncertainty
\end{aligned}
$$

예를 들어 전문 Agent 위임의 성공 기대가치가 가장 높더라도, 호출 비용과 인수인계 부담이 크면 검증된 Skill의 순효용이 더 높을 수 있다. $\lambda$는 각 벌점을 얼마나 중요하게 볼지 결정하며, 기술 파라미터인 동시에 조직의 위험 선호를 반영한다.

선택은 두 단계로 수행된다.

$$
l_t^*=\arg\max_{l\in L_t}Q_L(s_t,l)
$$

$$
\omega_t^*=\arg\max_{\omega\in\Omega_t^{adm}(l_t^*)}Q_\Omega(s_t,\omega)
$$

**실습 산출물:** 후보별 성공·비용·위험·지연 값과 가중치 민감도 표.  
**통과 기준:** 최대값과 argmax의 차이, 성공 확률과 순효용의 차이를 설명할 수 있어야 한다.

## 8단계. 그래프·부분집합·귀납법·기초 통계 익히기

[![8단계. 그래프·부분집합·귀납법·기초 통계 익히기](/assets/images/agent-level-step-08-graph-induction-statistics.png)](/assets/images/agent-level-step-08-graph-induction-statistics.png)
*8단계. 그래프·부분집합·귀납법·기초 통계 익히기 — 클릭하면 원본 크기로 볼 수 있습니다.*

조직 구조와 실행 이력은 그래프로 표현할 수 있다.

```text
SalesStaff --reports_to--> SalesManager
SalesManager --may_request--> QualityTeam
QualityLead --owns--> QualityDocumentDB
SalesManager --approves--> ExternalCustomerMessage
```

자식 권한은 정책상 위임 가능한 권한 집합 안에 있어야 한다.

$$
\Lambda_c \subseteq D(\Lambda_p,\rho_p,P)
$$

귀납법은 루트에서 제약이 성립하고, 모든 부모-자식 전환에서 제약이 보존된다면, 어느 깊이의 실행 leaf에서도 조상 경로의 미해결 제약이 유지된다는 구조를 설명하는 데 사용된다.

실험 결과는 한 번의 성공률만으로 판단하지 않는다. 평균, 분산, 신뢰구간, 효과크기를 함께 봐야 한다.

**실습 산출물:** 조직·승인·위임 그래프, 깊이 0~4 제약 전달표, 신뢰구간이 포함된 결과표.  
**통과 기준:** 직접 권한과 위임 가능한 권한의 차이를 설명하고, 결과의 불확실성을 통계적으로 표현할 수 있어야 한다.

## 9단계. Data·State·Event·Command·Effect 구분하기

[![9단계. Data·State·Event·Command·Effect 구분하기](/assets/images/agent-level-step-09-data-state-event-command-effect.png)](/assets/images/agent-level-step-09-data-state-event-command-effect.png)
*9단계. Data·State·Event·Command·Effect 구분하기 — 클릭하면 원본 크기로 볼 수 있습니다.*

| 개념 | 정의 | 주문 업무 예 |
|---|---|---|
| Data | 저장된 사실 또는 기록 | 주문번호, 납기일, 고객명 |
| State | 현재 판단에 필요한 값 | 납기 지연, 검사 완료, 인증서 누락 |
| Event | 상태를 변화시키는 발생 사실 | 검사 완료, 관리자 승인 |
| Command | 변화를 요청하는 명령 | 이메일 발송 요청 |
| Effect | 실행 후 실제 발생한 변화 | 이메일 발송됨, 주문 보류 전환 |

문서에서 “승인이 필요하다”는 문장을 검색한 것과 승인 시스템에 검증된 승인 이벤트가 존재하는 것은 다르다. 전자는 정보이고, 후자는 보호된 상태 또는 권한 증거다.

**실습 산출물:** 주문·인증서·메시지·승인 사례를 다섯 개념으로 분류한 표.  
**통과 기준:** LLM 메모리에 적힌 문장이 보호 상태를 직접 변경하면 안 되는 이유를 설명할 수 있어야 한다.

## 10단계. 상태기계와 Tool 계약 만들기

[![10단계. 상태기계와 Tool 계약 만들기](/assets/images/agent-level-step-10-state-machine-tool-contract.png)](/assets/images/agent-level-step-10-state-machine-tool-contract.png)
*10단계. 상태기계와 Tool 계약 만들기 — 클릭하면 원본 크기로 볼 수 있습니다.*

상태기계는 허용된 전이와 금지 전이를 명시한다.

```text
DRAFT
  └─ submit_for_approval → PENDING_APPROVAL

PENDING_APPROVAL
  ├─ approve → APPROVED
  └─ reject  → REJECTED

APPROVED
  └─ send → SENT

금지 전이: DRAFT → SENT
```

Tool은 이름과 설명만으로 충분하지 않다. 입력·출력, 선행조건, 권한, 효과, 위험, 가역성, 사후조건, Verifier를 계약으로 가져야 한다.

```yaml
Action: SEND_CUSTOMER_EMAIL
Preconditions:
  - message.status == APPROVED
  - recipient.verified == true
  - actor has external_email:send
  - no restricted data in body
Postconditions:
  - delivery_provider accepted message
  - audit_log contains message_id
  - message.status == SENT
```

**실습 산출물:** 12개 Tool 계약과 효과 있는 Tool의 사후조건 테스트.  
**통과 기준:** Tool이 오류 없이 반환한 것과 실제 외부 효과가 발생한 것을 구분하고, 멱등성의 필요성을 설명할 수 있어야 한다.
