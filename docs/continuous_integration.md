# Continuous Integration

## Elasticsearch

The fields that are indexed into the elasticsearch cluster can be found in `constants.py`

All the documents are re-indexed every cycle. As we are using the `id` given by the IATI API as the id in elasticsearch it will ignore any that it has seen before so documents that are already indexed won't be added again. They will be added to the `docs.deleted` on the index (viewable at `_cat/indices?v`) but this appears to be cleaned up by elasticsearch[1][2] so we don't have to do any work ourselves. 

[1] https://discuss.elastic.co/t/purge-the-deleted-documents-on-disk/19768
[2] https://github.com/elastic/elasticsearch/issues/30237