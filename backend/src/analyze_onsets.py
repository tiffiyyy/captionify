import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

# get the file path of this script
path = os.path.realpath(__file__)

# get path directory
dir = os.path.dirname(path)

# replace the directory to the sibling folder
dir = dir.replace("src", "audio")

# set the file IO directory to the audio folder
os.chdir(dir)

# get all files in the audio folder
files = os.listdir()

y, sr = librosa.load(files[0])

stft = librosa.stft(y)

# Find maximum amplitude across frequencies for each time step
amplitude_envelope = np.max(np.abs(stft), axis=0)

plt.figure(figsize=(12, 6))

onset_time = librosa.onset.onset_detect(y=y, sr=sr, units='time')

# Plot the waveform
plt.subplot(3, 1, 1)
librosa.display.waveshow(y, sr=sr, alpha=0.5)
plt.title(files[0])

# Plot the peak amplitude envelope
plt.subplot(3, 1, 2)
line, = plt.plot(librosa.frames_to_time(np.arange(len(amplitude_envelope)), sr=sr), amplitude_envelope, label='Max Amplitude')
y_values = line.get_ydata().tolist()
x_values = line.get_xdata().tolist()
print("y values:", len(y_values))
print("x values:", len(x_values))
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Peak Amplitude Envelope')
plt.legend()

# Plot onset times as vertical lines
plt.subplot(3, 1, 3)
librosa.display.waveshow(y, sr=sr, alpha=0.5)
line_collection = plt.vlines(onset_time, -1, 1, color='g', linestyle='dashed', label='Onsets')
# Get the line segments
segments = line_collection.get_segments()

# Extract onset-values from segments
extracted_onset_values = [s[0][0] for s in segments]

print("onsets:", len(extracted_onset_values))
plt.legend()
plt.title('Onset Detection')

plt.tight_layout()

def avg_amplitude(xs, ys, onsets, min_cutoff):
    avgs = []
    i = 0
    j = 0
    k = 0
    sum = 0
    while j < len(ys):
        if i >= len(onsets):
            break
        if k > 0 and xs[j] >= float(onsets[i]):
            if sum / k < min_cutoff:
                avgs.append(min_cutoff)
            else:
                avgs.append(sum / k)
            k = 0
            sum = 0
            i += 1
        k += 1
        sum += ys[j]
        j += 1
    return avgs

averages = avg_amplitude(x_values, y_values, extracted_onset_values, 10)

print("averages:")
for a in averages:
    print(a)
print("averages length:", len(averages))

plt.subplot(4, 1, 4)
plt.plot(extracted_onset_values, averages)
plt.show()