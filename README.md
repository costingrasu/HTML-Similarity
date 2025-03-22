# HTML-Similarity

## **Overview**

This project implements an algorithm to group similar HTML documents based on their content, DOM structure, and styling. The goal is to cluster HTML documents that share structural and visual similarities, without requiring full visual rendering (which would require image processing). The solution combines traditional text similarity techniques (using **TF-IDF**) with a focus on DOM structure and styling to achieve meaningful clustering of HTML files.

## **Solution Approach**

The solution follows a **multi-feature** approach where we analyze:
- **Textual content** (extracted via `get_text()`).
- **DOM structure** (tags and their nesting).
- **Styling and Layout** (classes, IDs, and inline styles).

The approach involves these steps:

1. **Parse HTML documents**:
    - For each HTML file, we extract the raw text content, the tags used, the CSS classes, and any inline styles.
  
2. **Feature Extraction**:
    - We **count occurrences** of HTML tags, CSS classes, and inline styles.
    - We also keep track of the **text content** in the document.
    - All these features are combined into a single **feature vector** for each document.
  
3. **TF-IDF Transformation**:
    - The textual content is vectorized using **TF-IDF (Term Frequency-Inverse Document Frequency)**, which transforms the text into a vector representation. This highlights important words in each document and reduces the influence of common terms like "the", "and", etc.
  
4. **K-means Clustering**:
    - After extracting features from each document, the **K-means clustering algorithm** is used to group documents into clusters based on the similarity of their feature vectors. K-means groups documents with similar content, structure, and styling.

5. **Output**:
    - The program outputs the grouped documents into an `output.txt` file, with each group representing a cluster of similar HTML documents.

## **Code Explanation**

### 1. **Parsing HTML Documents**
The `parse_html()` function reads each HTML file, extracts the plain text content using **BeautifulSoup**, and also extracts the tags, CSS classes, and inline styles for further analysis. This provides a comprehensive understanding of the document beyond just the raw text.

### 2. **Generating Feature Vectors**
The `featureVector()` function combines the extracted text, tags, classes, and inline styles into a single feature vector. This vector is essentially a string of the text content and counts of various HTML elements. The counts are represented as `tag:count`, `class:count`, and `style:count` to capture the structural and styling aspects of the document.

### 3. **TF-IDF Transformation**
The **TF-IDF vectorizer** is used to convert the textual content into numerical form, taking into account the importance of words within the document as well as across the entire corpus. This ensures that documents are clustered based on meaningful words while ignoring common, unimportant words.

#### **TF-IDF Formula Explanation**

- **Term Frequency (TF)**: Measures how frequently a term (word) appears in a document. It is calculated as:

TF(t) = Number of times term t appears in the document / Total number of terms in the document

- **Inverse Document Frequency (IDF)**: Measures how important a term is across the entire corpus. It is calculated as:

IDF(t) = log (Total number of documents / Number of documents containing term t) 

- **TF-IDF**: The product of TF and IDF gives us the TF-IDF score for a word in a document:

TF-IDF(t) = TF(t) * IDF(t)

The **TF-IDF** score increases for terms that are frequent in a particular document but rare in the entire corpus.

### 4. **Clustering with K-means**
Once we have the **TF-IDF matrix**, which represents the documents as vectors, we apply the **K-means clustering algorithm**. The number of clusters is specified (e.g., 5), and K-means groups similar documents into clusters based on the vectorized features.

### 5. **Grouping Documents by Cluster**
The `group_html()` function coordinates the process by:
- Parsing all the HTML documents.
- Generating the TF-IDF matrix.
- Running K-means clustering.
- Grouping the documents based on the cluster labels.

### 6. **Running the Code**
To run the code on a dataset, specify the directory of the HTML files (e.g., `tier1`, `tier2`, etc.) and choose the number of clusters. The program will output the HTML files grouped by similarity.

## **Results**

The program groups HTML files based on their content, structure, and styling. After running the code, the output will display each cluster and the files that belong to it.

Each cluster will contain HTML documents that are similar to each other based on the features extracted (text, tags, classes, and styles).

## **Reasoning Behind the Approach**

- **Why TF-IDF?**: TF-IDF is an efficient way to vectorize text, allowing us to capture the important words in the HTML content while ignoring less relevant, frequently occurring words.
- **Why K-means?**: K-means is a straightforward and effective clustering algorithm for grouping similar documents based on their feature vectors. It is chosen because it works well with TF-IDF features and provides clear, understandable clusters.
- **Why DOM structure and styling?**: In addition to the textual content, DOM structure and styling provide additional context about how a page is laid out and styled, which can be important for grouping visually similar pages. By counting tags, classes, and inline styles, we incorporate this structural and styling information into the clustering process.