import time
import os
import logging
import csv
import matplotlib.pyplot as plt

from lib.FX29Sensor import FX29Sensor

# # Configure logging
# log_dir = "logs"
# os.makedirs(log_dir, exist_ok=True)
# logging.basicConfig(
#     filename=os.path.join(log_dir, "sensor_readings.log"),
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

def define_sampling_rate():
    default_sampling_rate = 0.1
    while True:
        try:
            sampling_rate_input = input(f"Enter the sampling rate in seconds (default is {default_sampling_rate}): ").strip()
            if sampling_rate_input.strip() == "":
                sampling_rate = default_sampling_rate
                logging.info(f"No input for sampling rate. Using default: {sampling_rate} seconds.")
                break
            sampling_rate = float(sampling_rate_input)
            if sampling_rate <= 0:
                raise ValueError("Sampling rate must be greater than zero.")
            logging.info(f"User set sampling rate to {sampling_rate} seconds.")
            break
        except ValueError as e:
            print("Invalid input. Please enter a valid positive number for the sampling rate.")
            logging.warning(f"Invalid sampling rate input: {sampling_rate_input}. Error: {e}")
    return sampling_rate

def log_force_data_to_csv(sensor, sampling_rate, filename):
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header if the file is empty
        if file.tell() == 0:
            writer.writerow(["Timestamp", "Force (N)"])
        
        # Continuous force reading and logging
        try:
            timestamp = 0  # Initial timestamp
            while True:
                try:
                    force = sensor.read_force()
                    if force is not None:
                        print(f"Force: {force:.2f} N at {timestamp}")
                        writer.writerow([timestamp, force]) 
                        file.flush()
                        timestamp += 1  
                    time.sleep(sampling_rate)
                except Exception as e:
                    logging.error(f"Error during force reading: {e}")
                    print("Error: " + str(e))
        except KeyboardInterrupt:
            logging.info("Program interrupted by the user.")
            print("\nProgram terminated by the user.")



def plot_force_curve_from_csv(csv_file_path, output_image_path):
    try:
        # Read data from the CSV file
        timestamps = []
        forces = []

        with open(csv_file_path, mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                timestamps.append(float(row[0]))
                forces.append(float(row[1]))

        # Generate a plot
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, forces, label="Force (N)", color="blue")
        plt.xlabel("Time (s)")
        plt.ylabel("Force (N)")
        plt.title("Force vs. Time")
        plt.legend()
        plt.grid(True)

        # Save the plot as an image
        plt.savefig(output_image_path)
        print(f"Force curve saved as {output_image_path}")
        plt.close()

    except Exception as e:
        logging.error(f"Error while plotting force curve: {e}")
        print(f"Error while plotting force curve: {e}")



def read_force():
    logging.info("Program started.")

    # Sensor Address 
    default_address = 0x28
    address_input = input(f"Enter the I2C address in hex (if {hex(default_address)}, hit enter): ")
    if address_input.strip() == "":
        address_input = default_address
        logging.info(f"No input for given address. Using default: {hex(default_address)}.")
    else:
        try:
            address_input = int(address_input, 16)
            logging.info(f"User entered address: {hex(address_input)}.")
        except ValueError:
            logging.error("Invalid hex address entered for given address. Exiting.")
            print("Invalid hex address entered. Exiting...")
            return
    
    
   # Prompt user for the sampling rate
    sampling_rate = define_sampling_rate()
    
    # Initialize the sensor
    sensor = FX29Sensor(device_address=address_input)
    logging.info(f"Sensor initialized at {hex(address_input)}.")


    # Default offset and sensitivity values
    default_zero_offset = 0.0  # !TODO Replace with your predetermined offset
    default_sensitivity = 1.0  # !TODO Replace with your predetermined sensitivity

    # Calibrate the sensor (or not)
    user_input = input("calibrate the sensor? (yes/no): ").strip().lower()
    if user_input in ["yes", "y"]:
        logging.info("started calibrating the sensor...")
        while not sensor.calibrate():
            logging.warning("Calibration failed. Trying again...")
            print("Calibration failed. Try again...")
        logging.info(f"Calibration successful. Setting the zero offset to {sensor.zero_offset} and sensitivity to {sensor.sensitivity}.")
    else:
        logging.info("no calibration. Using default offset and sensitivity.")
        sensor.zero_offset = default_zero_offset
        sensor.sensitivity = default_sensitivity
        logging.info(f"Set zero_offset to {default_zero_offset:.2f} and sensitivity to {default_sensitivity:.2f}.")


    log_dir = "./logs"
    csv_filename = "force_data.csv"
    csv_filepath = os.path.join(log_dir, csv_filename)
    log_force_data_to_csv(sensor, sampling_rate, csv_filepath)
    
    plot_filename = "force_data.png"
    plot_path = os.path.join(log_dir, plot_filename)
    plot_force_curve_from_csv(csv_filepath, plot_path)

read_force()