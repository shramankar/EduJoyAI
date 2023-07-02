import os 
import re 
import openai
from dotenv import load_dotenv
import requests 
from common import next_story_directory
story = [{'image': 'A black hole, depicted as a dark sphere with a bright ring of light around it.',
  'narration': "A black hole is a place in space where gravity pulls so much that even light can not get out. The gravity is so strong because matter has been squeezed into a tiny space. This can happen when a star is dying. Because no light can get out, people can't see black holes. They are invisible. Space telescopes with special tools can help find black holes."},
 {'image': 'A star, collapsing under its own gravity',
  'narration': 'Stars are like big balls of gas. They are held together by gravity. When a star dies, it starts to collapse. If the star is big enough, it will collapse so much that it forms a black hole.'}]

current_directory = os.getcwd() 
IMAGE_DIRECTORY = current_directory + '\images'
CUR_STORY_DIR, _ = next_story_directory(base_dir = IMAGE_DIRECTORY, 
                                     name = 'story')
load_dotenv()
openai.api_key = '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'

for idx, script in enumerate(story, start=1):
    image = script["image"]
    response = openai.Image.create(
        prompt=image,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    r = requests.get(image_url)
    if r.status_code == 200:
        with open(os.path.join(CUR_STORY_DIR, f"image{idx}.png"), "wb") as f:
            f.write(r.content) # Write the contents (bytes) to a file
            print(f"image{idx}.png created")


