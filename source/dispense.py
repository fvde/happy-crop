import RPi.GPIO as GPIO
import time
import logging

class DispenseModule():
    """ This class may only be instantiated once, because otherwise eletrical/mechanical
    errors due to inconsistent control of pumps/valves may occur"""
    instance_counter = 0
    def __init__(self, logger):
        self.logger = logger
        self.valve_dict = {0:11,1:13,2:15,3:19,4:21,5:23} #these are the physical pins on the pcb board
        self.pump = 37 # this is the physical pin on the pcb board
        
        DispenseModule.instance_counter = DispenseModule.instance_counter + 1
        if DispenseModule.instance_counter > 1:
            self.logger.error("Too much instances of DispenseModule, this is not possible!")
            raise Exception("Too much instances of DispenseModule, this is not possible")
            
            
    def dispense(self, valves, times):
        """ this method accepts a list of valves (0-5) and a list of times, size of lists must be identical
        the valves will be opened for the specified time in seconds"""
        try:
            # configuration of output ports
            self.logger.info(f"Starting to dispense, input valves: {valves}, input times: {times}")
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(list(self.valve_dict.values()), GPIO.OUT)
            GPIO.setup(self.pump, GPIO.OUT)
            
            # start pump first to apply pressure
            self.logger.info("Activating pump")
            GPIO.output(self.pump, 1)
            time.sleep(1)
            for counter, i in enumerate(valves):
                self.logger.debug(f"Dispensing at valve {self.valve_dict[i]} / {i} for {times[counter]} seconds")
                GPIO.output(self.valve_dict[i], 1)
                time.sleep(times[counter]) # this is the actual dispense time
                GPIO.output(self.valve_dict[i], 0)
                self.logger.info(f"Finished dispensing at valve {self.valve_dict[i]} / {i} for {times[counter]} seconds")
                time.sleep(0.5) # time to let the valve close
            GPIO.output(self.pump, 0) # stop pump after dispensing
                
        finally:
            GPIO.cleanup()
    
if __name__ == '__main__':
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(module)s - linenumber: %(lineno)d - %(message)s')
    logger = logging.getLogger('Dispense')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    stream.setLevel(logging.DEBUG)
    logger.addHandler(stream)

    filehandler = logging.FileHandler('dispense.log', mode ='a')
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    # example usage
    examplevalves =[0,1,2,3,4,5]
    exampletimes =[2,2,2,1,3,1]
    dispensemodule = DispenseModule(logger)
    dispensemodule.dispense(examplevalves, exampletimes)
