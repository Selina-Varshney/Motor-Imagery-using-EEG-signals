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
EEG lab, a matlab tool has been used to convert .gdf files to .csv for efficent usage. For example data for 22 channels will have 22 columns each representing data of each electrode.
By analysing the datasets, we labeled the training datasets with a ground truth value of 1,2,3,4 based on left arm, right arm, foot and tongue movement as given by EVENT.TYPE in the dataset.
<br>
We removed 0 and NA values from the csv files and applied baseline correction using EEG Lab.
We then applied a bandwidth filter of 10-30Hz. These bands are particularly relevant when studying or classifying motor tasks, as they reflect brain activity related to motor control, movement planning, and execution. 
<br>
<br>
![image](https://github.com/user-attachments/assets/69651634-9c7c-4efc-96e9-c6a1898c70bd)

<br>

Even after applying a bandpass filter, there can still be residual noise or small fluctuations in the EEG data that affect signal clarity. The Savitzky-Golay (S-G) filter is applied because it provides additional smoothing without distorting the critical features of the signal, such as peaks and edges, which are important for analysis.
<br>
<br>

![image](https://github.com/user-attachments/assets/787f7795-ff33-48ad-bab3-7d04fbf6af0c)

<br>
Normalization and Standardization:
since the data values are greater than 1 , it needs to be normalized.
<br>
<br>

![image](https://github.com/user-attachments/assets/1341f45b-e2fb-4d0a-a878-d9e3b8ce38ac)

We are now working to extract spatial temporal features from this dataset and fuse them together. 






 

