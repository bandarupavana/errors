#.github\workflows\ci-dockerhub.yml

name: ci-dockerhub

on:
  push:
    branches: [ "main" ]
    tags: [ "*" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-test-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: PYTHONPATH=. pytest -q

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ secrets.DOCKERHUB_USERNAME }}/python-ci-lab
          tags: |
            type=raw,value=latest,enable={{is_default_branch}}
            type=sha,prefix=sha-,format=short
            type=ref,event=tag

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64

----------------------

#tests\test_app.py

from app import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
--------------------------------------------
#gitgnore

_pycache__/
.venv/
.pytest_cache/
.DS_Store
*.pyc

------------------------------
app.py
def add(a, b):
    return a + b

if __name__ == "__main__":
    print("Hello from Python CI Lab!")
    print("2 + 3 =", add(2, 3))
--------------------------------
Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]

-----------------------------------

requirements.txt

pytest==8.3.2
pytest
--------------------------------

#commands
python app.py
pytest -q or python -m pytest -q
docker build -t yourname/python-ci-lab:local .
docker run --rm yourname/python-ci-lab:local

create new github repos 

git init
git add .
git commit -m "Initial commit for Python CI/CD pipeline"
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main

Go to same GitHub repository → click Settings → Secrets and variables → Actions → New
repository secret → create two secrets:

DOCKERHUB_USERNAME → your Docker Hub username

DOCKERHUB_TOKEN → your Docker Hub access token (acc settings -> Personal access tokens -> Create access token
access token description = randomname
expiration = none
access permissions = read,write,delete 
)
copy 2.

git add .
git commit -m "Trigger CI/CD workflow"
git push










