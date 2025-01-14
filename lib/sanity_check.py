import time
import logging
import sys
import os
import numpy as np

from lib.FX29Sensor import FX29Sensor

 
def sanity_check_sensors(addresses):
    """
    Reads the sensor N times at each address and checks whether
    at least 2 readings differ. If that is true, the sensor
    is deemed 'working properly'.
    """
    print("Starting sensor sanity check...\n")

    results = {}
    for address in addresses:
        print(f"Checking sensor at address {hex(address)}")
        try:
            sensor = FX29Sensor(device_address=address)
        except Exception as e:
            print(f"  [ERROR] Could not initialize sensor at {hex(address)}: {e}")
            continue

        readings = []
        number_of_readings = 5
        for i in range(number_of_readings):
            try:
                force_value = sensor.read_force()
                readings.append(force_value)
                print(f"  Reading {i+1}: {force_value:.2f} N")
                time.sleep(0.1)
            except Exception as e:
                print(f"  [ERROR] Failed to read from sensor at {hex(address)}: {e}")
                readings.append(None)
        
        # Check if the sensor produced at least 2 different force values
        # "None" reading is invalid
        if None in readings:
            print(f"  [FAIL] Sensor at {hex(address)} produced an invalid reading.\n")
            results[hex(address)] = "no values"
        else:
            mean_reading = sum(readings) / len(readings)
            if mean_reading not in [49152, 65535]:
                print(f"  [PASS] Sensor at {hex(address)} is working properly.\n")
                results[hex(address)] = f"works"
            else:
                print(f"  [FAIL] Sensor at {hex(address)} did NOT produce 2 distinct readings.\n")
                results[hex(address)] = f"bad values, {readings[0]}"
    
    print("\nSensor sanity check results:", results)
    logging.info(f"Sensor sanity check results: {results}")


def main():
    # Optional: configure logging if desired
    logging.basicConfig(
        filename="logs/sensor_sanity_check.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Define your sensor addresses
    sensor_addresses = [
        0x11, 0x12, 0x14, 0x15,
        0x31, 0x32, 0x34, 0x35
    ]

    # Define a default sampling rate for reading the sensor
    sampling_rate = 0.1  # seconds between readings

    # Run the sanity check
    sanity_check_sensors(sensor_addresses)
    


if __name__ == "__main__":
    main()