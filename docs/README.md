
# 시스템 개요

## v0
![](./img/aid_v0_system.png)

## 화면
<p align=center>
    <img src="./img/aid_v0_home.png" width=400/>
    <img src="./img/aid_v0_submit.png" width=400/>
</p>
<p align=center>
    <img src="./img/aid_v0_mail.png" width=400/>
    <img src="./img/aid_v0_admin.png" width=400/>
</p>


## v1
![](./img/aid_v1_system.png)

---

# Test 방법

```sh
# 파일 생성
backend/env/.server.env
    mongo_user=admin_user
    mongo_password=password
    mongo_host=db
    mongo_port=27017
    SECRET_KEY=***
    REFRESH_SECRET_KEY=***
    email_id=***
    email_pw=***(앱 비밀번호)

backend/env/.db.env
    MONGO_INITDB_ROOT_USERNAME=admin_user
    MONGO_INITDB_ROOT_PASSWORD=password


docker compose up -d
```
