# 시스템 개요도

![](./img/system.png)


---

# Test 방법

```sh
# 파일 생성
env/.server.env
    mongo_user=admin_user
    mongo_password=password
    mongo_host=localhost
    mongo_port=27017
    email_id=***
    email_pw=***(앱 비밀번호)

env/.db.env
    MONGO_INITDB_ROOT_USERNAME=admin_user
    MONGO_INITDB_ROOT_PASSWORD=password


docker compose up -d
```
