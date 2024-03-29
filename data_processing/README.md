# CAMS-Dialogue-Annotation-Data-Processing

The data_processing directory contains the Python scripts for calculating inter-annotator agreement and analysing the
agreement, rating and timing data produced in the study.

The [results.ipynb](/data_processing/results.ipynb) contains results for all experiments reported.

## Directories
- label_data - contains all DA, AP and AP type distance matrices, generated with label_distance_utilities.py,
 and DA label tree data.
- results - contains agreement, distribution, rating and timing analysis results generated with process_data.py.
Including .csv files of results and statistics and .png plots.

## Scripts
- process_data.py runs all the data analysis used within the study and saves to the results directory.
- agreement_statistics.py - contains functions for calculating agreement coefficients.
- label_data_utilities.py, rating_data_utilities.py and timing_data_utilities.py - contain functions for processing and
analysis of their respective data type.
- stats_utilities.py, plot_utilities.py and data_utilities.py - contain helper functions for calculating statistics,
generating plots and processing/saving data.
  
## DA Relationship Graph
Calculation of inter-annotator agreement using weighted agreement coefficients used distance functions defined in
label_distance_utilities.py
The following depicts the undirected graph used for DA labels. Leaf nodes are DA, while intermediate nodes represent
the communicative function subcategories. 

<p align="center">
<img src="/data_processing/label_data/DA Tree Diagram.png" width="1100">
</p>