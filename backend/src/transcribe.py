import whisper
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

# print filenames
print(files)

# use the base Whisper model
model = whisper.load_model("base")

# transcribe the first audio file in the list
result = model.transcribe(files[0], fp16 = False)

# print the result
print(result["text"])
"""