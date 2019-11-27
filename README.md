# IATI Partner Search
 Description of the project goes here

## Installation
To install the python packages, make sure that you have your virtual environment activated and run the following:

```powershell
pip install invoke
invoke install-all
```
This will install all of the development and testing packages as well

## Testing
To run tests:

```powershell
invoke test
```

To run linting, formatting and tests:

```powershell
invoke ci
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

If you're not working from within the Docker container, you will also need to download the nltk data.Execute the following:

```powershell
invoke download-nltk-data
```

## Run the Flask application
After adding the required data and installing the required packages you will be able to run the Flask app locally.

In the `/data` directory make sure you have

    - all_downloaded_records.csv
    - processed_records.csv
    - term_document_matrix.pkl
    - vectorizer.pkl

Then, using invoke, run

```bash
invoke build-docker
```
to build the docker and then

```bash
invoke run-docker
```
to run it.

After a few seconds of start up time it should be up and running. Navigate to `localhost:5000` in your web browser to view the page.
