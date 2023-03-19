# intent-classification-shallow-ml
Training an ML classifier to distinguish between intents

To train a multi-class classifier in Python that can distinguish between the intents atis_flight, atis_flight_time, and atis_aircraft, we can use the following steps:

* Load the dataset: The dataset can be loaded using the pandas library in Python.

* Preprocess the data: We need to preprocess the data by converting the text to lowercase, removing punctuation and stop words, and stemming the words.

* Split the data into training and testing sets: We can use the train_test_split() function from scikit-learn to split the data into training and testing sets.

* Extract features: We can extract features from the preprocessed data using the bag-of-words approach. We can use the CountVectorizer from scikit-learn to convert the text data into a matrix of word counts.

* Train the classifier: We can use a classifier such as Naive Bayes, Logistic Regression, or Support Vector Machine to train the model.

* Evaluate the model: We can evaluate the performance of the model using metrics such as accuracy, precision, recall, and F1-score.
