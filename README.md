
# Book catalog web app

Web app with book catalog:
- guests have read only permissions
- logged in users can edit catalog's content (CRUD in PostgreDB)

This README covers only deployment of the project to AWS instance with:
-pipenv
-Gunicorn
-Nginx

For detailed deployment please refer to [README for master branch](https://github.com/diSciPy/Book_catalog#readme)

## Deployment

### AWS instance with pipenv:

To deploy web app on AWS EC2 with Unit file for Gunicorn and Nginx:
1. Create virtual envrinonment with pipenv:
In app directory (in my case it's Book-catalog)
```bash
python3.9 -m pipenv shell
```
2. Based on requirements.txt pipenv should've created Pipfile for you.If not, run:
```bash
python3.9 -m pipenv install
```
or 
```bash
python3.9 -m pipenv install -r path/to/requirements.txt
```
3. Create Pipfile.lock
```bash
python3.9 -m pipenv lock
```
4. Run webapp from pipenv:

```bash
python3.9 -m pipenv run python3.9 run.py
```


## Unit file for Gunicorn

Create unit file for web app service using gunicorn:

```bash
  sudo vim /etc/systemd/system/<name of the service>.service
```
Run command to start webapp service:

```bash
  sudo systemctl start <service_name - foreignlit>
```
Manage commands related to the service:
```bash
  sudo systemctl status <service_name - foreignlit>
  sudo systemctl restart <service_name - foreignlit>
  sudo systemctl stop <service_name - foreignlit>
```

##Nginx.conf
edit default or create webapp dedicated in:
```bash
vim /etc/nginx/sites-enabled/default
```


![Logo](./app/static/logo-fl.png)


## Acknowledgements

 - [Setting up a Python development environment with pipenv]([https://phrase.com/blog/posts/i18n-advantages-babel-python](https://dev.to/davidshare/setting-up-a-python-development-environment-with-pipenv-3lfj))
