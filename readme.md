# IATI Partner Search
 Description of the project goes here

 ## Installation
 To install the python packages, make sure that you have your virtual environment activated and run the following:

 ```{bash}
 pip install -r requirements.txt
 ```

## Get the Data
Currently (and temporarily) we copy in the data manually. Copy the file named `all_downloaded_records.csv` in to the `/data/` directory.

You will also need to download the nltk data. We're working on making this more contained, but in the mean time, open your python shell and execute the following:

```{python}
>>> import nltk
>>> nltk.download('words')
>>> nltk.download('stopwords')
```