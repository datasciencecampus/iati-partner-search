from invoke import task

@task
def install_dependencies(c):
    c.run("pip install -r requirements.txt")

@task
def check_python_formatting(c):
    c.run("black --check python/*.py")

@task
def build_docker(c):
    c.run("docker build -t rabshab/iati-partner-search-app -f .\app.Dockerfile .")

@task
def run_docker(c):
    c.run("docker run --name=ipsapp -p 5000:5000 rabshab/iati-partner-search-app")

@task
def push_docker(c):
    c.run("docker push rabshab/iati-partner-search-app:latest")

@task(install_dependencies, check_python_formatting, build_docker, push_docker)
def ci(c):
    print("Running CI scripts")