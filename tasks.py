import os
from os.path import isfile, join
import shutil

from invoke import task
from ips_python.utils import get_data_path
from ips_python.constants import INPUT_DATA_FILENAME


@task
def install_dependencies(c):
    c.run("pip install -r requirements.txt")


@task
def install_dev_dependencies(c):
    c.run("pip install -r requirements-dev.txt")


@task
def install_all(c):
    install_dependencies(c)
    install_dev_dependencies(c)


@task
def check_format(c):
    c.run("black --check .")


@task
def format(c):
    c.run("black .")


@task
def lint(c):
    c.run("flake8 .")


@task
def build_dev_docker(c):
    c.run("docker build -t iati_partner_search -f ./app.Dockerfile .")


@task
def build_docker(c):
    tag = (
        os.environ["TRAVIS_BUILD_NUMBER"]
        if "TRAVIS_BUILD_NUMBER" in os.environ
        else "latest"
    )
    c.run(
        f"docker build -t datasciencecampus/iati-partner-search-app:{tag} -f app.Dockerfile ."
    )


@task
def run_docker(c):
    c.run(
        "docker run --name=ipsapp -p 5000:5000 datasciencecampus/iati-partner-search-app"
    )


@task
def push_docker(c):
    travis_build_number = os.environ["TRAVIS_BUILD_NUMBER"]
    c.run(
        f"docker push datasciencecampus/iati-partner-search-app:{travis_build_number}"
    )


@task
def build_and_deploy_flask_docker(c):
    build_docker(c)
    push_docker(c)


@task
def test(c):
    # update pyproject.toml for py.test defaults
    c.run("py.test --cov=./")


@task
def clear_data(c):
    protected_files = [".gitkeep", INPUT_DATA_FILENAME]
    data_path = get_data_path()
    files_to_be_deleted = [
        (f, join(data_path, f))
        for f in os.listdir(data_path)
        if isfile(join(data_path, f)) and f not in protected_files
    ]

    for file_name, file_path in files_to_be_deleted:
        print(f"DELETING {file_name}")
        os.remove(file_path)


@task
def download_nltk_data(c):
    import nltk

    nltk.download("stopwords")
    nltk.download("words")


def get_docs_source_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def get_docs_build_path():
    return os.path.join(get_docs_source_path(), "_build")


@task
def makedocs(
    c, doctype="html", docs_build_path=get_docs_build_path(),
):
    from sphinx.cmd.build import build_main
    from m2r import convert

    with open("./README.md", "r") as _file:
        markdown_contents = _file.read()

    with open(os.path.join(get_docs_source_path(), "readme.rst"), "w+") as _file:
        _file.write(convert(markdown_contents))

    build_main(["-b", doctype, get_docs_source_path(), docs_build_path])


@task
def cleandocs(c):
    shutil.rmtree(get_docs_build_path())


@task
def download_data(c):
    from ips_python.download import main

    main()
