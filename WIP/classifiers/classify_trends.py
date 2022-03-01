import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns   #for data visualization

from sklearn import tree
from sklearn.metrics import accuracy_score, precision_score, f1_score

from sklearn.neighbors import NeighborhoodComponentsAnalysis, KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline



for i in os.listdir("data"):
    if ("lock" not in str(i)):
        file_loc = "data/" + str(i)
        df = pd.read_csv(file_loc)
        df.dropna(inplace=True)

        print(df.columns)
        pruned_data = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'prices_usd', 'market_caps', 'total_volumes',
        'unix_timestamp', 'Unix_Timestamp_Difference', 'Price_Shift', 'day_of_week'], axis=1)

        print('------------')
        print(pruned_data.head())

        dataY = pruned_data["shift_classification"] 
        dataX = pruned_data.drop(["shift_classification"], axis=1)


        X = dataX.values
        y = dataY.values
        """
        performance = []
        for i in range(5):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
            clf = tree.DecisionTreeClassifier(criterion='gini', max_depth=3)
            clf = clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)

        performance.append([accuracy_score(y_test, y_pred), precision_score(y_test, y_pred, average='weighted'), f1_score(y_test, y_pred, average='weighted')])
        df = pd.DataFrame(performance, columns=["Accuracy", "Precision", "F-measure"])
        agg = df.aggregate('mean')

        print(df)
        print(f"\nFinal average:\n{agg}")
        agg.plot.bar()
        """
        #"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
        nca = NeighborhoodComponentsAnalysis()
        knn = KNeighborsClassifier(n_neighbors=5)
        nca_pipe = Pipeline([('nca', nca), ('knn', knn)])
        nca_pipe.fit(X_train, y_train)

        print(nca_pipe.score(X_test, y_test))
        #"""