# Motor-Imagery-using-EEG-signals
# Objective
This project aims to aid people with motor defects by using their brain EEG signals to predict the intended body movement.  

# Dataset
The dataset has been taken from https://www.bbci.de/competition/iv/
<br> There are various datasets available as per the number of electrodes used in the EEG skull cap. For reference data for 22 channel has been provided in this repositiory.
<br>
<br>
![image](https://github.com/user-attachments/assets/174da9c0-db14-4956-bf71-730e0e7a7091)


# Data Preprocessing
EEG lab, a matlab tool has been used to convert .gdf files to .csv for efficent usage. The columns represent the 22 electrodes placed all over the skull, while the rows represent the voltage at these electrodes over time.
By analysing the datasets, we labeled the training datasets with a ground truth value of 1,2,3,4 based on left arm, right arm, foot and tongue movement as given by EVENT.TYPE in the dataset.
<br>
We removed 0 and NAN values from the csv files and applied baseline correction using EEG Lab.
We then applied a bandwidth filter of 10-30Hz. These bands are particularly relevant when studying or classifying motor tasks, as they reflect brain activity related to motor control, movement planning, and execution. 
<br>
<br>
![image](https://github.com/user-attachments/assets/69651634-9c7c-4efc-96e9-c6a1898c70bd)

<br>

Even after applying a bandpass filter, there can still be residual noise or small fluctuations in the EEG data that affect signal clarity. The Savitzky-Golay (S-G) filter is applied because it provides additional smoothing without distorting the critical features of the signal, such as peaks and edges, which are important for analysis. In order to apply the savitzky golay filter, we needed to find the appropriate window for the critical channels - 8 C3, 10 Cz, 12 C4
1) Code 1: To find the optimal window for each of the 3 channels
2) Code 2: Out of the 3 optimal windows we selected the one with minimum log dispersion
3) Code 3: Applied savitzky golay for that window and polynomial factor of 3
   
<br>
<br>
<br>

![image](https://github.com/user-attachments/assets/787f7795-ff33-48ad-bab3-7d04fbf6af0c)

<br>
Normalization and Standardization:
<br>
We then applied zscore standardization and min-max normalization.
<br>

![image](https://github.com/user-attachments/assets/1341f45b-e2fb-4d0a-a878-d9e3b8ce38ac)

We are now working to extract spatial temporal features from this dataset and fuse them together. 
Proceeding further, we divided the data as per their ground label and we extracted temporal features using LSTM with skip connections, and spacial features using Residual connections. We then removed irrelevant features that displayed a lot of zero values.  We then mixed the ground labels for temporal and spacial data. Finally we fused the temporal and spacial data to have one file with mixed ground labels using feature pyramid fusion.

We will now use this as an input to find out accuracy.






 

