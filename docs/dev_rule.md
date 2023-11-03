## Branch Rule

> **main**: PR만 가능한 branch, PR시 자동으로 배포하는 github action 실행<br/>
> **dev**: 실제 개발 브랜치, PR은 이곳으로 하고 로컬 테스트를 한다.<br/>
> **feat/<기능>**: clone후 작업해야할 브랜치, 이런 이름의 브랜치를 파고 작업후 dev로 PR한다.<br/>
> **hotfix/<수정내용>**: 긴급한 수정내용인 경우 main에서 새로 분기하여 작업해 merge한다.<br/>

## 작업 후 PR 방법
feat/<기능 내용>에서 작업한 후 아래 내용 실행
```sh
git pull upstream dev # 달라진 내용 있으면 반영
git checkout -b dev
git merge feat/<기능 내용>
```
이후 깃허브로 이동후 PR 보내기


## Commit Convention

> Type: subject
>
> Body
>
> Footer(이슈 트랙시 사용)
>
> ---
> example
>
> feat: add login decorator
> - add decorator in utils.py
> - add docstring
>
> issue #31

## Type
- feat: 새로운 기능 추가 작업
- fix: 버그 수정
- style: 코드 변경 없이 포맷만 변경한 경우
- refactor: 코드 리팩토링
- docs: 문서 수정
- rename: 코드변경 없이 파일 명 수정
- remove: 파일/코드 삭제할 경우
- comment: 주석 추가
- test: 테스트 코드 추가
- chore: 빌드 관련 파일 수정, 패키지 추가 및 수정
- WIP: 작성중 잠시 push가 필요한 경우 사용(비권장)


## Python Code Style
- 함수명, 변수명 : snake case
- 클래스명 : Pascal case
