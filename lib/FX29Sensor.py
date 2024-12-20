import logging
import time

import smbus2
import RPi.GPIO as GPIO



class FX29Sensor:
    """
    A class to communicate with the FX29 load cell using I2C.   

    """    

    def __init__(self, bus_number=1, device_address=0x28, register_addr=0x06):
        """
        Initialize the sensor.

        Args:

            bus_number (int): The I2C bus number (default is 1 for RaspPi).

            device_address (int): The I2C address of the sensor (default is 0x28).

            register_addr (int): The register address for force data (default is 0x06).

        """
        self.bus = smbus2.SMBus(bus_number)
        self.device_address = device_address
        self.register_addr = register_addr
        self.zero_offset = 0
        self.sensitivity = 1
        self.power_pin = 4 # GPIO 4 (PIN 7)

        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.power_pin, GPIO.OUT)

    def read_raw_value(self):
        """
        Read the raw value from the FX29 sensor.

        Returns:
        
            int: The raw 16-bit value from the sensor.
        
        """

        self.bus.write_byte(self.device_address, self.register_addr)
        time.sleep(0.01)  
        data = self.bus.read_i2c_block_data(self.device_address, 0x06, 2)
        raw_value = (data[0] << 8) + data[1]
        return raw_value


    def calibrate(self):
        """
        Calibrate the FX29 sensor. First, using no load, then applying a known force.

        Returns:
            
            bool: True if calibration was successful, False otherwise.
        
        """

        input("Ensure the load cell is unloaded, then press Enter...")
        self.zero_offset = self.read_raw_value()
        print(f"The zero offset is: {self.zero_offset}")
      
        known_weight = float(input("Apply a known weight (in Newtons!) and enter the value: "))
        input("Press Enter when the weight is stable...")
        loaded_value = self.read_raw_value()
        
        if loaded_value != self.zero_offset:
            self.sensitivity = known_weight / (loaded_value - self.zero_offset)
            print(f"Sensitivity: {self.sensitivity}")
            print("Load cell calibrated!")
            return True
        else:
            print("Error: Loaded value is the same as zero offset. Please try again.")
            return False



    def read_force(self):
        """
        Read the force value from the calibrated sensor.

        Returns:

            float: The calculated force in Newtons, or None if reading fails.
       
        """

        raw_value = self.read_raw_value()

        if raw_value is not None:

            force = (raw_value - self.zero_offset) * self.sensitivity

            return force

        return None

    

    



    # Changing the I2C address ----------------

    

    def power_up_sensor(self):
        """Power cycle the FX29 sensor."""
        
        GPIO.output(self.power_pin, GPIO.LOW)
        time.sleep(0.1) 
        GPIO.output(self.power_pin, GPIO.HIGH)  
        time.sleep(0.0001)  # Wait for 0.1ms after power-up (less than 6ms window)
    

    def change_address(self, old_address, new_address):

        try:
            # Power up the sensor
            print("Powering up the sensor...")
            self.power_up_sensor()
            print("Sensor powered up.")

            # Step 1: Enter Command Mode
            print("Step 1: Entering command mode...")
            self.bus.write_i2c_block_data(old_address, 0xA0, [0x00, 0x00])
            time.sleep(0.01)
            print("Command mode entered.")

            # Step 2: Command to read EEPROM word 02
            print("Step 2: Sending command to read EEPROM word 02...")
            self.bus.write_i2c_block_data(old_address, 0x02, [0x00, 0x00])
            time.sleep(0.01)
            print("Command to read EEPROM word 02 sent.")

            # Step 3: Fetch EEPROM word 02
            print("Step 3: Fetching EEPROM word 02...")
            data = self.bus.read_i2c_block_data(old_address, 0x00, 3)
            print(f"Received data: {[hex(b) for b in data]}")

            if data[0] != 0x5A:
                print(f"Warning: Unexpected response byte: {hex(data[0])}")
            else:
                print("EEPROM word 02 read successfully.")

            # Step 4: Modify Word 02
            print("Step 4: Modifying EEPROM word 02...")
            word_02 = (data[0] << 8) | data[2]
            new_word_02 = (word_02 & 0x8007) | (new_address << 3) | (0b011 << 10)
            print(f"Modified EEPROM word 02: {hex(new_word_02)}")

            # Step 5: Write new version of Word 02 to sensor EEPROM
            print("Step 5: Writing modified word 02 to EEPROM...")
            high_byte = (new_word_02 >> 8) & 0xFF
            low_byte = new_word_02 & 0xFF
            self.bus.write_i2c_block_data(old_address, 0x42, [high_byte, low_byte])
            time.sleep(0.01)
            print("Modified word 02 written to EEPROM successfully.")

            # Step 6: Exit command mode & start normal operating mode
            print("Step 6: Exiting command mode and starting normal operation...")
            self.bus.write_i2c_block_data(old_address, 0x80, [0x00, 0x00])
            time.sleep(0.01)
            print("Exited command mode. Sensor is now in normal operating mode.")
            
            # Power up the sensor
            print("Restarting the sensor...")
            self.power_up_sensor()
            print("Sensor restarted.")

            
            print(f"I2C address changed successfully from {hex(old_address)} to {hex(new_address)}.")


        except Exception as e:
            print(f"Error changing address: {e}")
            return False






