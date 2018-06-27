# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Much is this code is at least partially co-opted from https://developers.google.com/machine-learning/crash-course/
# A fantastic and easy to follow TensorFlow tutorial. Check it out!

import pandas as pd
import numpy as np
import IsThisLossHelper as helper
from matplotlib import pyplot as plt
import tensorflow as tf
from sklearn import metrics
import seaborn as sns
import os
import glob
import math

#------------------------------------------------------------------------------------------------
# Google boilerplate with a little bit of personal configuration here.
def train_nn_classification_model(
    learning_rate,
    steps,
    batch_size,
    hidden_units,
    training_examples,
    training_targets,
    validation_examples,
    validation_targets,
    l2_reg_strength = 0.01,
    periods = 10):

  # Caution: input pipelines are reset with each call to train.
  # If the number of steps is small, your model may never see most of the data.
  # So with multiple `.train` calls like this you may want to control the length
  # of training with num_epochs passed to the input_fn. Or, you can do a really-big shuffle,
  # or since it's in-memory data, shuffle all the data in the `input_fn`.
  steps_per_period = steps / periods

  # Create the input functions.
  predict_training_input_fn = helper.create_predict_input_fn(
    training_examples, training_targets, batch_size)
  predict_validation_input_fn = helper.create_predict_input_fn(
    validation_examples, validation_targets, batch_size)
  training_input_fn = helper.create_training_input_fn(
    training_examples, training_targets, batch_size)

  # Create feature columns.
  feature_columns = [tf.feature_column.numeric_column('pixels', shape=10000)]

  # Create a DNNClassifier object.
  my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
  my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
  classifier = tf.estimator.DNNClassifier(
      feature_columns=feature_columns,
      n_classes=2,
      hidden_units=hidden_units,
      optimizer=my_optimizer,
      config=tf.estimator.RunConfig(keep_checkpoint_max=1)
  )

  # Train the model, but do so inside a loop so that we can periodically assess
  # loss metrics.
  print("Training model...")
  print("LogLoss error (on validation data):")
  training_errors = []
  validation_errors = []
  for period in range (1, periods+1):
    # Train the model, starting from the prior state.
    classifier.train(
        input_fn=training_input_fn,
        steps=steps_per_period
    )

    # Take a break and compute probabilities.
    training_predictions = list(classifier.predict(input_fn=predict_training_input_fn))
    training_probabilities = np.array([item['probabilities'] for item in training_predictions])
    training_pred_class_id = np.array([item['class_ids'][0] for item in training_predictions])
    training_pred_one_hot = tf.keras.utils.to_categorical(training_pred_class_id, 2)

    validation_predictions = list(classifier.predict(input_fn=predict_validation_input_fn))
    validation_probabilities = np.array([item['probabilities'] for item in validation_predictions])
    validation_pred_class_id = np.array([item['class_ids'][0] for item in validation_predictions])
    validation_pred_one_hot = tf.keras.utils.to_categorical(validation_pred_class_id, 2)

    # Compute training and validation errors.
    training_log_loss = metrics.log_loss(training_targets, training_pred_one_hot)
    validation_log_loss = metrics.log_loss(validation_targets, validation_pred_one_hot)
    # Occasionally print the current loss.
    print("  period %02d : %0.2f" % (period, validation_log_loss), flush=True)
    # Add the loss metrics from this period to our list.
    training_errors.append(training_log_loss)
    validation_errors.append(validation_log_loss)
  print("Model training finished.")
  # Remove event files to save disk space.
  _ = map(os.remove, glob.glob(os.path.join(classifier.model_dir, 'events.out.tfevents*')))

  # Calculate final predictions (not probabilities, as above).
  final_predictions = classifier.predict(input_fn=predict_validation_input_fn)
  final_predictions = np.array([item['class_ids'][0] for item in final_predictions])


  accuracy = metrics.accuracy_score(validation_targets, final_predictions)
  print("Final accuracy (on validation data): %0.2f" % accuracy)


  # Output a plot of the confusion matrix.
  cm = metrics.confusion_matrix(validation_targets, final_predictions)
  # Normalize the confusion matrix by row (i.e by the number of samples
  # in each class).
  cm_normalized = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
  ax = sns.heatmap(cm_normalized, cmap="bone_r")
  ax.set_aspect(1)
  plt.title("Confusion matrix")
  plt.ylabel("True label")
  plt.xlabel("Predicted label")
  plt.show()


  # Output the first hidden layer of images
  weights0 = classifier.get_variable_value("dnn/hiddenlayer_0/kernel")
  num_nodes = weights0.shape[1]
  num_rows = int(math.ceil(num_nodes / 10.0))
  fig, axes = plt.subplots(num_rows, 10, figsize=(20, 2 * num_rows))
  for coef, ax in zip(weights0.T, axes.ravel()):
      # Weights in coef is reshaped from 1x784 to 28x28.
      ax.matshow(coef.reshape(100, 100), cmap=plt.cm.pink)
      ax.set_xticks(())
      ax.set_yticks(())
  plt.show()

  return classifier
#------------------------------------------------------------------------------------------------

def getIsThisLossModel():
    # Printing often, for entertainment! :)
    print("Reading in your data...")
    picture_dataframe = pd.read_csv(
        "TrainingDataNCG.csv",
        sep = ",",
        header = None)
    print("DONE!")


    print("Reordering your data...")
    picture_dataframe = picture_dataframe.reindex(np.random.permutation(picture_dataframe.index))
    print("DONE!")

    training_targets, training_examples = helper.parse_labels_and_features(picture_dataframe[:1100])
    validation_targets, validation_examples = helper.parse_labels_and_features(picture_dataframe[1100:1400])

    classifier = train_nn_classification_model(
        learning_rate=0.0075,
        steps=5,
        batch_size=15,
        hidden_units=[50, 50],
        training_examples=training_examples,
        training_targets=training_targets,
        validation_examples=validation_examples,
        validation_targets=validation_targets,
        periods=1)

    print("Reading in your test data...")
    test_dataframe = pd.read_csv(
        "TestDataNCG.csv",
        sep = ",",
        header = None)
    print("DONE!")

    test_targets, test_examples = helper.parse_labels_and_features(test_dataframe)
    predict_test_input_fn = helper.create_predict_input_fn(
        test_examples, test_targets, batch_size=50)

    evaluation_metrics = classifier.evaluate(input_fn=predict_test_input_fn)

    print("AUC on the test set: %0.2f" % evaluation_metrics['auc'])
    print("Accuracy on the test set: %0.2f" % evaluation_metrics['accuracy'])
    print("Precision on the test set: %0.2f" % evaluation_metrics['precision'])
    print("Recall on the test set: %0.2f" % evaluation_metrics['recall'])

    save = input("\nWould you like to use the model? (y/n)")
    while save != "y" and save != "n":
        save = input("Not a valid answer.\nWould you like to save the model? (y/n)\n")
    if save == "y":
        return classifier, evaluation_metrics['accuracy']
    else:
        #Try again!
        return getIsThisLossModel()
