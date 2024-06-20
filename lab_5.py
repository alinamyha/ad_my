import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt

# Функція для створення гармонічного сигналу
def harmonic(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

# Функція для створення шуму
def create_noise(t, noise_mean, noise_covariance):
    return np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))

# Функція для створення гармонічного сигналу з шумом
def harmonic_with_noise(t, amplitude, frequency, phase=0, noise_mean=0, noise_covariance=0.1, show_noise=True, noise=None):
    harmonic_signal = harmonic(t, amplitude, frequency, phase)
    if noise is not None and show_noise:
        return harmonic_signal + noise
    elif show_noise:
        return harmonic_signal + create_noise(t, noise_mean, noise_covariance)
    else:
        return harmonic_signal

# Функція для створення фільтра низьких частот
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# Функція для застосування фільтра низьких частот до даних
def lowpass_filter(data, cutoff_freq, fs, order=5):
    b, a = butter_lowpass(cutoff_freq, fs, order=order)
    y = filtfilt(b, a, data)
    return y

class SignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing Application")

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.controls_frame = ttk.Frame(root)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.init_controls()

        self.t = np.linspace(0, 10, 1000)
        self.sampling_frequency = 1 / (self.t[1] - self.t[0])

        self.initial_amplitude = 1.0
        self.initial_frequency = 1.0
        self.initial_phase = 0.0
        self.initial_noise_mean = 0.0
        self.initial_noise_covariance = 0.1
        self.noise_g = create_noise(self.t, self.initial_noise_mean, self.initial_noise_covariance)

        self.plot_signals()

    def init_controls(self):
        ttk.Label(self.controls_frame, text="Amplitude:").pack(side=tk.LEFT)
        self.amplitude_var = tk.DoubleVar(value=1.0)
        ttk.Scale(self.controls_frame, from_=0.1, to=10.0, variable=self.amplitude_var, orient=tk.HORIZONTAL, command=self.update).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.controls_frame, text="Frequency:").pack(side=tk.LEFT)
        self.frequency_var = tk.DoubleVar(value=1.0)
        ttk.Scale(self.controls_frame, from_=0.1, to=10.0, variable=self.frequency_var, orient=tk.HORIZONTAL, command=self.update).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.controls_frame, text="Phase:").pack(side=tk.LEFT)
        self.phase_var = tk.DoubleVar(value=0.0)
        ttk.Scale(self.controls_frame, from_=0.0, to=2 * np.pi, variable=self.phase_var, orient=tk.HORIZONTAL, command=self.update).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.controls_frame, text="Noise Mean:").pack(side=tk.LEFT)
        self.noise_mean_var = tk.DoubleVar(value=0.0)
        ttk.Scale(self.controls_frame, from_=-1.0, to=1.0, variable=self.noise_mean_var, orient=tk.HORIZONTAL, command=self.update_noise).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.controls_frame, text="Noise Covariance:").pack(side=tk.LEFT)
        self.noise_covariance_var = tk.DoubleVar(value=0.1)
        ttk.Scale(self.controls_frame, from_=0.0, to=1.0, variable=self.noise_covariance_var, orient=tk.HORIZONTAL, command=self.update_noise).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.controls_frame, text="Cutoff Frequency:").pack(side=tk.LEFT)
        self.cutoff_frequency_var = tk.DoubleVar(value=3.0)
        ttk.Scale(self.controls_frame, from_=0.1, to=10.0, variable=self.cutoff_frequency_var, orient=tk.HORIZONTAL, command=self.update_filter).pack(side=tk.LEFT, padx=5)

        self.show_noise_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.controls_frame, text="Show Noise", variable=self.show_noise_var, command=self.update).pack(side=tk.LEFT, padx=5)

        ttk.Button(self.controls_frame, text="Regenerate Noise", command=self.regenerate_noise).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.controls_frame, text="Random Params", command=self.random_params).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.controls_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

    def plot_signals(self):
        self.ax.clear()

        amplitude = self.amplitude_var.get()
        frequency = self.frequency_var.get()
        phase = self.phase_var.get()
        noise_mean = self.noise_mean_var.get()
        noise_covariance = self.noise_covariance_var.get()
        cutoff_frequency = self.cutoff_frequency_var.get()
        show_noise = self.show_noise_var.get()

        harmonic_signal = harmonic(self.t, amplitude, frequency, phase)
        noise_signal = harmonic_with_noise(self.t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, noise=self.noise_g)
        filtered_signal = lowpass_filter(noise_signal, cutoff_frequency, self.sampling_frequency)

        self.ax.plot(self.t, harmonic_signal, lw=2, color='black', linestyle=':', label='Harmonic Signal')
        self.ax.plot(self.t, noise_signal, lw=2, color='red', label='Noise Signal')
        self.ax.plot(self.t, filtered_signal, lw=2, color='#0f16e6', label='Filtered Signal')

        self.ax.set_title("Signal Analysis", fontsize=16)
        self.ax.set_xlabel("Time", fontsize=14)
        self.ax.set_ylabel("Amplitude", fontsize=14)
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

    def update(self, val=None):
        self.plot_signals()

    def update_noise(self, val=None):
        self.noise_g = create_noise(self.t, self.noise_mean_var.get(), self.noise_covariance_var.get())
        self.plot_signals()

    def update_filter(self, val=None):
        self.plot_signals()

    def regenerate_noise(self):
        self.noise_g = create_noise(self.t, self.noise_mean_var.get(), self.noise_covariance_var.get())
        self.plot_signals()

    def random_params(self):
        self.amplitude_var.set(np.random.uniform(0.1, 10.0))
        self.frequency_var.set(np.random.uniform(0.1, 10.0))
        self.phase_var.set(np.random.uniform(0.0, 2 * np.pi))
        self.noise_mean_var.set(np.random.uniform(-1.0, 1.0))
        self.noise_covariance_var.set(np.random.uniform(0.0, 1.0))
        self.regenerate_noise()

    def reset(self):
        self.amplitude_var.set(1.0)
        self.frequency_var.set(1.0)
        self.phase_var.set(0.0)
        self.noise_mean_var.set(0.0)
        self.noise_covariance_var.set(0.1)
        self.cutoff_frequency_var.set(3.0)
        self.show_noise_var.set(True)
        self.regenerate_noise()


if __name__ == "__main__":
    root = tk.Tk()
    app = SignalApp(root)
    root.mainloop()
