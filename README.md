# Clustering_Arxiv_Research_Papers
In this project I have used information retrieval concept to extract relevant information from research papers available on Arxiv. 
Furthermore, these research papers were clustered with the help of abstract of each paper

For this project I had fetched the dataset from Kaggle where information about computer science related research papers was available in json format. The aim of the
project was to cluster the research papers by extracting apt keywords from the abstracts of each research paper. At last we would also be able to find research papers
related to the keyword search.

Initially frequent words from abstract of research papers were found, after this preprocessing of abstract was performed for applying TF-IDF algorithm. For performing 
keyword search, topic modelling was used to fetch relevant labels for abstracts of different research paper. All the relevant models were saved using pickle library for
usage at different instances. For better visualization, top 10 research paper authors and count of research papers for each year is presented.

<center>![Keyword_Search](https://github.com/Palash09/Clustering_Arxiv_Research_Papers/blob/master/Keyword_Search_Result.png)</center>
![Vis_1](https://github.com/Palash09/Clustering_Arxiv_Research_Papers/blob/master/Vis_1.png)

