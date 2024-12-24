# FX29 Force Sensor I2C Control

This project provides a Python interface to control and read data from the FX29 Force Sensor via I2C. It includes functionality to calibrate the sensor, change its I2C address, and read force data. The project also supports logging and data plotting features.

## Features
- Read force data from the FX29 Force Sensor
- Change I2C address of the sensor
- Calibrate the sensor
- Logging of force readings
- Plot force data and save to CSV
- Adjustable sampling rate

## Requirements
- Raspberry Pi or compatible device with I2C support
- Python 3.x
- `RPi.GPIO`, `smbus`, `matplotlib`, `logging`, `time`, and `csv` libraries

To create and run a virtual environment then install the required Python libraries, run in bash:
```bash
./create_venv.sh
```
Then run the script:
```bash
python -m main
```
