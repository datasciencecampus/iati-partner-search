from invoke import task

@task
def build_docker(c):
    c.run("docker build -t iati-partner-search .")

@task
def run_docker(c):
    c.run("docker run --name=ips -it -v ${pwd}:/iati-partner-search -p 5000:5000 iati-partner-search bash")

@task
def start(c):
    c.run("python -m flask run --host=0.0.0.0")