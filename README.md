main.py 시작전 아래의 환경변수를 설정하고 구동하면 됩니다.
set POSTGRESQL_USER=사용자
set POSTGRESQL_PASSWORD=비밀번호
set POSTGRESQL_SERVER=서버주소
set POSTGRESQL_PORT=포트번호
set POSTGRESQL_DB=디비명

macos, linux 에서는 일반유저는 80번 포트를 열수 없으므로 sudo 을 앞여 붙여줘야 합니다.

>sudo python main.py
