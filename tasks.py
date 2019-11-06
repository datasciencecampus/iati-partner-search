from invoke import task
import os


@task
def install_dependencies(c):
    c.run("pip install -r requirements.txt")


@task
def check_format(c):
    c.run("black --check python/*.py")


@task
def lint(c):
    c.run("flake8 .")


@task
def build_dev_docker(c):
    c.run("docker build -t iati_partner_search .")


@task
def build_docker(c):
    tag = os.environ["TRAVIS_BUILD_NUMBER"] if "TRAVIS_BUILD_NUMBER" in os.environ else "latest"
    c.run(f"docker build -t rabshab/iati-partner-search-app:{tag} -f app.Dockerfile .")


@task
def run_docker(c):
    c.run("docker run --name=ipsapp -p 5000:5000 rabshab/iati-partner-search-app")


@task
def push_docker(c):
    travis_build_number = os.environ["TRAVIS_BUILD_NUMBER"]
    c.run(f"docker push rabshab/iati-partner-search-app:{travis_build_number}")


@task
def ci(c):
    print("Running CI scripts")
    check_format(c)
    lint(c)
    if "TRAVIS_PULL_REQUEST" in os.environ:
        build_docker(c)
        push_docker(c)
