# IATI Partner Search
 Description of the project goes here

## Installation
To install the python packages, make sure that you have your virtual environment activated and run the following:

```powershell
pip install -r requirements.txt
```

## Using Docker
This repo provides a Dockerfile, that you can build on your machine, which should provide an environment in which the code can execute.

### Python Pipeline Development
We do not currently publish our images to a registry. You must build them on your machine. Make sure that the Docker VM is running, then run:
```powershell
docker build -t iati_partner_search .
```
The `-t iati_partner_search` means that we're telling Docker that we want the image to be called `iati_partner_search`.

Once the image has been built, we can run a container:
```powershell
docker run --name=ips -it -v ${pwd}:/iati-partner-search -p 5000:5000 iati_partner_search bash
```
to break this down:

- `--name=ips`: tells what we will call this container when we want to start and stop it again.
- `-it`: 
- `-v ${pwd}:/iati-partner-search`: tells Docker to share the files on your machine, with the Docker container.
- `-p 5000:5000`: tells Docker that we want to map port 5000 on our machine to port 5000 of the container
- `iati_partner_search`: refers to the image that we want to build the container from.
- `bash`: is the process that want the container to run. In this case we're asking it to start the CLI

You can then stop and start the container by running `docker stop ips` and `docker start ips` respectively.

You can read more about Docker containers and this process [here](https://docs.docker.com/).

## Get the Data
Currently (and temporarily) we copy in the data manually. Copy the file named `all_downloaded_records.csv` in to the `/data/` directory.

If you're not working from within the Docker container, you will also need to download the nltk data. Open your python shell and execute the following:

```python
>>> import nltk
>>> nltk.download('words')
>>> nltk.download('stopwords')
```

## Run the Flask application
After adding the required data and installing the required packages you will be able to run the Flask app locally.

In the `/data` directory make sure you have

    - all_downloaded_records.csv
    - processed_records.csv
    - term_document_matrix.pkl
    - vectorizer.pkl

The easiest way is to run the application inside the docker container. Build and run the container using the instructions in the [Python Pipeline Development](#python-pipeline-development) section.

Then, from within the running container, run 

```bash
python -m flask run --host=0.0.0.0
```

After a few seconds of start up time it should be up and running. Navigate to `localhost:5000` in your web browser to view the page.

There is also the docker container which is used for running the application in production which is described by `app.Dockerfile`. To use this one instead it is necessary to remove `data/` from the `.dockerignore` first. 

Then run 

```bash 
docker build -t iati-partner-search-app -f .\app.Dockerfile .
```

to build the image and

```bash
docker run --name=ipsapp -p 5000:5000 iati-partner-search-app
```
to run it.

After a few seconds of start up time it should be up and running. Navigate to `localhost:5000` in your web browser to view the page.