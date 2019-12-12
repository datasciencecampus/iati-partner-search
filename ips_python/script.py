try:
    from ips_python.preprocessing import preprocess_query_text
    from ips_python.vectorize import (
        create_tfidf_term_document_matrix,
        vectorize_input_text,
    )
    from ips_python.cosine import get_cosine_similarity
    from ips_python.refinement import process_results, gather_top_results
    from ips_python.word2vecaverage import average_per_doc
except ModuleNotFoundError:
    from preprocessing import preprocess_query_text
    from vectorize import create_tfidf_term_document_matrix, vectorize_input_text
    from cosine import get_cosine_similarity
    from refinement import process_results, gather_top_results
    from word2vecaverage import average_per_doc


def download_data():
    """
    this is a placeholder function to show that we need to run something in order to procure the data
    """
    pass


def main():
    download_data()
    create_tfidf_term_document_matrix()


def process_query(
    query_text,
    vectorizer,
    term_document_matrix,
    processed_iati_records,
    full_iati_records,
):
    processed_query_dataframe = preprocess_query_text(query_text)
    vectorized_query = vectorize_input_text(processed_query_dataframe, vectorizer)
    df_result = get_cosine_similarity(
        vectorized_query, term_document_matrix, processed_iati_records
    )
    smart_results = process_results(df_result, full_iati_records)
    top_results = gather_top_results(smart_results, "reporting.org", 3)
    return top_results


def process_query_embeddings(
    query_text, w2v_model, w2v_avg, processed_iati_records, full_iati_records
):
    processed_query_dataframe = preprocess_query_text(query_text)

    query_average = average_per_doc(
        str(processed_query_dataframe["description"]), w2v_model, 300
    ).reshape(1, -1)

    df_result = get_cosine_similarity(query_average, w2v_avg, processed_iati_records)
    smart_results = process_results(df_result, full_iati_records)
    top_results = gather_top_results(smart_results, "reporting.org", 3)
    return top_results


if __name__ == "__main__":
    main()
