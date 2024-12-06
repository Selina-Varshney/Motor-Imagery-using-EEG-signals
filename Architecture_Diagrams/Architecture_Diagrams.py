# import pandas as pd
# import numpy as np
# from tensorflow.keras import layers, Model, Input
# from tensorflow.keras.utils import plot_model
#
# # Load Temporal and Spatial Feature files, excluding the ground truth column
# temporal_data = pd.read_csv(r"C:\Users\selin\Desktop\capstone\mixed_temporal_skip.csv")
# spatial_data = pd.read_csv(r"C:\Users\selin\Desktop\capstone\mixed_spatial_residual_modified.csv")
#
# temporal_features = temporal_data.iloc[:, :-1].to_numpy()  # Exclude ground truth (last column)
# spatial_features = spatial_data.iloc[:, :-1].to_numpy()  # Exclude ground truth (last column)
#
# # Ensure the same number of samples
# assert temporal_features.shape[0] == spatial_features.shape[0], "Temporal and spatial features must have the same number of samples"
#
# # Reshape features to match for CNN processing if needed
# n_samples = temporal_features.shape[0]
#
# # Define the input shape for the temporal and spatial features
# temporal_input = Input(shape=(temporal_features.shape[1], 1), name="Temporal_Input")
# spatial_input = Input(shape=(spatial_features.shape[1], 1), name="Spatial_Input")
#
# # Pad the temporal features to match the spatial feature dimensions (from 32 to 36 columns)
# padded_temporal = layers.ZeroPadding1D(padding=(0, spatial_features.shape[1] - temporal_features.shape[1]))(temporal_input)
#
# # Temporal Feature Pyramid
# temporal_scale1 = layers.Conv1D(64, 3, activation='relu', padding='same')(padded_temporal)
# temporal_scale2 = layers.MaxPooling1D(pool_size=2)(temporal_scale1)
# temporal_scale3 = layers.MaxPooling1D(pool_size=2)(temporal_scale2)
#
# # Spatial Feature Pyramid
# spatial_scale1 = layers.Conv1D(64, 3, activation='relu', padding='same')(spatial_input)
# spatial_scale2 = layers.MaxPooling1D(pool_size=2)(spatial_scale1)
# spatial_scale3 = layers.MaxPooling1D(pool_size=2)(spatial_scale2)
#
# # Global Average Pooling to make the shapes compatible for concatenation
# temporal_scale1 = layers.GlobalAveragePooling1D()(temporal_scale1)
# temporal_scale2 = layers.GlobalAveragePooling1D()(temporal_scale2)
# temporal_scale3 = layers.GlobalAveragePooling1D()(temporal_scale3)
#
# spatial_scale1 = layers.GlobalAveragePooling1D()(spatial_scale1)
# spatial_scale2 = layers.GlobalAveragePooling1D()(spatial_scale2)
# spatial_scale3 = layers.GlobalAveragePooling1D()(spatial_scale3)
#
# # Feature Fusion using Pyramid Fusion (Concatenate features from different scales)
# merged_scale1 = layers.concatenate([temporal_scale1, spatial_scale1], axis=-1)
# merged_scale2 = layers.concatenate([temporal_scale2, spatial_scale2], axis=-1)
# merged_scale3 = layers.concatenate([temporal_scale3, spatial_scale3], axis=-1)
#
# # Final merged representation
# fused_features = layers.concatenate([merged_scale1, merged_scale2, merged_scale3], axis=-1)
#
# # Flatten the fused features to feed into a dense layer
# fused_flatten = layers.Flatten()(fused_features)
# fused_output = layers.Dense(128, activation='relu')(fused_flatten)
#
# # Define the model
# fusion_model = Model(inputs=[temporal_input, spatial_input], outputs=fused_output)
#
# # Compile the model (you can use different loss functions and optimizers as per your needs)
# fusion_model.compile(optimizer='adam', loss='mse')
#
# # Print the model summary
# fusion_model.summary()
#
# # Generate and save the architecture diagram
# plot_model(fusion_model, to_file='model_architecture.png', show_shapes=True, show_layer_names=True, dpi=300)
#
# print("Model architecture diagram has been saved as 'model_architecture.png'.")



import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.utils import plot_model

# Load your EEG data file
# Assuming your data is in a CSV format and the last column is ground truth
eeg_data = pd.read_csv(r"C:\Users\selin\Desktop\BCICIV_2a_gdf\label_1_data.csv")  # Replace with the actual file path
eeg_data = eeg_data.iloc[:, :-1].to_numpy()  # Exclude the last column (ground truth)

# Parameters
window_size = 500  # Window size of 500 rows (samples)
n_columns = 59  # The number of features (columns in the data), excluding the ground truth column

# Function to create windows for spatial feature extraction
def create_windows(data, window_size):
    windows = []
    for i in range(0, len(data) - window_size + 1, window_size):
        window = data[i:i + window_size, :]
        windows.append(window)
    return np.array(windows)

# Create windows
eeg_windows = create_windows(eeg_data, window_size)
print(f"Shape of EEG windows: {eeg_windows.shape}")

# CNN Model with Residual Connections for Spatial Feature Extraction
def build_cnn_residual_model(input_shape):
    inputs = layers.Input(shape=input_shape)

    # First convolutional block
    x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)

    # Residual block 1
    residual = x
    x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.add([x, residual])  # Skip connection
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)

    # Residual block 2
    residual = x
    x = layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)

    # Project residual to match the number of filters (64)
    residual = layers.Conv2D(64, (1, 1), padding='same')(residual)

    # Add the skip connection
    x = layers.add([x, residual])
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)

    # Fully connected layer for feature extraction
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)
    outputs = layers.Dense(64, activation='relu')(x)  # Output layer for spatial features

    model = Model(inputs, outputs)
    return model

# Building the CNN model
input_shape = (window_size, n_columns, 1)  # Add channel dimension for Conv2D
cnn_model = build_cnn_residual_model(input_shape)

# Compile the model
cnn_model.compile(optimizer='adam', loss='mse')

# Generate and save the architecture diagram
plot_model(cnn_model, to_file='cnn_model_architecture.png', show_shapes=True, show_layer_names=True, dpi=300)

print("Model architecture diagram has been saved as 'cnn_model_architecture.png'.")


