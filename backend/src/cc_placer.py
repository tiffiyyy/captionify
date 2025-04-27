import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

import transcribe
import analyze_onsets

video_input_path = "/audio/file_example_MP4_480_1_5MG"
output_video_path ="/finalVid/"

avgs = analyze_onsets.getAverages
ons = analyze_onsets.getOnsetVals

video = VideoFileClip(video_input_path)
audio_path = "/audio/test.wav"



result = transcribe.getResult("text") 
segments = result["segments"]

caption_clips = []

for idx, segment in enumerate(segments):
    start = segment['start']
    end = segment['end']
    duration = end - start
    text = segment['text']

    # Check the corresponding onset value
    onset_value = ons[idx] if idx < len(ons) else 0  # fallback if ons shorter than segments

    if onset_value > 75:
        font_size = 40
    else:
        font_size = 25

#Font characterist
    caption = TextClip(
        text,
        fontsize= font_size,
        color='white',
        stroke_color='black',
        stroke_width=2,
        size=(video.w * 0.8, None),
        method='caption'  # auto-wrap text nicely
    ).set_position(('center', 'bottom')).set_start(start).set_duration(duration)
    caption_clips.append(caption)


final = CompositeVideoClip([video] + caption_clips)

final.write_videofile(
    output_video_path,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
    fps=video.fps
)

if os.path.exists(audio_path):
    os.remove(audio_path)

print(f"✅ Done! Output saved to {output_video_path}")
