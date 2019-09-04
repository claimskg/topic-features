# topic-features

This project contains different python scripts and notebooks for the tasks of fake news detection.

## Data
The data used comes from the ClaimsKG dataset, for space reasons the data is not stored here, a full dump can be downloaded from https://zenodo.org/record/2628745#.XW9x3i4za70

## Scripts
- rdftocsv: Loads the knowledge graph and transforms it into a csv file
- clustering: Using the output from "rdftocsv" determines the n-occurring keywords and clusters the keywords based on their co-occurrence matrix using the ward clustering algorithm

## Notebooks
- Clustering: Notebook version of the "clustering" script
- Cluster Statistics: Using the output from "clustering" determines which claims belong to each cluster, outputs how many claims belong to each cluster and creates separated csv files containing the claims for each cluster
- Baseline: Does standard preprocessing steps to the clusters and uses a Linear SVM for classification.
- ICF ITF: Contains the methods necessary to compute the "Inverse Category Frequency" and the "Inverse Document Frequency", it also classifies the data using these weighting schemes
- Authors: For each author found in one of the cluster files it extracts additional information from both politifact and wikipedia in order to classify them in different groups. The groups chosen are: "Democrat, Republican, Political, Journalist, Person, Organization"
- Authors as a feature: Adds the data determined in "Authors" to the baseline and classifies using these new features.
- Credibility Vectors: Computes the credibility vector for each of the author groups determines in "Authors" and classifies using these new features. 
