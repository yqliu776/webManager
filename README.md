## WebManager
### 
### build db with docker
```powershell
docker run --name mysql-5.7 \
-p 3306:3306 \
-v D:\devTools\Docker\DockerData\mysql57/data:/var/lib/mysql \
-v D:\devTools\Docker\DockerData\mysql57/logs:/var/log/mysql \
-v D:\devTools\Docker\DockerData\mysql57/conf:/etc/mysql/conf.d \
-e MYSQL_ROOT_PASSWORD=090910 \`
--restart=always \
-d mysql:5.7
```
#### Then put web_manager.sql in your database.

#### To change the db modules
1. flask db init
2. flask db migrate
3. flask db upgrade
#### Add your packages with
pip freeze > requirements.txt
#### Run this before run.py
pip install -r requirements.txt