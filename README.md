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
## Docker
1. Create Dockerfile, or pull one from Dockerhub:
```bash
docker pull discipy/book-catalog:v0.0.1
```
if image was 'pulled' from Dockerhub, skip step 2
2. Build image:
```bash
docker build --tag discipy/book-catalog:v0.0.1 .
```
3. Run container: use --net to connect container to AWS instance network, --enf-file to declare env vars
```bash
docker run --net="host" --env-file .env --name web_bcatalog discipy/book-catalog:v0.0.1
```
Use following commands to manage container:
```bash
docker stop web_bcatalog

docker start web_bcatalog
```

The following command removes container (**which should be stopped beforehand**)
```bash
docker rm web_bcatalog
```



![Logo](./app/static/logo-fl.png)


## Acknowledgements

 - [docker docs](https://docs.docker.com/)

