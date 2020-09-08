import pocketvna
import math
import matplotlib.pyplot as plt

class VectorNetworkAnalyzer:
    def __init__(self):
        
        print("Setting up Vector Network Analyzer:")
        
        #Getting the driver version and pi (why not)
        v, pi = pocketvna.driver_version()
        print('pocketvna.driver_version() => VERSION: {}, PI: {}\n'.format(v, pi))

        self.driver = pocketvna.Driver()

        if self.driver.count() < 1:
            print('No device is detected. Connect and call enumerate() again')
            exit(1)
        else:
            print("Driver Amount: {}".format(self.driver.count()))
        
        if not self.driver.connect_to(0):
            print('Failed to connect')
            exit(2)
        
        print("Driver info:\n")
        print(self.driver.info_at(0))
        self.min_frequency = 0 
        self.max_frequency = 0
        
    def test_request(self):
    
        #In most cases, if device is disconnected during any call PocketVnaHandlerInvalid exception is raised
        try:
            print('TEST REQUST: ')
            r, s = driver.test_req()
        
            print(' '.join(["%02x " % x for x in r]).strip(), "x", s)
        
            test_is_ok = ( r[0] == 0 and  r[7] == 0x0d and r[4] == 0x0d )
            if not test_is_ok:
                print("BAD TEST RESULT!!")
                print('')
            else:

                r, s = driver.read_internal_buffer()
                print(' '.join(["%02x " % x for x in r]).strip(), "x", s)
        except:
            print("Error in Test Request")
            pocketvna.close_api()

            
    
    def S_Params_And_Versions(self):
            
        nps = ''
        print("Finding S params available")
        if self.driver.has_s11(): 
            nps = nps + " S11 "
        if self.driver.has_s21(): 
            nps = nps + " S21 "
        if self.driver.has_s12(): 
            nps = nps + " S12 "
        if self.driver.has_s22(): 
            nps = nps + " S22 "
    
        firmware_version = self.driver.version()
        
        self.nps = nps
        self.firmware = firmware_version
        
        print('Supports: {}, Firmware: {}\n'.format(nps, firmware_version))

    def get_Impedance(self):
        
        #GET Characteristic Impedance (Zero Resistance/Impedance; Reference Impedance/Resistance).
        #Usually it is 50Ohms
        self.impedance = self.driver.Z0()
        
        print("Z0: {} Ohms".format(self.impedance))
        
    def get_Frequency_Range(self):
        # Get working frequency. Usually [100_KHz; 6 GHz]. It is a range device claims to process correctly
        start, end = self.driver.valid_frequency_range()
        #self.min_frequency, self.max_frequency = start, end
        print('Frequncy range = {} to {}\n'.format(start, end))
        
        
    def setup(self):
        self.test_request()
        self.S_Params_And_Versions()
        self.get_Impedance()
        self.get_Frequency_Range()

        print("Setup was sucessful")
        return 0
            

        
    def single_scan(self, frequency, average=10):
        try:
            print('Single Scan (S11, S21, S12, S22 parameters): ')
            s11, s21, s12, s22 = self.driver.single_scan(frequency, average,  pocketvna.NetworkParams.ALL)
            
            return s11, s21, s12, s22
        
        except Exception as e:
            print("Exception: {}".format(e))
            pocketvna.close_api()
            print("F")
            return [0,0,0,0]
        
    def scan_frequency_range(self,freq_array,average=10):

        try:
            print('Frequency Vector Scan (S11, S21, S12, S22 parameters):')
            print(freq_array)
            s11, s21, s12, s22 = self.driver.scan(freq_array, average,  pocketvna.NetworkParams.AllSupported)
            print("Done")
            return s11, s21, s12, s22
        
        except Exception as e:
            print("Exception: {}".format(e))
            pocketvna.close_api()
            print("yes")
            return [0,0,0,0]
    
    def plot_s_vals(self,freq_array, s_list,num_s):
        
        fig, axs = plt.subplots(2, 2)
       
        try:
            s = ["${S}_{11}$", "${S}_{21}$","${S}_{12}$","${S}_{22}$"]
            for i in range(0,num_s,1):
                try:
                    real_S = s_list[i].real
                    imag_S = s_list[i].imag
                except Exception as e:
                    real_S = s_list[i]
                    imag_S = s_list[i]
                
                axs[i//2,i%2].plot(freq_array,real_S,color="red",label="Real component")
                axs[i//2,i%2].plot(freq_array,imag_S,color="blue",label="Imaginary component")
                axs[i//2,i%2].legend(loc="upper right")
                axs[i//2,i%2].set_xlabel("Frequency (Hz)")
                axs[i//2,i%2].set_ylabel(s[i])
            plt.show()
        except:
            self.driver.close()
            pocketvna.close_api()
            print("problem plotting :(")
            return [0,0,0,0]
            
            
    def close(self):
        self.driver.close()
        try:
            pocketvna.close_api()
            print("Sucessfully closed")
        except Exception as e:
            print("not closed :( ")
            print("Exception: {}".format(e))
            pocketvna.close_api()
            
            
