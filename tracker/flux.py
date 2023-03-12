import time
import ADS1263
import RPi.GPIO as GPIO
from log_cfg import logger
import numpy

class quad_flux:
    def __init__(self):
        self.REF = 5.08
        self.channelList = [0, 1, 2, 3]
        self.offsets = [0.0] * len(self.channelList)

    def __enter__(self):
        self.ADC = ADS1263.ADS1263()
        if (self.ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1):
            logger.error("ADC Init Error")
            raise Exception("ADC Init Error") 
        self.ADC.ADS1263_SetMode(0)
        return self

    def clean_up(self):
        self.ADC.ADS1263_Exit()
        pass


    def read(self, samples = 100, sample_delay = .01):
        return_values = [0.0] * len(self.channelList)
        ADC_Value = self.ADC.ADS1263_GetAll(self.channelList) 
        for l in range(samples):
            for i in self.channelList:
                value = 0
                if(ADC_Value[i]>>31 ==1):
                    value = self.REF*2 - ADC_Value[i] * self.REF / 0x80000000
                    #logger.debug("ADC1 IN%d = -%lf" %(i, (self.REF*2 - ADC_Value[i] * REF / 0x80000000)))
                else:
                    value = ADC_Value[i] * self.REF / 0x7fffffff
                    #logger.debug("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * self.REF / 0x7fffffff)))   # 32bit

                return_values[i] = return_values[i] + value

            time.sleep(sample_delay)
        for i in range(  len(self.channelList) ):
            return_values[i] = (return_values[i] / samples) + self.offsets[i]
 
        return return_values

    def normalize(self,samples = 1000, sample_delay = .01):
        data = self.read( samples, sample_delay)
        mean = numpy.mean(data)
        for i in range(  len(self.channelList) ):
            self.offsets[i] = mean - data[i]
        
        return mean

    def __exit__(self, exc_type, exc_value, traceback):
        self.clean_up()

  
if __name__ == '__main__':
    from db_con import get_db, get_cursor
    #create table flux_data_array(s1 numeric, s2 numeric, s3 numeric, s4 numeric);
    db = get_db()
    cur = get_cursor(db)
    with  quad_flux() as flux_g:
        data = flux_g.read()
        cur.execute("insert into flux_data_array( ? , ? , ? ,?)", data)
        db.commit()
        time.sleep(.1)




