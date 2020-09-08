# PocketVNA Repository

Here is a simple enough interface library to use the pocketVNA to scan S-parameters for a given set of frequency inputs, save the output to complex numpy arrays and finally plot the 4 S-parameters in separate matplotlib subplots (2 plots in each, one real and one imaginary).

Using the library is simple, it only involves importing the library (the VectorNetworkAnalyzer library), along with numpy.

To use the library, only a few steps are required:

1. Initialize an object of type VectorNetworkAnalyzer.
2. Setup the VNA with.
3. Generate a list of frequencies (or just one specific frequency) and choose the amount of “averaging” you want, as the pocketVNA functions by measuring the same S-parameter and averaging it.
4. Scanning your frequency range (or the one)
5. Plotting your frequencies
6. Closing the VNA

``` python
from VectorNetworkAnalyzer import *
import numpy as np
 
#Initializing and setting up the VNA
VNA = VectorNetworkAnalyzer()
VNA.setup()
 
#Setting up the frequency list/singular frequency and the amount of measurements (average)
freq_list = np.linspace(1000,10000,10)
average = 10
freq = 1000
 
#Doing a scan of a single frequency
s_list = VNA.single_scan(average, freq)
print(s_list)
 
#Doing a scan of the entire frequency list
s_list = VNA.scan_frequency_range(average,freq_list)
print(s_list)
 
#Plotting the results
VNA.plot_s_vals(freq_list,s_list, 4)
 
#Closing the VNA
VNA.close()

```
