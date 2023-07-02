import os
import subprocess
from moviepy.editor import *
from pydub import AudioSegment

def calculate_n(image_folder, name):
    # Get the largest value of n based on image files
    image_files = os.listdir(image_folder)
    print(image_files)
    n = max([int(file.split(name)[1].split('.')[0]) for file in image_files])
    return n

def concatenate_audio_image(audio_folder, image_folder, output_folder):
    # Calculate n
    n = calculate_n(image_folder, 'image')

    inputs = []

    # Iterate over audio and image files
    for i in range(1, n+1):
        # Input filenames
        image_filename = os.path.join(image_folder, f'image{i}.png')
        audio_filename = os.path.join(audio_folder, f'narration{i}.wav')

        # Append input filenames to the list
        inputs.append(ffmpeg.input(image_filename))
        inputs.append(ffmpeg.input(audio_filename))
    # Concatenate all input files
    print(inputs)
    joined = ffmpeg.concat(*inputs, v=1, a=1).output(f'{output_folder}/output.mp4', vcodec='libx264', acodec='aac', pix_fmt='yuv420p', r=25).run()

# Provide the folder paths
current_path = os.getcwd()
image_path = os.path.join(current_path, "images")
audio_path = os.path.join(current_path, "audio")
n = calculate_n(image_path, 'story')
print(n)
audio_folder = os.path.join(audio_path, f'story{n}')
image_folder = os.path.join(image_path, f'story{n}')
print(audio_folder, image_folder)
output_folder = os.path.join(current_path, 'output')

num_files = len(os.listdir(audio_folder))

# Let's store each individual clip in a list
clips = []

for i in range(1, num_files + 1):
    # Create the filepaths for the audio and image files
    audio_path = f"{audio_folder}/narration{i}.wav"
    image_path = f"{image_folder}/image{i}.png"
    
    # Get the duration of the audio file in seconds
    audio = AudioSegment.from_wav(audio_path)
    duration = len(audio) / 1000  # pydub calculates in millisec

    # Create a moviepy clip for the image, the duration of the image clip should be the same as the audio file's duration
    img_clip = ImageClip(image_path, duration=duration)

    # Set the audio of the image clip to be the audio file
    img_clip = img_clip.set_audio(AudioFileClip(audio_path))

    # Append this clip to our list of clips
    clips.append(img_clip)

# Concatenate all clips together
final_clip = concatenate_videoclips(clips)

# Write the result to a file
final_clip.write_videofile(os.path.join(output_folder, "final_video.mp4"), codec='libx264', fps=24)
