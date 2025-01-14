import logging
from change_address import change_sensor_address
from read_force import read_sensor_force


# Configure logging
logging.basicConfig(
    filename="main.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("Program started.")
    
    print("Welcome to the Sensor Manager!")
    print("1. Change the I2C address of the sensor")
    print("2. Read force data from the sensor")
    print("3. Exit")

    while True:
        try:
            choice = input("Enter your choice (1/2/3): ").strip()
            if choice == "1":
                logging.info("User chose to read force data.")
                read_sensor_force()
                break
            elif choice == "2":
                logging.info("User chose to change the sensor address.")
                change_sensor_address()
                break
            elif choice == "3":
                logging.info("User exited the program.")
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                logging.warning(f"Invalid menu choice: {choice}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
