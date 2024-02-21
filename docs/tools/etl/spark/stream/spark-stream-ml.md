# Spark Streaming: ML

[MLlib](https://spark.apache.org/docs/latest/mllib-guide.html) is Apache Spark’s
scalable machine learning library consisting of common learning algorithms and
utilities.

**Tested with 4 Classifiers**:

```text
1. Decision Tree
2. LogisticRegression
3. NaiveBayes
4. RandomForest
```

## Set Pipeline

```scala
// Indesing Label
val labelIndexer = new StringIndexer()
        .setInputCol("flower")
        .setOutputCol("indexedFlower")
        .fit(transformed_data)

// Automatically identify categorical features, and index them.
val featureIndexer = new VectorIndexer()
        .setInputCol("features")
        .setOutputCol("indexedFeatures")
        .setMaxCategories(4)
        .fit(transformed_data)

// Convert indexed labels back to original labels.
val labelConverter = new IndexToString()
        .setInputCol("prediction")
        .setOutputCol("predictedLabel")
        .setLabels(labelIndexer.labels)

// Declaring ML Pipeline
val pipeline = new Pipeline()
```

=== "Decision Tree"

    ```scala
    // Train a DecisionTree
    val dt: DecisionTreeClassifier = new DecisionTreeClassifier()
            .setLabelCol("indexedFlower")
            .setFeaturesCol("indexedFeatures")

    // Setting stages in the ML Pipeline
    pipeline.setStages(Array(labelIndexer, featureIndexer, dt, labelConverter))
    ```

=== "Logistic Regression"

    ```scala
    // Train the Logistic Regression.
    val lr: LogisticRegression = new LogisticRegression()
            .setLabelCol("indexedFlower")
            .setMaxIter(10)
            .setRegParam(0.3)
            .setElasticNetParam(0.8)
            .setFamily("multinomial")

    // Setting stages in the ML Pipeline
    pipeline.setStages(Array(labelIndexer, featureIndexer, lr, labelConverter))
    ```

=== "Naive Bayes"

    ```scala
    // Train the Naive Bayes
    val nb: NaiveBayes = new NaiveBayes().setLabelCol("indexedFlower")

    // Setting stages in the ML Pipeline
    pipeline.setStages(Array(labelIndexer, featureIndexer, nb, labelConverter))
    ```

=== "Random Forest"

    ```scala
    // Train a RandomForest
    val rf: RandomForestClassifier = new RandomForestClassifier()
            .setLabelCol("indexedFlower")
            .setFeaturesCol("indexedFeatures")
            .setNumTrees(10)

    // Setting stages in the ML Pipeline
    pipeline.setStages(Array(labelIndexer, featureIndexer, rf, labelConverter))
    ```

## References

- [Machine Learning with Spark Streaming](https://blog.clairvoyantsoft.com/machine-learning-with-spark-streaming-281b2d1e4fd5)
