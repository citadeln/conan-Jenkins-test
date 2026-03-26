## Usful commands

### Как делать бэкапы красивые

rsync /backup jenkins_home — это бэкап директории с конфигом Jenkins,

docker run / docker-compose.yml + Jenkinsfile — это инфраструктура в коде, которые хранятся в Git.

1. Бэкап jenkins_home через rsync
Предположим, Jenkins у тебя запущен так:

```bash
docker run -v jenkins_home:/var/jenkins_home ...
```
Docker хранит jenkins_home в своём volume. Чтобы его бэкапить, удобно заранее смонтировать его в папку, либо использовать volume‑директорию.

1.1. Создай папку бэкапа
```bash
mkdir ~/backup
```
1.2. Копируй jenkins_home через rsync

Если у тебя есть доступ к содержимому volume‑папки (например, через контейнер‑копию, см. ниже) или ты используешь прямую docker run -v ~/jenkins_home:/var/jenkins_home, то:

```bash
rsync -av ~/jenkins_home/ ~/backup/jenkins_home/
```
Если используешь Docker‑volume, можно делать так:

```bash
docker run --rm -v jenkins_home:/input:ro \
  -v ~/backup:/backup \
  alpine:latest \
  tar czf /backup/jenkins_home_$(date +%Y%m%d_%H%M%S).tar.gz -C /input .
```
Это делает «снимок» Jenkins в архиве внутри ~/backup.

2. Хранить docker run / docker-compose.yml и Jenkinsfile в Git
Это и есть твой Mini‑DevOps‑стек.

2.1. Создай репозиторий
bash```
mkdir ~/devops-lab
cd ~/devops-lab
git init
Добавь файлы:

docker-compose.yml (или docker-run-notes.md, если предпочитаешь живой docker run).

Jenkinsfile — pipeline для твоего C++‑проекта.

README.md — короткая инструкция, как запустить.

Пример docker-compose.yml:

text
version: '3.8'

services:
  jenkins:
    image: jenkins/jenkins:lts-jdk17
    container_name: jenkins
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
    restart: unless-stopped

volumes:
  jenkins_home:
2.2. Закомить в Git
bash```
git add docker-compose.yml Jenkinsfile README.md
git commit -m "Initial Jenkins + Docker setup"
Если хочешь, залей в GitHub/GitLab:

```bash
git remote add origin https://github.com/monroe/my-devops-lab.git
git push -u origin main
3. Как это выглядит в практике
Перед экспериментом:

git pull → обновляешь локальный docker-compose.yml и Jenkinsfile;

делаешь ~/backup_jenkins.sh → резервная копия jenkins_home сохранена.

После эксперимента (или если всё сломалось):

останавливаешь Jenkins:

```bash
docker stop jenkins
docker volume rm jenkins_home
восстанавливаешь данные:

```bash
docker volume create jenkins_home
docker run --rm -v jenkins_home:/target -v ~/backup:/backup \
  alpine:latest \
  tar xzf /backup/jenkins_home_*.tar.gz -C /target
заново запускаешь Jenkins:

```bash
docker-compose up -d
если Jenkins‑конфиг сломан навсегда — можно заново создать джобы по Jenkinsfile из Git.

4. Профессиональность для сеньоров
rsync + бэкап jenkins_home — базовый, но корректный подход; сеньоры обычно автоматизируют это через cron и контроль за местом хранения, а также через инструменты вроде restic / borg.

docker-compose.yml и Jenkinsfile в Git — это уже инфраструктура как код, стандартный DevOps‑паттерн:

можно развернуть Jenkins в любом окружении,

можно тестировать пайплайны через CI/CD,

можно откатывать изменения на уровне Git‑коммитов.

То есть то, что ты сейчас делаешь, — это классический начальный DevOps‑стек, а не «детские снэпшоты» — в перспективе именно так работают с CI/CD‑инстансами.