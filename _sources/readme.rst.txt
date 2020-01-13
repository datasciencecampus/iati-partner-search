
IATI Partner Search
===================


.. image:: https://travis-ci.com/datasciencecampus/iati-partner-search.svg?branch=master
   :target: https://travis-ci.com/datasciencecampus/iati-partner-search/
   :alt: Build Passing/Failing on TravisCI.com



.. image:: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fdatasciencecampus%2Fiati-partner-search%2Fbadge%3Fref%3Dmaster&style=flat
   :target: https://actions-badge.atrox.dev/datasciencecampus/iati-partner-search/goto?ref=master
   :alt: Build Status



.. image:: https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg
   :target: https://hub.docker.com/r/datasciencecampus/iati-partner-search-app/tags
   :alt: Docker Automated build



.. image:: https://codecov.io/gh/datasciencecampus/iati-partner-search/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/datasciencecampus/iati-partner-search
   :alt: Code Coverage


`![https://readthedocs.org/projects/iati-partner-search/badge/?version=latest] <https://datasciencecampus.github.io/iati-partner-search/>`_


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black


A tool using NLP technology to match aid funders with potential implementers.

A more detailed break-down of the project can be found `here <http://datasciencecampus.github.io/iati-partner-search>`_.

Installation
------------

To install the python packages, make sure that you have your virtual environment activated and run the following:

.. code-block:: shell

   pip install invoke
   invoke install-all

This will install all of the development and testing packages as well

Pre-Commit
^^^^^^^^^^

`Pre-commit <https://pre-commit.com>`_ is a helpful tool that will catch file errors when you try to commit work.
This is helpful so that small bugs and typos aren't pushed to Github, and we don't have to wait for out automated tests to find them.

This is optional, but to initialize pre-commit, run the following:

.. code-block:: shell

   pre-commit install

Testing
-------

To run tests:

.. code-block:: shell

   invoke test

To run linting, formatting and tests:

.. code-block:: shell

   invoke ci

Using Docker
------------

This repo provides a Dockerfile (\ ``app.Dockerfile``\ ), that you can build on your machine, which should provide an environment in which the code can execute.

Python Pipeline Development
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We do not currently publish our images to `DockerHub <https://hub.docker.com/r/datasciencecampus/iati-partner-search-app>`_. You must build them on your machine. Make sure that the Docker VM is running, then run:

.. code-block:: shell

   docker build -t iati_partner_search -f ./app.Dockerfile .

Or if you have ``invoke`` installed, run ``invoke build-dev-docker`` which will run this command on your behalf.

The ``-t iati_partner_search`` means that we're telling Docker that we want the image to be called ``iati_partner_search``.
The ``-f ./app.Dockerfile`` tells Docker which Dockerfile to use.

Once the image has been built, we can run a container:

.. code-block:: shell

   docker run --name=ips -it -v ${pwd}:/iati-partner-search -p 5000:5000 iati_partner_search bash

to break this down:


* ``--name=ips``\ : tells what we will call this container when we want to start and stop it again.
* ``-it``\ :
* ``-v ${pwd}:/iati-partner-search``\ : tells Docker to share the files on your machine, with the Docker container.
* ``-p 5000:5000``\ : tells Docker that we want to map port 5000 on our machine to port 5000 of the container
* ``iati_partner_search``\ : refers to the image that we want to build the container from.
* ``bash``\ : is the process that want the container to run. In this case we're asking it to start the CLI. If instead we want to start the web application, do not include this, and it will be started automatically.

You can then stop and start the container by running ``docker stop ips`` and ``docker start ips`` respectively.

You can read more about Docker containers and this process `here <https://docs.docker.com/>`_.

Get the Data
------------

To download the raw data, run:

.. code-block:: shell

   invoke download-data

Note the data is currently just over 1GB in size and so could take some time to download.

If you're not working from within the Docker container, you will also need to download the nltk data. Execute the following:

.. code-block:: shell

   invoke download-nltk-data

Run the Flask application
-------------------------

After adding the required data and installing the required packages you will be able to run the web application on your own computer.

In the ``/data`` directory make sure you have

.. code-block::

   - all_downloaded_records.csv
   - processed_records.csv
   - term_document_matrix.pkl
   - vectorizer.pkl


Then, using invoke, run

.. code-block:: bash

   invoke build-docker

to build the docker and then

.. code-block:: bash

   invoke run-docker

to run it.

After a few seconds of start up time it should be up and running. Navigate to ``localhost:5000`` in your web browser to view the page.
