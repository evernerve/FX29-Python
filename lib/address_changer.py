import logging
import os
from time import sleep
from lib.FX29Sensor import FX29Sensor

# LOGGING
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "sensor_address_change.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def change_sensor_address():
    logging.info("address_changer started.")
    
    default_old_address = 0x28

    # define old and new sensor addresses
    old_address_input = input(f"Enter the old I2C address in hex (if {hex(default_old_address)}, hit enter): ")
    if old_address_input.strip() == "":
        old_address = default_old_address
        logging.info(f"No input for old address. Using default: {hex(old_address)}.")
    else:
        try:
            old_address = int(old_address_input, 16)
            logging.info(f"User entered old address: {hex(old_address)}.")
        except ValueError:
            logging.error("Invalid hex address entered for old address. Exiting.")
            print("Invalid hex address entered. Exiting...")
            return

    new_address_input = input("Enter the new I2C address in hex: ")
    try:
        new_address = int(new_address_input, 16)
        logging.info(f"User entered new address: {hex(new_address)}.")
    except ValueError:
        logging.error("Invalid hex address entered for new address. Exiting.")
        print("Invalid hex address entered. Exiting...")
        return

    # Initialize the sensor
    try:
        sensor = FX29Sensor(device_address=old_address)
    except Exception as e:
        logging.error(f"Failed to initialize sensor at {hex(old_address)}. Error: {e}")
        print("Failed to initialize the sensor. Exiting...")
        return

    sleep(0.001)

    # Change the address
    try:
        sensor.change_address(old_address, new_address)
        
    except Exception as e:
        logging.error(f"Error when changing the address from {hex(old_address)} to {hex(new_address)}: {e}")
        print("Error when changing the address: " + str(e))

    logging.info("address_changer completed.")

change_sensor_address()