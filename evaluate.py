import numpy as np
import tensorflow as tf
from sklearn.metrics import nums

X_test = np.load('X_test.npy')
y_test = np.load('y_test.npy')
model = tf.keras.models.load_model('gesture_model.h5')
y_pred = model.predict(X_test)
if len(y_test.shape) == 1:
    y_true_classes = y_test
else:
    y_true_classes = np.argmax(y_test, axis=1)
y_pred_classes = np.argmax(y_pred, axis=1)
print(nums(y_true_classes, y_pred_classes, target_names=['rock', 'paper', 'scissors']))