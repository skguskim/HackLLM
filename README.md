# HackLLM

<div align="center">
    <img src="" alt="HackLLM" />
    <p>해킹을 통해 배우는 LLM 보안</p>
    <p>OWASP LLM Top10를 기반으로 한 LLM 취약점 실습 환경</p>
    <a href="https://whs-hackllm.streamlit.app/">
        HackLLM 바로가기
    </a>
</div>

<br />

## 📖 Description | 설명

### OWASP LLM Top10 이란?
생성형 AI·LLM에서 자주 발생하고 치명적인 10대 보안·안전 위험을 정리해 개발자와 보안팀이 대응 우선순위를 세울 수 있도록 돕는 공개 표준 목록

| 번호 | 취약점 명칭                   | 설명 |
|------|------------------------------|------|
| 01   | 프롬프트 인젝션              | 공격자가 입력을 통해, 원래 설정된 시스템 지침이나 보안 제한을 우회하고 모델의 응답을 유도 |
| 02   | 민감 정보 유출               | LLM 출력이나 프롬프트 인젝션을 악용하여 개인 정보, 기밀 데이터, 또는 학습된 모델 내부의 민감 정보를 유출 |
| 03   | 공급망                       | LLM 공급망의 배포 경로를 조작해 악성 모델을 주입하거나 백도어를 심어 LLM의 동작을 통제 |
| 04   | 데이터 및 모델 오염          | LLM fine-tuning 단계에 조작된 데이터를 주입, 모델이 특정 조건에서 편향되거나 악성 출력을 내도록 기능을 왜곡 |
| 05   | 부적절한 출력 처리           | LLM이 생성한 출력을 검증 없이 시스템에 전달하도록 유도하여 XSS, SQL 인젝션, 원격 코드 실행 등의 공격을 실행 |
| 06   | 과도한 위임                  | LLM이 과도한 기능, 권한, 자율성을 부여받은 기능을 통해 사용자 확인 없이 민감한 작업을 수행하도록 유도 |
| 07   | 시스템 프롬프트 유출         | 시스템 프롬프트에 포함된 민감 정보나 내부 규칙을 유출시켜, 권한 상승, 필터 우회 같은 후속 공격을 수행 |
| 08   | 벡터 및 임베딩 취약점        | 벡터 데이터의 취약점을 악용해 민감 정보를 역추적하거나, 검색 결과를 조작하여 LLM의 출력을 왜곡, 기밀성 침해 |
| 09   | 허위 정보                    | LLM이 생성한 허위 정보, 환각으로 인해 사용자가 잘못된 결정을 내리게 하거나 시스템에 보안상 취약한 동작을 유도 |
| 10   | 무제한 소비                  | LLM에 반복적으로 쿼리를 보내 시스템 리소스를 고갈시키거나, 재정적 손실과 지적 재산 침해를 유도 |


<br />

## 📱 Features | 기능

1. 기능 1
    - 이런거 있음

<br />

## ⭐ Contributors | 개발팀
<table style="text-align: center">
    <tr>
        <th style="text-align: center;">[ PM ]<br/>개발</th>
        <th style="text-align: center;">메인 개발</th>
        <th style="text-align: center;">개발</th>
        <th style="text-align: center;">개발</th>
    <tr>
    <tr>
        <td>
            <a href="https://github.com/seokjea" target="_blank"><img src="" alt="seokjea" width="100"></a>
        </td>
        <td>
            <a href="https://github.com/hanataba227" target="_blank"><img src="https://github.com/user-attachments/assets/3f4e5828-9eb2-48b1-9729-cb61bc7c4378" alt="hanataba227" width="100"></a>
        </td>
        <td>
            <a href="https://github.com/esthervery" target="_blank"><img src="" alt="esthervery" width="100"></a>
        </td>
        <td>
            <a href="https://github.com/jeonminju2" target="_blank"><img src="" alt="jeonminju2" width="100"></a>
        </td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <a href="https://github.com/seokjea" target="_blank">seokjea</a>
        </td>
        <td style="text-align: center;">
            <a href="https://github.com/hanataba227" target="_blank">hanataba227</a>
        </td>
        <td style="text-align: center;">
            <a href="https://github.com/esthervery" target="_blank">esthervery</a>
        </td>
        <td style="text-align: center;">
            <a href="https://github.com/jeonminju2" target="_blank">jeonminju2</a>
        </td>
    </tr>
</table>
<table style="text-align: center">
    <tr>
        <th style="text-align: center;">개발</th>
        <th style="text-align: center;">개발</th>
        <th style="text-align: center;">개발</th>
        <th style="text-align: center;">개발</th>
    <tr>
    <tr>
        <td>
            <a href="https://github.com/tellgeniewish" target="_blank"><img src="" alt="tellgeniewish" width="100"></a>
        </td>
        <td>
            <a href="https://github.com/skguskim" target="_blank"><img src="" alt="skguskim" width="100"></a>
        </td>
        <td>
            <a href="https://github.com/haupjun" target="_blank"><img src="" alt="haupjun" width="100"></a>
        </td>
        <td>
            <a href="https://github.com/eclipse0707" target="_blank"><img src="" alt="eclipse0707" width="100"></a>
        </td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <a href="https://github.com/tellgeniewish" target="_blank">tellgeniewish</a>
        </td>
        <td style="text-align: center;">
            <a href="https://github.com/skguskim" target="_blank">skguskim</a>
        </td>
        <td style="text-align: center;">
            <a href="https://github.com/haupjun" target="_blank">haupjun</a>
        </td>
        <td style="text-align: center;">
            <a href="https://github.com/eclipse0707" target="_blank">eclipse0707</a>
        </td>
    </tr>
</table>
<table style="text-align: center">
    <tr>
        <th style="text-align: center;">멘토</th>
        <th style="text-align: center;">PL</th>
    <tr>
    <tr>
        <td>
            <a href="https://github.com/멘토" target="_blank"><img src="" alt="멘토" width="100"></a>
        </td>
        <td>
            <a href="https://github.com/PL" target="_blank"><img src="" alt="PL" width="100"></a>
        </td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <a href="=https://github.com/멘토" target="_blank">멘토</a>
        </td>
        <td style="text-align: center;">
            <a href="https://github.com/PL" target="_blank">PL</a>
        </td>
    </tr>
</table>

<br />

## 🔧 Stack | 기술 스택
[![Streamlit](https://img.shields.io/badge/STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/SUPABASE-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![ChatGPT API](https://img.shields.io/badge/CHATGPT_API-10A37F?style=for-the-badge&logo=openai&logoColor=white)](https://platform.openai.com/docs/api-reference)

<br />

## 🔨 Structure | 구조
![HackLLM 구조도]()


## 🔗 Links
- [화이트햇 스쿨 공식 홈페이지](https://whitehatschool.kr/home/kor/main.do)
