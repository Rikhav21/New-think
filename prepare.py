import os
import json
import numpy as np
from sklearn.model_selection import train_test_split

# Define the gestures and their corresponding labels
gestures = ['rock', 'paper', 'scissors']
label_map = {gesture: i for i, gesture in enumerate(gestures)}

# Function to load data from JSON files
def load_data():
    data = []
    labels = []
    for gesture in gestures:
        gesture_dir = os.path.join(gesture)
        for filename in os.listdir(gesture_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(gesture_dir, filename)
                with open(filepath, 'r') as f:
                    landmark_data = json.load(f)
                    landmarks = landmark_data['landmarks']
                    data.append([lm['x'] for lm in landmarks] + [lm['y'] for lm in landmarks] + [lm['z'] for lm in landmarks])
                    labels.append(label_map[gesture])
    return np.array(data), np.array(labels)

# Load the data and split it into training and testing sets
data, labels = load_data()
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Save the prepared data
np.save('X_train.npy', X_train)
np.save('X_test.npy', X_test)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)