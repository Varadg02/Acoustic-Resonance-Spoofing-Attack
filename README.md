# Acoustic-Resonance-Spoofing-Attack
## Overview
This project provides a Python-based simulation of an **Acoustic Resonance Spoofing Attack** targeting Micro-Electro-Mechanical Systems (MEMS) sensors, such as accelerometers and gyroscopes. The script (`RAS.py`) mathematically models a baseline physical movement, injects a targeted high-frequency resonant acoustic attack, and implements software-level defensive mitigation strategies.

This simulation is highly relevant for hardware security research, digital forensics, and the vulnerability assessment of embedded systems and IoT devices.

##  Features
- **MEMS Signal Simulation**: Generates a clean baseline sine wave representing normal, low-frequency physical movement (e.g., 2Hz).
- **Acoustic Spoofing Injection**: Simulates a targeted acoustic attack by injecting high-frequency noise (e.g., 450Hz) at the sensor's theoretical resonant frequency during a specific time window.
- **Heuristic Anomaly Detection**: Calculates the derivative of the signal to detect physically impossible acceleration rates, instantly flagging the onset of an attack.
- **Signal Mitigation (DSP)**: Applies a 4th-order Butterworth low-pass filter (`scipy.signal.filtfilt`) to strip out the resonant noise without introducing phase distortion.
- **Visualization**: Leverages Matplotlib to plot the clean, attacked, and mitigated signals for side-by-side comparative analysis.

##  Prerequisites
Ensure you have Python 3.7+ installed along with the following required libraries:
- `numpy` (for numerical operations and array generation)
- `scipy` (for advanced signal processing and filtering)
- `matplotlib` (for data visualization)

##  Installation & Execution

1. **Download the Script**:
   Ensure `RAS.py` is saved in your local directory.

2. **Install Dependencies**:
   Open your terminal or command prompt and run: python RAS.py

   How It Works (Under the Hood)
   
   1. simulate_mems_sensor_data():Generates a 2Hz sine wave sampled at 1kHz, simulating standard physical movement over a 10-second window.
   2. inject_noise():Between t = 3.0s and t = 4.5s, a 450Hz high-amplitude signal is superimposed onto the baseline data. This mimics a real-world scenario where an acoustic wave matches the MEMS mass's      resonant frequency, causing it to vibrate uncontrollably and output spoofed data.
   3. detect_anomalies():Acts as a software-based Intrusion Detection System (IDS). By calculating the rate of change ($\Delta amplitude / \Delta time$), it identifies spikes that exceed a predefined physical threshold (e.g., an acceleration that is physically impossible for the device to achieve on its own), flagging them as an anomaly.
   4. butter_lowpass_filter():Acts as the mitigation layer. It uses a 15Hz cutoff frequency to filter out the 450Hz spoofed noise. By utilizing filtfilt, the filter is applied both forward and backward, ensuring the cleaned signal remains perfectly phase-aligned with the original physical movement.

   Author
   Varad Gandhi
