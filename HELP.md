## Below is a set of information to assist with development at ARPAKIT Company

Note: This is not related to arpakitlib, it is just a collection of helpful information

### Emoji

- https://www.prosettings.com/emoji-list/

### Timezones

- https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568

### Docker help

- https://www.ionos.com/digitalguide/server/configuration/install-docker-on-ubuntu-2204/

```
sudo apt update
sudo apt upgrade
sudo apt install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo groupadd docker
sudo usermod -aG docker $USER

docker ps -a
docker stop $(docker ps -a -q)
docker container rm $(docker ps -a -q)
docker rmi $(docker images -a -q)
docker stop $(docker ps -a -q) && docker container rm $(docker ps -a -q)
docker stop $(docker ps -a -q) && docker container rm $(docker ps -a -q) && docker rmi $(docker images -a -q)
docker build -p 8080:8080 -t tagname -f Dockerfile .
docker stats


docker rm ...
docker run --name ... -d -p ...:5432 -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_DB=... postgres:16 -c max_connections=100
docker start ...
```

### Systemd help

```
[Unit]
Description=...
After=network.target

[Service]
User=...
WorkingDirectory=...
ExecStart=...
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target

sudo systemctl start ...
sudo systemctl stop ...


[Unit]
Description=divar_site

[Service]
User=divar_site
WorkingDirectory=/home/divar_site/divar_site
Environment=PATH=/home/divar_site/.nvm/versions/node/v18.16.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
ExecStart=/bin/bash -c "npm run start"
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx help

```
sudo apt update
sudo apt install nginx
systemctl start nginx
systemctl stop nginx
systemctl restart nginx

server {
    listen 80;
    listen [::]:80;

    server_name ...;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:...;
    }
}
```

### Poetry help

- https://python-poetry.org/docs/

```
curl -sSL https://install.python-poetry.org | python3 -
# After downloading u should update .profile, bashrc etc...
exec "$SHELL"
# export PATH="$HOME/.local/bin:$PATH"
poetry config virtualenvs.in-project true
poetry self add poetry-plugin-export
poetry self update

poetry env use ...
poetry install
poetry update

pyproject.toml
package-mode = false

poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi ...
poetry publish --build --repository testpypi
poetry source add --priority=explicit testpypi https://test.pypi.org/legacy/
poetry config pypi-token.pypi <your-pypi-token>

poetry export -f requirements.txt --without-hashes --output requirements.txt

poetry cache clear pypi --all

export TWINE_HTTP_TIMEOUT=60
poetry publish

poetry cache clear --all PyPI
```

### Pyenv help

- https://kfields.me/blog/pyenv_on_ubuntu_22

```
sudo apt update
sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
curl https://pyenv.run | bash
# After downloading u should update .profile, bashrc etc...
# export PYENV_ROOT="$HOME/.pyenv"
# [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
exec "$SHELL"
pyenv install ...
pyenv versions
```

### Certbot help

```
sudo apt install snapd -y
sudo snap install --classic certbot
su - root

certbot --nginx -d "a.domain.com" -d "b.domain.com"
sudo certbot certificates
```

### Proxy example help

```
socks5://user:passwd@hostname:port
https://user:passwd@hostname:port
```

### PostgreSQL help

- https://selectel.ru/blog/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04/

```
# install postgresql
sudo apt install postgresql postgresql-contrib
sudo apt install postgresql-client
sudo systemctl start postgresql.service
sudo systemctl status postgresql.service
sudo -i -u postgres
psql
\conninfo - info
\q - exit
\list - databases
\du - users
createuser --interactive --pwprompt
createdb -U postgres ...
ALTER ROLE username WITH PASSWORD 'newpassword';
sudo nano /etc/postgresql/<версия>/main/pg_hba.conf
host    all             all             0.0.0.0/0               md5
sudo nano /etc/postgresql/<версия>/main/postgresql.conf
listen_addresses = '*'
#port = 5432
CREATE USER ... WITH PASSWORD '...';
ALTER USER ... WITH SUPERUSER;
CREATE DATABASE ... OWNER '...';

# postgresql db url, db_url
postgresql://username:password@host:port/database_name

# postgresql pg_dump
pg_dump -U postgres -h localhost -t <имя_таблицы> mydb > table_dump.sql
pg_dump -U ... -h ... ... -p ... > ...

# postgresql db_restore
pg_restore -U ... -h ... -p ... -d ... ....dump

```

### Install Python from apt help

```
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.12
sudo apt install python3.12-venv

# create venv with python
python3 -m venv .venv
```

### Git help

```
git remote -v
git remote remove origin_name
git remote add origin_name URL
git remote set-url origin_name URL
git remote rename old new
git fetch --all
git branch -r
git branch -a
```

### Linux help

```
free -h проверка оперативной памяти
df -h - проверка постоянной памяти
nano /etc/apt/sources.list.d
deluser --remove-home user
adduser user
usermode -aG sudo user
```

### Swagger-ui, /docs help

- https://github.com/swagger-api/swagger-ui (folder dist for download static docs)

### npm, nvm help

- https://github.com/nvm-sh/nvm
- https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04

```
# install nvm, npm, node (https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
exec "$SHELL"
npm -v
nvm current
nvm ls
nvm list-remote
nvm install --lts
nvm use ...
npm install
npm run build
npm run start
```

### Xray help

- https://github.com/XTLS/Xray-install

```
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install-geodata
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ remove
```

### Celery help

```
celery -A app worker --loglevel=info -Q queue_name -c 1 -n worker_name &
celery -A app beat --loglevel=info &
wait
```

### Licence help

- https://choosealicense.com/

---