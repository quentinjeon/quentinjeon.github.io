# ChatGPT 이미지 생성 프롬프트 — 3편

본문(`Orchestrator와 Agent Runner를 실제 코드로 구현.md`)을 먼저 ChatGPT에 그대로 붙여넣고,
아래 프롬프트를 하나씩 이어서 요청하면 됩니다.

생성한 이미지는 이 폴더에 아래 이름으로 저장해 주세요. 그대로 블로그에 반영합니다.

```text
01_전체_실행_흐름.png
02_Task_상태_머신.png
03_권한_교집합.png
04_리비전_루프와_에스컬레이션.png
05_이벤트_로그_복원.png
```

---

## 공통 스타일 지시 (첫 요청에 한 번만)

```
지금 붙여넣은 글을 바탕으로 인포그래픽을 만들어줘.

스타일 조건:
- 1536 x 1536 정사각형
- 한국어 텍스트, 오탈자 없이 정확하게
- 네이비(#1B3A6B)와 블루(#2E6FD4) 중심, 배경은 흰색/연회색
- 포인트 컬러는 그린(#1A7F3C) 하나만, 경고는 앰버(#C77700)
- 플랫 아이콘, 그림자 최소화, 선은 얇게
- 좌상단에 라운드 배지로 "PART 3 · Orchestrator & Runner"
- 우상단에 "N/5" 진행 표시
- 최상단에 제목 + 한 줄 부제
- 본문은 카드 박스로 구획을 나누고, 박스마다 소제목 띠를 둘 것
- 코드 폰트가 필요한 부분은 monospace 로
- 장식보다 정보 밀도를 우선. 빈 공간에 의미 없는 일러스트를 넣지 말 것
```

---

## 1/5 — 전체 실행 흐름

```
1/5 이미지를 만들어줘.

제목: "PART 3. 전체 실행 흐름"
부제: "run_id 하나가 Planner → Developer → Reviewer 를 관통한다"

포함할 내용:
- 상단 가로 흐름: 사용자 요청("이 프로젝트 README를 개선해줘")
  → Orchestrator → Planner → Developer → Reviewer → Final Artifact
- 각 Agent 아래에 그 Agent 가 만든 산출물을 작게 표기
  Planner: drafts/plan.md (art-plan-1)
  Developer: drafts/README.v1.md, drafts/README.v2.md
  Reviewer: 판정 결과(반려 → 통과)
- 흐름 전체를 감싸는 띠에 "run_id: run-2026-08-23-001 · 이벤트 31건"
- 하단 카드 3개:
  "Agent 는 서로 대화하지 않는다 — Task 를 받아 Artifact 를 낸다"
  "누구에게 넘길지는 Orchestrator 가 정한다"
  "모든 행동은 이벤트로 기록된다"
- 맨 아래 강조 띠: "312줄 · 프레임워크 없음"
```

---

## 2/5 — Task 상태 머신

```
2/5 이미지를 만들어줘.

제목: "PART 3. Task 상태 머신"
부제: "허용된 전이만 통과한다. 나머지는 코드가 거부한다"

포함할 내용:
- 중앙에 상태 전이도
  CREATED → READY → RUNNING → REVIEW → COMPLETED
  REVIEW → REVISION → RUNNING (되돌아가는 화살표)
  RUNNING → FAILED, 각 단계 → BLOCKED
- COMPLETED 와 FAILED 는 "종료 상태"로 표시하고
  나가는 화살표가 없다는 점을 시각적으로 강조(자물쇠 아이콘 등)
- 우측에 실제 코드 카드(monospace):
  ALLOWED = {
      CREATED:  {READY, BLOCKED},
      READY:    {RUNNING, BLOCKED},
      RUNNING:  {REVIEW, FAILED, BLOCKED},
      REVIEW:   {COMPLETED, REVISION},
      REVISION: {RUNNING},
      BLOCKED:  {READY, FAILED},
      COMPLETED: set(),
      FAILED:    set(),
  }
- 하단 경고 카드(앰버):
  "CREATED → COMPLETED 는 예외를 발생시킨다
   IllegalTransition: CREATED → COMPLETED 는 허용되지 않는다"
- 맨 아래 강조 띠: "그림은 어겨도 아무 일도 없다. 표는 어기면 예외가 난다"
```

---

## 3/5 — 권한 교집합

```
3/5 이미지를 만들어줘.

제목: "PART 3. 권한은 선언이 아니라 교집합이다"
부제: "워크스페이스 허용 ∩ Agent 요구 = 실제 실행 권한"

포함할 내용:
- 중앙에 벤다이어그램 2개
  왼쪽 원: WORKSPACE_GRANTS = { fs.read, fs.write, fs.list }
  오른쪽 원: AGENT_REQUESTS (developer) = { fs.read, fs.write }
  교집합 부분을 그린으로 강조하고 "실제 실행 권한" 이라고 표기
- 우측에 Agent 별 권한 표
  planner    요구 fs.read, fs.list    → 허용 fs.read, fs.list
  developer  요구 fs.read, fs.write   → 허용 fs.read, fs.write
  reviewer   요구 fs.read             → 허용 fs.read
- 하단 카드(앰버 경고):
  "워크스페이스가 fs.write 를 회수하면
   developer 정의에 fs.write 가 남아 있어도 차단된다
   PermissionDenied: developer 는 fs.write 권한이 없다"
- 맨 아래 강조 띠: "권한의 최종 결정권은 Agent 가 아니라 워크스페이스에 있다"
```

---

## 4/5 — 리비전 루프와 에스컬레이션

```
4/5 이미지를 만들어줘.

제목: "PART 3. 리비전 루프와 에스컬레이션"
부제: "while True 를 쓰되 탈출구를 먼저 만든다"

포함할 내용:
- 중앙에 순환 흐름
  RUNNING(Developer 작성) → REVIEW(Reviewer 판정)
  → 통과면 COMPLETED
  → 반려면 REVISION → RUNNING 으로 복귀
- 실제 판정 결과를 표로 함께 표시
  1차: 설치 O · 사용법 O · 라이선스 X → 반려
  2차: 설치 O · 사용법 O · 라이선스 O → 통과
- 버전이 덮어써지지 않고 쌓이는 것을 시각화
  README.v1.md (반려됨) / README.v2.md (통과) 를 나란히, v1 도 보존됨을 표시
- 우측 하단 카드(앰버):
  "MAX_REVISION 초과 시 FAILED 가 아니라 BLOCKED
   escalated_to_human 이벤트 기록 → 사람 판단으로 넘김"
- 맨 아래 강조 띠: "반려된 초안도 증거로 남는다"
```

---

## 5/5 — 이벤트 로그로 실행 복원

```
5/5 이미지를 만들어줘.

제목: "PART 3. 이벤트 로그 하나로 실행을 복원한다"
부제: "replay.py 는 메모리를 보지 않는다. 로그만 읽는다"

포함할 내용:
- 좌측: 이벤트 로그 스트림을 monospace 카드로
  seq 1  run_started
  seq 2  task_created    (granted: fs.list, fs.read)
  seq 3  task_state_changed  CREATED → READY
  seq 5  tool_called     fs.read  README.md
  seq 6  artifact_created  art-plan-1  v1
  ... (총 31건)
- 우측: 그 로그에서 복원되는 7개 질문과 답
  1 Task 2개
  2 Agent 3종 (planner 8 · developer 16 · reviewer 5)
  3 Tool 호출 7회
  4 Artifact 3개 (v1 · v2 보존)
  5 Reviewer 검토 2회 (반려 → 통과)
  6 Revision 1회
  7 run_id 1개 · seq 연속
- 두 영역을 화살표로 연결하고 가운데에 "run_id" 키 아이콘
- 맨 아래 강조 띠: "로그는 나중에 물어볼 질문을 미리 정해야 설계된다"
```

---

## 생성 후

이미지 5장을 이 폴더에 위 파일명으로 저장한 뒤 알려주세요.
본문 각 섹션에 배치하고 블로그를 갱신하겠습니다.

| 이미지 | 배치될 섹션 |
|---|---|
| `01_전체_실행_흐름.png` | 도입부 (무엇을 만들었는가) |
| `02_Task_상태_머신.png` | 1. 상태 전이를 표로 박아둔다 |
| `03_권한_교집합.png` | 2. 권한은 선언이 아니라 교집합이다 |
| `04_리비전_루프와_에스컬레이션.png` | 5. 루프에는 상한이 있어야 한다 |
| `05_이벤트_로그_복원.png` | 7. 7개 질문에 답하기 |
