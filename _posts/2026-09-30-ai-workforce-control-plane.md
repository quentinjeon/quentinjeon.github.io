---
layout: single
title: "AI 조직도와 사원증 레이어, 비즈니스가 될까?"
seo_title: "AI 사원증과 AI Workforce Control Plane — 기업 AI 권한 통제"
excerpt: "기업 AI의 다음 인프라는 '답변하는 AI'가 아니라 '권한을 가지고 일하는 AI'를 통제하는 시스템일 수 있습니다. AI 사원증은 좋은 메시지지만, 돈이 되는 것은 Identity가 아니라 Authority와 Action의 통제입니다."
description: "AI Agent가 ERP·MES·CRM에서 실제 업무를 수행할 때 필요한 권한 구조. Agent Registry, Delegated Authority, Capability Registry, Policy Engine, Action Gateway로 이어지는 AI Workforce Control Plane과 그 수익모델·GTM·해자를 정리합니다."
categories:
  - ax
  - foundation
tags:
  - AI 에이전트
  - AI 거버넌스
  - 에이전트 아키텍처
  - 기업 AI 도입
toc: true
toc_sticky: true
header:
  teaser: /assets/images/thumbs/agent-authority.jpg
---

기업에 AI Agent가 들어오기 시작하면서 재미있는 문제가 하나 생기고 있습니다.

AI가 단순히 질문에 답하는 수준에 머문다면 문제가 크지 않습니다. 사내 문서를 검색하고, 보고서를 요약하고, 이메일 초안을 만들어주는 정도라면 기존의 인증과 권한 체계 안에서도 어느 정도 운영할 수 있습니다.

하지만 AI가 **실제 업무를 수행하기 시작하면** 이야기가 달라집니다. 예를 들어 AI가 다음과 같은 일을 한다고 생각해보겠습니다.

- ERP에서 재고를 조회한다.
- MES에서 생산계획을 확인한다.
- CRM에서 고객 정보를 가져온다.
- 구매 요청을 생성한다.
- 거래처에 메일을 보낸다.
- 그룹웨어에서 결재를 요청한다.
- 생산계획을 수정한다.

이때부터 AI는 단순한 챗봇이 아닙니다. 기업 안에서 실제로 일을 수행하는 하나의 **업무 주체**에 가까워집니다.

그러면 자연스럽게 이런 질문이 생깁니다. **AI에게도 사원증이 필요한 것 아닐까?**

그리고 한 단계 더 나아가면 질문은 이렇게 바뀝니다.

> AI는 누구를 대신해서 일하고 있는가?
> 어떤 시스템에 접근할 수 있는가?
> 어떤 데이터를 볼 수 있는가?
> 어떤 행동까지 수행할 수 있는가?
> 어디부터는 사람의 승인을 받아야 하는가?

저는 이 문제가 앞으로 Enterprise AI에서 상당히 중요해질 수 있다고 봅니다. 다만 여기서 중요한 것은 **'AI 사원증'을 만드는 것 자체가 사업의 핵심은 아니라는 점**입니다. 진짜 사업은 그보다 훨씬 아래에 있습니다.

## 1. AI 조직도와 AI 사원증이라는 아이디어

먼저 가장 직관적인 그림부터 생각해볼 수 있습니다. 기업에는 이미 조직도가 있습니다.

```text
CEO
│
├─ 영업팀
│   ├─ 영업팀장
│   └─ 영업담당자
│
├─ 생산팀
│   ├─ 생산팀장
│   └─ 생산담당자
│
└─ 재무팀
    ├─ 재무팀장
    └─ 재무담당자
```

앞으로 여기에 AI가 들어온다면 이런 형태가 될 수 있습니다.

```text
CEO
│
├─ 영업팀
│   ├─ 영업팀장
│   ├─ 영업담당자
│   └─ Sales Agent
│
├─ 생산팀
│   ├─ 생산팀장
│   ├─ 생산담당자
│   └─ MES Agent
│
└─ 재무팀
    ├─ 재무팀장
    ├─ 재무담당자
    └─ Finance Agent
```

이 구조는 UX적으로 상당히 이해하기 쉽습니다. AI를 별도의 시스템이나 복잡한 API로 설명하지 않고, **"우리 조직 안에서 일하는 또 하나의 디지털 직원"** 으로 표현할 수 있기 때문입니다.

그리고 각각의 Agent에게 다음과 같은 정보를 부여할 수 있습니다.

| 구분 | 항목 |
|---|---|
| **신원** | Agent ID · Agent Name · 사용하는 모델 |
| **소속** | 소속 조직 · 담당 업무 |
| **책임** | Owner · Human Sponsor |
| **수명** | 현재 상태 · 만료 시점 |
| **범위** | 접근 가능한 시스템 · 실행 가능한 업무 |

이것이 일종의 **AI 사원증**입니다.

하지만 여기까지만 만들면 아직 제품의 깊이가 부족합니다. 사원증은 단지 AI가 누구인지 알려줄 뿐입니다. 기업 입장에서 더 중요한 문제는 **그래서 이 AI가 실제로 무엇을 할 수 있는가?** 입니다.

![AI 조직도와 사원증 레이어, 어디서 돈이 되는가 — Identity·Authority·Action Control Plane](/assets/images/agent-authority-01-org-chart-and-badge.jpg)

## 2. 제품의 중심은 AI 사원증이 아니라 '실행 권한 통제'다

사람의 사원증을 생각해보면 쉽게 이해할 수 있습니다. 사원증에는 내 이름과 소속이 적혀 있습니다. 하지만 실제 회사 업무는 사원증 하나로 결정되지 않습니다. 같은 회사 직원이라도 사람마다 다음이 다릅니다.

- 어떤 문서를 볼 수 있는가
- 어떤 시스템에 로그인할 수 있는가
- 얼마까지 결제할 수 있는가
- 어떤 결재를 올릴 수 있는가
- 어떤 고객 정보를 조회할 수 있는가
- 어떤 데이터를 외부로 보낼 수 있는가

AI도 마찬가지입니다. 그래서 기업용 Agent를 운영하기 위해서는 최소 다음 개념이 분리되어야 합니다.

### User Identity — 요청한 사람은 누구인가?

이름, 직책, 부서, 직급, 조직, 계정.

### Agent Identity — 어떤 Agent가 업무를 수행하는가?

Sales Agent, MES Agent, Finance Agent, Procurement Agent.

### Delegated Authority — 사용자가 Agent에게 어떤 권한을 위임했는가?

예를 들어 생산팀장이 MES Agent를 사용한다고 해서 MES Agent가 생산팀장이 가진 모든 권한을 자동으로 가져가서는 안 됩니다.

```text
생산팀장 권한  100
        │
        ↓ 위임
MES Agent      30
```

처럼 제한된 권한만 위임할 수 있어야 합니다.

### Resource Permission — 어떤 데이터와 시스템에 접근 가능한가?

| 자원 | 접근 |
|---|---|
| ERP | 허용 |
| MES | 허용 |
| CRM | 차단 |
| 급여정보 | 차단 |
| 생산정보 | 허용 |
| 원가정보 | 제한 |

### Action Permission — 무엇을 할 수 있는가?

| 행동 | 허용 수준 |
|---|---|
| `Inventory.Read` | 허용 |
| `ProductionPlan.Read` | 허용 |
| `ProductionPlan.Update` | 승인 필요 |
| `PurchaseOrder.Create` | 승인 필요 |
| `Payment.Execute` | 차단 |

### Context — 상황에 따라 정책이 달라진다

같은 사용자가 같은 Agent에게 같은 업무를 시켜도 상황에 따라 정책이 달라질 수 있습니다.

```text
업무시간 중 + 사내 네트워크 + 1천만원 이하 구매
→ 실행 가능

새벽 2시 + 외부 접속 + 5억원 구매
→ 관리자 승인
```

따라서 Enterprise AI의 권한 문제는 단순한 `Role × Department` 문제가 아닙니다. 오히려 다음 조합에 가깝습니다.

```text
User Identity
  + Agent Identity
  + Delegated Authority
  + Resource Permission
  + Action Permission
  + Context
```

이 여섯 가지를 어떻게 연결하느냐가 중요합니다.

![AI Workforce Control Plane 상세 구조 — Identity Source에서 Action Gateway까지](/assets/images/agent-authority-02-control-plane-architecture.jpg)

## 3. AI Workforce Control Plane이라는 개념

이 구조를 하나의 제품으로 표현하면 저는 **AI Workforce Control Plane** 이라는 개념이 가장 자연스럽다고 봅니다.

기존 기업 시스템을 모두 갈아엎는 것이 아닙니다. ERP도 그대로 둡니다. MES도 그대로 둡니다. CRM도 그룹웨어도 그대로 둡니다. 그 위에 AI가 안전하게 시스템을 사용할 수 있도록 **새로운 통제 계층**을 만드는 것입니다.

```text
Human / Organization
        ↓
Agent Registry
        ↓
Organization & Authority Graph
        ↓
Capability Registry
        ↓
Policy Engine
        ↓
Action Gateway
        ↓
ERP / MES / CRM / Groupware / KMS
        ↓
Audit
```

여기서 각각의 역할이 명확합니다.

| 계층 | 역할 |
|---|---|
| **Identity Source** | 기존 HRIS, SSO, IAM, 조직도에서 사람과 조직 정보를 받아온다 |
| **Agent Registry** | 회사에서 운영되는 AI Agent를 등록한다. 사람에게 사번이 있다면 Agent에도 Agent ID가 있다 |
| **Organization & Authority Graph** | 사람·Agent·조직·데이터·업무·권한의 관계를 연결한다 |
| **Capability Registry** | 기업에서 수행 가능한 업무를 표준화한다 |
| **Policy Engine** | Agent가 특정 행동을 실행할 수 있는지 판단한다 |
| **Action Gateway** | 정책 검증이 끝난 행동만 실제 시스템에 전달하고 결과를 기록한다 |

Authority Graph는 예를 들어 이렇게 표현할 수 있습니다.

```text
김생산 팀장
    │ owns
    ↓
Production Agent
    ├─ ProductionPlan.Read
    ├─ Inventory.Read
    └─ ProductionPlan.Update
             └─ Require Approval
```

즉 제품의 핵심은 **AI에게 사원증을 발급하는 것이 아니라, AI가 실제 업무를 수행할 때 행동을 통제하는 것**입니다.

## 4. Agent에게 권한을 줬다고 끝나는 것이 아니다

여기서 또 하나의 중요한 문제가 생깁니다. 예를 들어 사용자가 AI에게 이렇게 말합니다.

> 지난달 재고 현황 보고서를 만들어서 거래처에 보내줘.

사람 입장에서는 단순한 한 문장입니다. 하지만 AI 입장에서는 여러 행동으로 분해됩니다.

```text
재고 조회 → 지난달 데이터 필터링 → 보고서 생성
  → 수신자 확인 → 메일 작성 → 메일 발송
```

이 과정에는 **서로 다른 위험 수준**이 존재합니다. 재고 조회는 상대적으로 위험도가 낮습니다. 보고서 생성도 낮습니다. 하지만 외부 메일 발송부터 위험도가 올라갑니다. 만약 보고서 안에 원가 정보나 개인정보가 들어 있다면 더욱 위험합니다.

따라서 Agent는 바로 실행하는 것이 아니라 먼저 **Action Proposal** 을 만들 수 있습니다. `Inventory.Read`, `Report.Generate`, `Mail.Send` 를 제안하고, Policy Engine이 각각을 개별적으로 검사합니다.

## 5. Delegated Authority가 중요한 이유

기업 AI에서 특히 중요한 개념 중 하나가 Delegated Authority, 즉 **위임된 권한**입니다. 사용자가 Agent에게 일을 맡겼다고 해서 사용자의 모든 권한을 AI에게 그대로 넘겨서는 안 됩니다.

예를 들어 CFO가 Finance Agent를 사용한다고 해보겠습니다. CFO는 회사의 거의 모든 재무 데이터를 볼 수 있다고 가정해보겠습니다. 그렇다고 Finance Agent에게 같은 권한을 줄 필요는 없습니다.

| | CFO | Finance Agent |
|---|---|---|
| 재무정보 조회 | 가능 | 가능 |
| 보고서 생성 | 가능 | 가능 |
| 예산 변경 | 가능 | **차단** |
| 송금 승인 | 가능 | **차단** |
| 계좌 변경 | 가능 | **차단** |

이것이 위임 권한입니다. **인간의 권한과 AI의 권한을 분리하는 것**입니다.

그리고 Agent가 다른 Agent를 호출한다면 문제가 한 단계 더 복잡해집니다.

```text
사용자 → Finance Agent → Research Agent → ERP Tool
```

이때 Research Agent는 누구의 권한으로 ERP에 접근하는가? Finance Agent의 권한인가, 최초 사용자의 권한인가, 별도의 서비스 계정인가? 이 문제를 명확히 정의하지 않으면 기업 AI가 커질수록 권한 구조가 매우 복잡해질 가능성이 높습니다.

## 6. Human-in-the-loop는 모든 업무에 동일하게 적용하면 안 된다

AI를 통제한다고 하면 흔히 모든 작업에 사람이 승인하는 방식을 생각합니다. 하지만 그렇게 하면 생산성이 크게 떨어집니다. AI를 사용하는 이유 자체가 사라질 수도 있습니다.

따라서 Human-in-the-loop는 **위험 기반으로 설계**하는 것이 더 현실적입니다.

| 위험 | 업무 예시 | 사람의 개입 |
|---|---|---|
| **낮음** | 사내 보고서 초안, 회의 요약, 문서 검색 | 자동 실행 |
| **중간** | 상품 추천, 분석 보고서, 내부 이메일 | 샘플 검증 또는 조건부 승인 |
| **높음** | 고객 이메일, 외부 데이터 전송, 계약서 생성 | 수신자·내용 검증 |
| **매우 높음** | ERP 주문 생성, 대규모 구매, 계좌 변경, 송금, 개인정보 대량 처리 | 명시적 승인 |

그래서 Human-in-the-loop의 핵심 기준은 "AI가 모든 과정을 설명할 수 있느냐"만으로 잡으면 안 됩니다. 오히려 더 실용적인 질문은 이것입니다.

> **AI가 실패했을 때 피해 규모가 얼마나 큰가?**

![Delegated Authority와 승인 흐름 — AI Agent의 업무 수행 7단계](/assets/images/agent-authority-03-delegated-authority-approval.jpg)

## 7. 입출력만 통제하면 충분하지 않다

LLM 기반 시스템을 만들다 보면 자주 나오는 생각이 있습니다. "Input을 잘 정의하고 Output Schema를 잘 만들면 가운데 AI는 어느 정도 자유롭게 두어도 되지 않을까?"

프로토타입에서는 가능합니다. 하지만 기업 시스템에서 실제 Action을 수행한다면 문제가 달라집니다. 예를 들어 AI가 다음 JSON을 만들었다고 생각해보겠습니다.

```json
{
  "vendor": "ABC",
  "amount": 120000000,
  "action": "purchase"
}
```

JSON 형식에는 아무 문제가 없습니다. Output Parser도 정상적으로 통과할 수 있습니다. 하지만 **사용자의 구매 한도가 1천만원이라면 이 Action은 실행되어서는 안 됩니다.**

따라서 Enterprise AI에서 중요한 개념은 **Deterministic Action Boundary** 입니다. AI Reasoning 자체는 확률적으로 동작하더라도, 실제 시스템의 상태를 바꾸는 순간에는 결정론적인 검증이 들어가야 합니다.

```text
Input → LLM Reasoning → Action Proposal
  → Policy Validation → Business Rule → Risk Check
  → Approval → Execution → Audit
```

## 8. 그다음 문제는 ERP와 MES를 어떻게 연결할 것인가

이 아이디어가 실제 사업이 되려면 매우 현실적인 문제가 하나 등장합니다. **기업마다 시스템이 다릅니다.** 예를 들어 재고조회만 하더라도 시스템마다 API가 다를 수 있습니다.

| 시스템 | API |
|---|---|
| ERP A | `get_inventory()` |
| ERP B | `stock_query()` |
| MES A | `fetch_material_status()` |
| MES B | `get_stock()` |

AI Agent에게 매번 "이번 회사에서는 어떤 API를 써야 하지?"를 판단하게 하는 구조는 운영 안정성이 떨어질 수 있습니다. 그래서 여기서 중요한 것이 **Canonical Capability Layer** 입니다.

## 9. 시스템 API가 아니라 Capability를 표준화한다

AI Agent에게 시스템별 API를 직접 노출시키는 대신, 기업 업무를 **표준 Capability** 로 정의할 수 있습니다.

```text
Inventory.Read          PurchaseOrder.Read
Inventory.Update        PurchaseOrder.Create

ProductionPlan.Read     Customer.Lookup
ProductionPlan.Update   Mail.Send
```

이렇게 해두면 Agent는 어떤 ERP가 연결되어 있는지 몰라도 됩니다. Agent는 그냥 `Inventory.Read` 를 호출하고, 그 밑에서 Adapter가 실제 시스템의 API로 변환합니다.

```text
Agent
  │  Inventory.Read
  ↓
Capability Layer
  ↓
Adapter
  ├─ ERP A → get_inventory()
  ├─ ERP B → stock_query()
  └─ MES A → fetch_material_status()
```

즉 **시스템의 차이는 Adapter가 흡수하고, 업무의 의미는 Capability가 담당하는 구조**입니다. 단순 Connector 숫자보다 Capability Model + Policy Engine + Adapter Framework가 제품 IP가 되어야 한다는 점이 중요합니다.

![Capability 모델과 Legacy Adapter 전략 — Connector 개수보다 중요한 것](/assets/images/agent-authority-04-capability-and-adapter.jpg)

## 10. Connector를 많이 만드는 회사가 되면 안 되는 이유

처음 고객을 구축하면 대부분 커스텀이 많을 수밖에 없습니다. ERP A, MES A, 그룹웨어를 연결합니다. 두 번째 고객은 또 다릅니다. ERP B, MES B, CRM B입니다.

이때 고객마다 모든 것을 새로 개발하면 **사업은 커질 수 있지만 제품은 커지지 않습니다.** 결국 이런 구조가 됩니다.

```text
고객 증가 → 개발자 증가 → 커스텀 코드 증가
  → 유지보수 증가 → 매출 증가 → 비용도 함께 증가
```

전형적인 SI 구조입니다. 따라서 고객이 늘어날수록 반대 방향으로 가야 합니다.

```text
Custom Code        ↓
Reusable Adapter   ↑
Capability         ↑
Policy Template    ↑
Evaluation Data    ↑
```

초기 고객에서 `80% Custom / 20% Reusable` 이었다면, 몇 번째 고객부터는 `20% Custom / 80% Reusable` 이 되어야 합니다. 그래야 플랫폼이 됩니다.

이를 판단할 핵심 지표도 매출 하나가 아닙니다. **Custom Code %, Reusable Component %, Integration Lead Time, Maintenance Cost, Gross Margin** 을 같이 봐야 합니다.

## 11. 그렇다면 실제로 무엇을 팔 것인가

사업모델은 몇 단계로 나눠볼 수 있습니다.

| 단계 | 수익원 | 내용 |
|---|---|---|
| **1** | Initial Integration Fee | 첫 도입 구축비. ERP·MES·그룹웨어 연결, 초기 PoC 포함 |
| **2** | Annual Platform License | Control Plane 자체 라이선스. Agent Registry, Policy Engine, Capability Registry, Audit |
| **3** | Connector / Industry Pack | ERP·MES Connector, 산업별 Capability Pack |
| **4** | Active Agent / Action Usage | 운영 Agent 수 또는 Action 호출량 기준 과금 |
| **5** | Governance / Audit Package | 감사로그, 실행이력, 권한 변경 이력, 승인, Agent Lifecycle, 컴플라이언스 리포팅 |

산업별 Capability 세트는 이렇게 달라질 수 있습니다.

| 제조업 | 건설업 |
|---|---|
| `Inventory.Read` | `Defect.Read` |
| `ProductionPlan.Read` | `Defect.Update` |
| `ProductionPlan.Update` | `Complaint.Read` |
| `Quality.Read` | `Complaint.Assign` |
| `Quality.Register` | `Vendor.Assign` |
| `Maintenance.Create` | `Payment.Request` |

대기업에서는 오히려 5번 Governance 항목이 중요해질 수 있습니다.

## 12. GTM은 범용 IAM보다 Vertical에서 시작하는 편이 현실적이다

이 사업이 실제로 시작된다면 "모든 기업의 AI Agent를 관리하는 플랫폼입니다"라고 시작하는 것은 너무 넓습니다. 조금 더 현실적인 접근은 **"ERP·MES를 사용하는 기업에서 AI Agent의 실행 권한을 통제합니다"** 정도가 될 수 있습니다.

특히 제조업이나 건설업처럼 **기존 시스템이 많고 업무 권한이 명확한 산업**이 초기 진입점이 될 수 있습니다.

예를 들어 제조기업과 PoC를 한다면 MES + ERP + Groupware를 연결하고, Production Agent · Procurement Agent · Quality Agent를 올립니다. 그리고 Capability Pack + Policy Template + Legacy Adapter까지 함께 구축합니다.

그러면 고객사는 단순 챗봇을 사는 것이 아니라, **기존 업무 시스템 위에서 실제 행동할 수 있는 AI 운영체계**를 도입하게 됩니다.

![수익모델 · GTM · 장기 해자 — 어떻게 돈을 벌고 무엇이 누적 해자가 되는가](/assets/images/agent-authority-05-revenue-gtm-moat.jpg)

## 13. 이 사업에서 AI 사원증 자체는 해자가 아니다

AI 사원증 UI는 쉽게 만들 수 있습니다. 조직도도 쉽게 만들 수 있습니다. Agent 이름, 부서, 역할을 표시하는 것도 어렵지 않습니다. 따라서 그것만으로는 장기적인 경쟁력이 되기 어렵습니다.

실제 해자는 **고객을 구축하면서 생기는 자산**에 있습니다.

| 고객 수 | 축적되는 것 |
|---|---|
| 1 | Adapter 생성, Capability 생성, Policy 생성 |
| 10 | Adapter 축적, Capability 축적, Policy Template 축적 |
| 50 | Audit Data 축적, Evaluation Data 축적, Industry Pattern 축적 |

결국 경쟁력은 다음과 같은 조합에서 만들어질 가능성이 높습니다.

```text
Enterprise Integration + Validated Policy Graph
  + Domain Capability + Domain Ontology
  + Workflow History + Evaluation Data + Partner Network
```

즉 Ontology 하나가 해자가 되는 것도 아니고, Connector 숫자만 많다고 해자가 되는 것도 아닙니다. **실제 기업 업무를 AI가 수행하면서 축적되는 Integration Context** 가 해자에 가깝습니다.

## 14. 최종적으로 내가 그리고 있는 제품

정리하면 처음 아이디어는 `AI 조직도 + AI 사원증` 이었습니다. 하지만 실제 제품 구조는 다음까지 내려가야 합니다.

```text
Identity + Agent Registry + Organization Graph
  + Delegated Authority + Capability Registry
  + Policy Engine + Action Gateway + Approval + Audit
```

그리고 다시 기존 기업 시스템으로 연결됩니다.

```text
Human → AI Agent → AI Workforce Control Plane
      → ERP / MES / CRM / KMS / Groupware
```

중요한 것은 ERP나 MES를 AI로 다시 만드는 것이 아닙니다. 기존 시스템은 그대로 둡니다. 대신 그 위에 **AI가 기업의 권한 안에서 실제 업무를 수행할 수 있는 새로운 Control Layer** 를 만드는 것입니다.

## 마무리

앞으로 기업에는 수십 개, 많게는 수백 개의 AI Agent가 들어갈 수 있습니다. 영업 Agent가 생기고, 구매 Agent가 생기고, 생산 Agent가 생기고, 재무 Agent가 생길 수 있습니다.

그 순간 기업은 새로운 문제를 만나게 됩니다.

> 이 AI는 누구인가?
> 누구의 지시를 받고 있는가?
> 어떤 정보를 볼 수 있는가?
> 어떤 일을 할 수 있는가?
> 어디까지 자동으로 실행할 수 있는가?
> 문제가 생기면 누가 책임지는가?
> 모든 행동을 추적할 수 있는가?

그래서 저는 **'AI에게도 사원증이 필요하다'** 는 표현이 좋은 출발점이라고 생각합니다. 다만 그것은 제품을 **설명하는 메시지**입니다. 실제 비즈니스의 중심은 더 깊은 곳에 있습니다.

> AI 조직도는 좋은 UX다.
> AI 사원증은 좋은 메시지다.
> 하지만 기업이 실제로 돈을 지불할 가능성이 높은 것은
> **AI의 Identity가 아니라 Authority와 Action을 통제하는 시스템이다.**

기업에 AI Agent가 본격적으로 들어오기 시작한다면, 앞으로 필요한 것은 단순한 AI 관리 화면이 아닐지도 모릅니다. 사람과 AI가 함께 일하는 기업을 위한 **새로운 권한 운영체제**. 저는 그것을 **Enterprise Agent Identity & Authority Layer**, 또는 조금 더 넓게는 **AI Workforce Control Plane** 이라고 부를 수 있다고 봅니다.
