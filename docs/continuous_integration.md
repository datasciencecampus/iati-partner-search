# Continuous Integration

## Elasticsearch

The fields that are indexed into the elasticsearch cluster can be found in `constants.py`

All the documents are re-indexed every cycle. As we are using the `id` given by the IATI API (note, this is *not* the same as the activity Identifier) as the id in elasticsearch it will ignore any that it has seen before so documents that are already indexed won't be added again. They will be added to the `docs.deleted` on the index (viewable at `_cat/indices?v`) but this appears to be cleaned up by elasticsearch ([1](https://discuss.elastic.co/t/purge-the-deleted-documents-on-disk/19768), [2](https://github.com/elastic/elasticsearch/issues/30237)) so we don't have to do any work ourselves.

### Data Wrangling

We use the IATI.Cloud data, which is stored as a CSV.
We are then faced with the challenge of reading this data to a pandas dataframe, converting it to a python dict, which is then passed to the `elasticsearch` python library and uploaded to Elasticsearch, using JSON.
The IATI data contains missing values, which need to be dealt with.
The first thing we do is let the Elasticseach instance know that it should accept missing values. This can either be done with the following cURL request:

```bash
curl --location --request PUT '<ELASTICSEARCH_URL>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "settings": {
        "index.mapping.ignore_malformed": true
    }
    }'
```

or you can use the python library, which we've wrapped with the `ensure_elasticsearch_keeps_malformed_fields` function in the `upload_to_elasticsearch.py` file.

The next issue we ran in to was that Elasticsearch was not automatically handling the missing values that we passed it, because we were using pandas to handle the data.
In this case, missing values that were interpreted as `NaN` numpy objects or `None` in the Python code, were not handled when we uploaded them to Elasticsearch.

This issue can be replicated with the following code:

```python
from elasticsearch import helpers
from elasticsearch import Elasticsearch

import pandas as pd
import numpy as np

from ips_python.upload_to_elasticsearch import document_generator

ELASTICSEARCH_URL="<CHANGEME>"
ELASTICSEARCH_INDEX_NAME="<CHANGEME>"

def create_dataframe_iteratable(dataframe_iterator):
    dataframe.iterrows()
    for index, document in dataframe_iterator:
        yield {"_index": elasticsearch_index_name, "_type": "_doc", "_id": f"{document['id']}", **document}

elasticsearch_instance = Elasticsearch(
    [
        ELASTICSEARCH_URL
    ]
)
dataframe = pd.DataFrame([["b", None, np.NaN]], columns=["id", "foo", "baz"])


helpers.bulk(elasticsearch_instance, create_dataframe_iteratable(dataframe))
```
This will throw an error when the python client attempts to upload the data.
Instead we must transform these missing data to empty strings.
This can be done with the `fillna` pandas method:

```python
...
dataframe = pd.DataFrame([["b", None, np.NaN]], columns=["id", "foo", "baz"]).fillna('')
...
```
The upload should now work.
See the `ips_python/upload_to_elasticsearch.py` file for more details on how this is solved.

### Updating Elasticsearch using Github Actions
We use Github Actions to update the data on the Elasticsearch server.
See the `.github/workflows/updateelasticsearch.yml` file for details on how to do this.
[This doc](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/persisting-workflow-data-using-artifacts) on workflow artifacts is helpful in understanding what is going on.
You can see the Actions and worklows for this project [here](https://github.com/datasciencecampus/iati-partner-search/actions).

This Action is triggered by a timer, the frequency may change, so check the `on` field.
It would look something like this in the `updateelasticsearch.yml` file:

```yml
on:
  schedule:
    - cron:  '0 1 * * *'
```

To understand how the timing is set, see the [Github scheduling events documentation](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows#scheduled-events-schedule).

Note that we store the production Elasticsearch URL using [Github Secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets) within the Github Action.
In the event that the URL changes, a repository administrator will need to delete an re-create the secret called `ELASTICSEARCH_URL`.
