import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def simulate_mems_sensor_data(duration=10.0, sample_rate=1000, frequency=2.0):
    """Generates a clean sine wave representing normal physical movement."""
    # Return both the time array and the data so they remain aligned
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    data = np.sin(2 * np.pi * frequency * t)
    return t, data

def inject_noise(t, data, start_time=3.0, end_time=4.5, noise_freq=450, noise_amp=2.0):
    """Injects high-frequency noise to simulate an acoustic resonance attack."""
    # Use .copy() so we don't accidentally modify the original clean data in-place
    attacked_data = data.copy()
    
    # Define the attack window
    attack_window = (t >= start_time) & (t < end_time)
    
    # Simulate the resonant frequency spoofing
    noise = noise_amp * np.sin(2 * np.pi * noise_freq * t[attack_window])
    attacked_data[attack_window] += noise
    
    return attacked_data


def butter_lowpass_filter(data, cutoff=15.0, fs=1000, order=4):
    """Filters out high-frequency acoustic spoofing noise."""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    
    # Use filtfilt instead of lfilter to apply the filter forward and backward.
    # This prevents phase distortion/shifting in the resulting plot.
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def detect_anomalies(t, data, threshold=500.0, fs=1000):
    """Flags sudden spikes in the signal derivative (physically impossible acceleration)."""
    # Calculate the derivative of the signal (change in amplitude over time dt)
    dt = 1.0 / fs
    signal_derivative = np.diff(data) / dt
    
    # Find indices where the rate of change exceeds the physical threshold
    anomaly_indices = np.where(np.abs(signal_derivative) > threshold)[0]
    
    if len(anomaly_indices) > 0:
        first_anomaly = t[anomaly_indices[0]]
        print(f"⚠️ ANOMALY DETECTED: Physically impossible acceleration rates found at {len(anomaly_indices)} data points.")
        print(f"   -> Attack commenced at approximately t = {first_anomaly:.3f}s")
    else:
        print("✅ No anomalies detected. Signal is within physical limits.")

if __name__ == '__main__':
    # 1. Setup Parameters
    SAMPLE_RATE = 1000  # 1 kHz sampling rate is typical for MEMS
    DURATION = 10.0
    
    # 2. Generate Simulated Data
    t, mems_data = simulate_mems_sensor_data(duration=DURATION, sample_rate=SAMPLE_RATE)

    # 3. Inject Noise into the sensor data (Attack Simulation)
    attacked_data = inject_noise(t, mems_data)

    # 4. Hardware Defense 1: Anomaly Detection
    # Run this on the RAW incoming data, as acoustic spoofing will cause 
    # the derivative of the sine wave to explode beyond physical limits.
    print("Running anomaly detection on incoming sensor data...")
    detect_anomalies(t, attacked_data, threshold=1000.0, fs=SAMPLE_RATE)

    # 5. Hardware Defense 2: Apply Butterworth Filter (Mitigation)
    filtered_data = butter_lowpass_filter(attacked_data, cutoff=15.0, fs=SAMPLE_RATE)

    # 6. Plot the results for comparison
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Clean Data
    plt.subplot(3, 1, 1)
    plt.plot(t, mems_data, label='Normal Movement (Clean)', color='blue', linewidth=2)
    plt.title('MEMS Sensor Original Data')
    plt.ylabel('Amplitude')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc="upper right")

    # Plot 2: Attacked Data
    plt.subplot(3, 1, 2)
    plt.plot(t, attacked_data, label='Attacked Data (Spoofed)', color='red', linewidth=1)
    plt.title('Attacked MEMS Sensor Data (Acoustic Resonance Injection)')
    plt.ylabel('Amplitude')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc="upper right")

    # Plot 3: Mitigated Data
    plt.subplot(3, 1, 3)
    plt.plot(t, filtered_data, label='Filtered Data (Mitigated)', color='green', linewidth=2)
    plt.title('MEMS Sensor Filtered Data (Low-pass Applied)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc="upper right")

    plt.tight_layout()
    plt.show()