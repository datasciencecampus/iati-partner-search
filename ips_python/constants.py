INPUT_DATA_FILENAME = "all_downloaded_records.csv"
PROCESSED_RECORDS_FILENAME = "processed_records.csv"
WORD_LIST_FILENAME = "word_list.pkl"
TERM_DOCUMENT_MATRIX_FILENAME = "term_document_matrix.pkl"
VECTORIZER_FILENAME = "vectorizer.pkl"
COSINE_FILENAME = "cosine_df.csv"
STOPWORDS_FILENAME = "stopwords.txt"
KEEPWORDS_FILENAME = "words_to_keep.txt"

CLUSTERING_SUM_OF_SQUARE_COMPARISON_FILENAME = "ssResults.csv"
CLUSTER_CENTROIDS_FILENAME_CONVENTION = "clusterCentroidsDict_{0}_clusters.pkl"
"clusterElbowResSVD.pkl"
ACTIVITY_CLUSTER_ASSIGNMENT_FILENAME_CONVENTION = (
    "activity_cluster_assignment_{0}_clusters.csv"
)
WORD2VECMODEL_FILENAME = "word2vec.model"
WORD2VECAVG_FILENAME = "word2vecdocavg.pkl"

DESCRIPTION_COLUMN_NAME = "description_narrative_text"
TITLE_COLUMN_NAME = "title_narrative_text"
IATI_IDENTIFIER_COLUMN_NAME = "iati_identifier"
ORG_ID_COLUMN_NAME = "reporting_org_ref"

IATI_FIELDS = [
    "id",
    IATI_IDENTIFIER_COLUMN_NAME,
    ORG_ID_COLUMN_NAME,
    "reporting_org_type_code",
    "reporting_org_type_name",
    "reporting_org_secondary_reporter",
    "reporting_org_narrative",
    "title_narrative",
    "title_narrative_lang",
    "title_narrative_text",
    "description_type",
    "description_narrative",
    "description_narrative_text",
    "participating_org_ref",
    "participating_org_type",
    "participating_org_role",
    "participating_org_narrative",
    "participating_org_narrative_lang",
    "participating_org_narrative_text",
    "description_lang",
]
ELASTICSEARCH_INDEX_NAME = "iati"
ELASTICSEARCH_LOGGING_INDEX_NAME = "logs"
