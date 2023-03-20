# intent-classification-shallow-ml
Training an ML classifier to distinguish between intents

# Feature Extraction Pipeline
* Text Preprocessing: The input text data is preprocessed to remove non-alphabetic characters, convert the text to lowercase, tokenize the text into words, stem each word using PorterStemmer, remove stop words, and join the remaining words into a string.

* Label Encoding: The target variable "intent" is encoded into numerical labels using the LabelEncoder() function from scikit-learn library.

* Vectorization: The preprocessed text data is tokenized into sequences using the TfidfVectorizer() function from scikit-learn library. This function converts the text data into a matrix of word frequencies or term frequency-inverse document frequency (TF-IDF) scores, where each row represents a text instance and each column represents a unique word in the vocabulary. The TF-IDF scores measure the importance of a word in a text instance relative to its frequency in the entire dataset.

* Classifier Training: The SVM and Logistic Regression classifiers are trained on the vectorized text data using the fit() method from scikit-learn library.

* Prediction: The trained classifiers are used to make predictions on the vectorized test data using the predict() method from scikit-learn library.

* Evaluation: The accuracy and confusion matrix of the classifiers are computed using the score() and confusion_matrix() methods from scikit-learn library.
