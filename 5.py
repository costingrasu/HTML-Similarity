import os
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from collections import Counter

# Function to parse HTML and extract content, tags, classes, and styles
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        # Extracting the text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Extracting the tags and their hierarchy
        tags = [tag.name for tag in soup.find_all()]
        
        # Extracting the classes and inline styles
        classes = [cls for tag in soup.find_all() for cls in tag.get('class', [])]
        styles = [tag.get('style', '') for tag in soup.find_all() if tag.get('style')]
        
        return text, tags, classes, styles

# Function to generate an occurrences vector of text, tags, classes and styles for a document
def featureVector(text, tags, classes, styles):
    # Count tags, classes, and style
    tag_counts = Counter(tags)
    class_counts = Counter(classes)
    style_counts = Counter(styles)
    
    # Convert counts into a list of occurrences
    tag_feature = ' '.join([f"{tag}:{count}" for tag, count in tag_counts.items()])
    class_feature = ' '.join([f"{cls}:{count}" for cls, count in class_counts.items()])
    style_feature = ' '.join([f"style:{count}" for count, count in style_counts.items() if count > 0])

    # Combining into string
    feature_vector = f"{text} {tag_feature} {class_feature} {style_feature}"
    return feature_vector

# Function to generate the TF-IDF matrix of the documents (each row is a document, each column a word, the value is the TF-IDF score)
def TF_IDF(documents):
    features = []
    for doc in documents:
        text, tags, classes, styles = doc
        feature_vector = featureVector(text, tags, classes, styles)
        features.append(feature_vector)
    
    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(features)
    return tfidf_matrix

# Function to perform K-means clustering
def kmeans_clustering(tfidf_matrix, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

# Function to group HTML files based on clustering results
def group_html(directory, n_clusters=5):
    # Parsing the HTML files and extract text content, tags, classes, and styles
    documents = []
    file_paths = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.html'):
            file_path = os.path.join(directory, file_name)
            text, tags, classes, styles = parse_html(file_path)
            documents.append((text, tags, classes, styles))
            file_paths.append(file_path)
    
    # Generating the TF-IDF matrix
    tfidf_matrix = TF_IDF(documents)
    
    # K-means
    cluster_labels = kmeans_clustering(tfidf_matrix, n_clusters)
    
    # Group files by cluster labels
    grouped_documents = {}
    for idx, cluster_id in enumerate(cluster_labels):
        if cluster_id not in grouped_documents:
            grouped_documents[cluster_id] = []
        grouped_documents[cluster_id].append(file_paths[idx])
    
    # Output
    for cluster_id, group in grouped_documents.items():
        print(f"Cluster {cluster_id}:")
        for file in group:
            print(f"  - {file}")
        print()

# Path to the folder where each tier directory is
folder = './'

print("TIER 1")

tier1= os.path.join(folder, 'tier1')
group_html(tier1, n_clusters=5) #Number of groups (clusters)

print("TIER 2")

tier2= os.path.join(folder, 'tier2')
group_html(tier2, n_clusters=5)

print("TIER 3")

tier3= os.path.join(folder, 'tier3')
group_html(tier3, n_clusters=5)

print("TIER 4")

tier4= os.path.join(folder, 'tier4')
group_html(tier4, n_clusters=5)