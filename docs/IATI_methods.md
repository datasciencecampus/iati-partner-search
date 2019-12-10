# IATI Approaches Overview

## Word Embeddings - Tom

### Approach
- For every word in your corpus (i.e. all the IATI descriptions) the word2vec model
    - 1. Using the words occuring more than 20 times it maps those words into a 50 dimensional space.
- Similarity: determined by context in the corpus (cat, dog), which helps to pick out synonyms.

### Current Status
  - adding context just from the IATI data.
  - * could add context from another corpus or use a pre-built model.
  - vector size (how many dimensions) is 50, but could be higher e.g. 300, but ideally you would want to decide based on the asymptote as to when more dimensions does not add anything.
  - but this is difficult to assess because hasn't been supervised

**How to use it:**
  1. Advanced key word search.
  2. Averaging the vector to document and using cosine similarity.
  3. doc2vec (may not have enough words in document to use this)

### Packages
- gensim.models word2vec

### Added value
- Includes synonyms, so may strengthen connections.

### Current challenges
- Entries with very few words.

## Information Searching - Saliha

[See Saliha's code base for overview](https://github.com/salihadfid1/NLP_INTRO)

## Elastic Search
* [Can do custom analysis at both index time and query time](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html)
* [Here are the ones that are supplied](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)
* [Or build out your own](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html)

### Approach

* Elastic search uses Apache Lucene.

   * according to **Lucene scoring formula**, a document would be most similar to itself due to the terms with the highest tf-idf.

* One of the query functions is more_like_this:

   * MLT: query extracts text from the input document, analyzes it, usually using the same analyzer at the field, then selects the top K terms with highest tf-idf to form a disjunctive query of these terms.

  * The fields on which to perform MLT must be indexed and of type text of keyword.


### How It works
- Acquire Raw Content
- Build the document
- Analyze the document
  - Specify which part of the text is to be indexed.
- Index the document
  - the documents need to be indexed so that the document can be retrieved based on certain keys instead of the entire content of the document.
  - the index process is similar to indexes at the end of a book (where common words are shown with their page numbers so that these words can be tracked quickly).
    - each index is comprised of multiple **shards**, which are the storage containers for your data.
    - Once your Index is created your cannot change the number of Primary shards.

### Deciding the right number of shards to use

- How much information you are going to store inside your index
- How fast/parallel you want ES to be able to write the data
- How much time you will want to wait when ES relocates your shard

### Index Mapping (Index Schema)

- There are the so-called 'field datatypes', which define the type of data your field contains. By 'field' we are meaning the value of a key inside indexed JSON Document.
- If you have JSON document like this:
```
{
    "Name": Travis,
    "Age" : 23
}
```

Each of the fields "Name" and "Age" will have their datatype (part of the Index Mapping).

If you let ElasticSearch choose the mapping for you, always double-check and make sure that the right mappings have been chosen for your scenario. You could easily check an Index mappings, by issuing ES query:

```
GET /my_test_index/_mapping?pretty
```



Currently the field data types you are able to choose from, contain:

* **basic:** text, keyword, date, long, double, boolean, ip

* **hierarchy support:** object, nested

* **special types:** geo_point, geo_shape, completion

- User Interface for Search
- Build Query
  - prepare a Query object using text which can be used to inquire index database to get the relevant details.
- Search Query
  - Using a query object, the index database is checked to get the relevant details and the content documents.
  - Common query types
      - TermQuery, TermRangeQuery, BooleanQuery, PhraseQuery, WildCardQuery, FuzzyQuery (searches documets using fuzzy implementation that is an approximate search based on the edit distance algorithm.)
      - edit distance is a way of quantifying how dissimilar two strings (e.g., words) are to one another by counting the minimum number of operations required to transform one string into the other. Edit distances find applications in natural language processing, where automatic spelling correction can determine candidate corrections for a misspelled word by selecting words from a dictionary that have a low distance to the word in question.

**Difference between keyword and text data types for storing your data.
* Keywords are stored as they are inside the Lucene Index
* Keyword can be sued for filtering and aggregations.  - that is imporotant if you try to do things liek 'GROUP By' or 'WHERE id = '5'"
* Keywords can be searched with Term-Level Queries like: **range, exists, regexp, wildcard**.


Other option:
- Can store Geo coordinates inside ElasticSearch.
