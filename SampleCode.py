from VectorNetworkAnalyzer import *
import numpy as np

VNA = VectorNetworkAnalyzer()
VNA.setup()

freq_array = np.linspace(1000,100000,10)
average = 10

s_list = VNA.single_scan(average, 10000)
print(s_list)

s_list = VNA.scan_frequency_range(freq_array,average)
print(s_list)



VNA.plot_s_vals(freq_array,s_list, 4)

VNA.close()