# 아그거여기요(AGeuGeoYeoGiYo)
* 버전 : `v.0.1.0`
* 목표 : 다중 플랫폼 뉴스 크롤러를 누구나 쉽게 경험하게 만듭니다.
* Who's TMook ([링크](https://t-mook.github.io/))

# 1. 사용
## 1-1. 실행 파일
* [다운로드 링크](https://drive.google.com/drive/folders/1oF4hMcvKRIiYEw_87Y89Hxgk3grhA5sZ?usp=sharing)
   * 더블 클릭이면 실행할 수 있는 파일을 다운로드 가능한 구글 드라이브로 연결됩니다.
   * 안에 있는 파일(`AGeuGeoYeoGiYo_TMook_v.0.0.0_alpha.exe`)을 다운로드 받으세요

## 1-2. 실행
1. 다운받은 실행 파일(`AGeuGeoYeoGiYo_TMook_v.0.0.0_alpha.exe`)를 실행합니다.
   * (Windows의 경우) 파일 실행 시 미확인된 앱이라며 경고가 등장할 수 있습니다.
      * '추가 정보'를 누르고 '실행'을 누르시면 실행됩니다.
      * 구글 드라이브에서 다운로드 시 바이러스 검사를 하지만 불안하시다면 ~~제가 못 미더울 수 있죠...~~ 실행하지 않으셔도 좋습니다 ㅜㅜ
2. `검색어`를 입력하고
3. `페이지 수`를 _1~5개_ 중에 선택한 후
4. `검색` 버튼을 누릅니다.
   * _**버튼 아래 주의사항(붉은 글씨와 그 아래)을 반드시 숙지해주세요!**_
6. `AGeuGeoYeoGiYo_TMook~.exe` 파일이 있는 현재 폴더에 검색결과가 `.excel` 파일로 저장됩니다.
   * 파일명은 `keyword_search_results_검색어_시간` 형태입니다.

## 1-3. 크롤링 대상
1. 네이버 뉴스
2. 다음 뉴스
3. 구글 뉴스
4. 네이버 VIEW (구 블로그)

# 2. 개발
## 2-1. 실행
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

## 2-2. 환경
```bash
# 신규 라이브러리 설치 후 환경 저장
$ pip freeze > requirements.txt
```

## 2-3. Build
```bash
# pyinstaller 설치
# requirements.txt 통한 설치를 마쳤다면 설치되어 있습니다
$ pip install pyinstaller

# build
# --onfile : 단일 파일로 생성
# --noconsole : console 창 띄우지 않도록 설정
$ pyinstaller --onefile --noconsole --icon=icon.ico run.py
```

## 2-4. Git
```
git config commit.template .github/GIT_COMMIT_TEMPLATE
```

# 3. 업데이트 내역
* v 0.1.0 - 네이버 VIEW, 다음 블로그 크롤링 추가
  * 네이버 VIEW는 약 30여개가 고정적 크롤링 (페이지 수에 영향받지 않음)
    * 페이지 형태로 이루어져 있지 않기 때문입니다
* v 0.0.0 - 네이버, 다음, 구글 뉴스 크롤링 및 excel 파일 저장 실행기