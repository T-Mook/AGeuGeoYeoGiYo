# 목표
* 뉴스 크롤러를 누구나 실행할 수 있도록 실행기로 만듭니다

## 실행
```bash
# 가상환경 설치
$ python -m venv .venv
# 가상환경 실행
$ . .venv/bin/activate # (Mac OS)
$ .venv/Scripts 폴더 내 activate 실행 # (Window OS)
# 필요 라이브러리 설치
$ python -m pip install -r requirements.txt
# 실행
$ python run.py
```

## 환경
```bash
# 신규 라이브러리 설치 후 환경 저장
$ pip freeze > requirements.txt
```

# Build
```bash
# pyinstaller 설치
$ pip install pyinstaller

# build
# --onfile : 단일 파일로 생성
# --noconsole : console 창 띄우지 않도록 설정
$ pyinstaller --onefile --noconsole --icon=icon.ico run.py
```
* 2021.2.3
   * 페이지 수는 1~5페이지 크롤링으로 제한되어 있습니다.
* 2021.1.30 (Done !)
   * path 지정 기능이 없습니다. 제작된 위치에서 실행하지 않으면 에러로 실행되지 않습니다. 그렇지 않은 경우에는 정상적으로 실행됩니다.