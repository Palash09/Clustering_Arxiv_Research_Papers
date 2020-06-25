import pickle

import numpy as np
from sklearn.decomposition import NMF

from preprocess import preprocess_text


def get_topics(model, feature_names, no_top_words):

    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict[topic_idx] = " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])

    return topic_dict


def possibleTopics(data_dir, tfidf_model, vectSum, no_components=10, num_top_words=10):
    """
        This function helps in generating topics of the papers through topic modelling
        and Non-Negative Matrix Factorization.

        For generating the results, function takes vectorized summary data which was
        obtained through TF-IDF model.


        Parameters
        -----------------
        query : list
            User's query to the recommendation engine.
        tfidf_model : sklearn.feature_extraction.text.TfidfVectorizer
            The model which is used to extract the tfidf vectors from a
            given processed corpus.
        vectSum: scipy.sparse.csr.csr_matrix
            The matrix with tfidf vectors of all the papers.

        Returns
        -------
        nmf_model : sklearn.decomposition.NMF
            An NMF model fitted to the given TF-IDF vectors.
    """

    tf_feature_names = tfidf_model.get_feature_names()

    nmf_model = NMF(n_components=no_components, random_state=1,
                    alpha=.1, l1_ratio=.5, init='nndsvd').fit(vectSum)

    with open(data_dir + "nmf_model.pk", 'wb') as fp:
        pickle.dump(nmf_model, fp)
    print("NMF model saved!")

    topic_dict = get_topics(
        nmf_model, tf_feature_names, num_top_words)

    with open(data_dir + "topic_dict.pk", 'wb') as fp:
        pickle.dump(topic_dict, fp)
    print("Saved topic dictionary!")

    return nmf_model


def get_topic_class(vect):
    """
        Calculates the most probable topic for a given vector.

        Parameters
        ----------
        vect : numpy.array
            A TF-IDF vector.

        Returns
        -------
        prob_topic : int
            The most probably topic the TF-IDF vector belongs to.
    """

    topic_probability_scores = nmf_model.transform(vect)

    prob_topic = np.argmax(np.sum(topic_probability_scores, axis=0))

    return prob_topic


def labelTopics(data_dir, nmf_model, vectSum):
    """
        Takes all the summary vectors and assigns a topic labels to it.
        Saves the labels to data_dir with name "topic_labels.pk".

        Parameters
        ----------
        data_dir : string
            Path to directory to store data.
        nmf_model : sklearn.decomposition.NMF
            NMF model used to get topics from a TF-IDF vector.
        vectSum : np.ndarray
            TF-IDF vectors for the summary of all the research papers.
    """
    topic_labels = np.array(list(map(get_topic_class, vectSum)))

    with open(data_dir + "topic_labels.pk", 'wb') as fp:
        pickle.dump(topic_labels, fp)
    print("Saved topic labels!")


if __name__ == "__main__":
    data_dir = "data/"

    with open(data_dir + 'vectorizer.pk', 'rb') as pickle_in:
        vectorizer = pickle.load(pickle_in)

    with open(data_dir + "tfidf-vectors-100.pk", "rb") as fp:
        vectSum = pickle.load(fp)

    try:
        with open(data_dir + "nmf_model.pk", 'rb') as fp:
            nmf_model = pickle.load(fp)
    except FileNotFoundError:
        nmf_model = possibleTopics(data_dir, vectorizer, vectSum)

    labelTopics(data_dir, nmf_model, vectSum)
