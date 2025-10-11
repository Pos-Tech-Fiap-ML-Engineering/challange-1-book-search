# challange-1-book-search


# Comandos úteis

* ```bash 
    poetry run poe {TASK_NAME}
  ```
* ```bash
    poetry export -f requirements.txt --without-hashes -o requirements.txt
  ```
* ```bash
    docker build -t book-search:latest -f Dockerfile ../../
  ```
* ```bash
  docker run --rm -it -p 8000:8000 -e GUNICORN_WORKERS=6 --name book-search book-search:latest
  ```
* ```bash
  docker run --rm -it --entrypoint /bin/sh book-search:latest
  ```