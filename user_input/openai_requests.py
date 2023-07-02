import os
import openai
import re

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_storyline(age, interests, topic):
    # Prepare the list of messages. The role can be 'system', 'user', or 'assistant'.
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"""
        Please create a storyline to explain me the {topic}. The storyline should be separated in the sections. Each section should contain 2 things: the description of an image and the script of the story. The image descriptions will be put into DALL-E 2. Make sure the script always relates back to the topic being explained. I am {age} and my interests are {interests}. Please don't feel like you need you use my interests to create the story. Just do whatever will explain the story in the clearest way.

        The format of the storyline should be as such:

        Section 1: (topic)
        Image: (Description of the image)
        Narration: (Script)

        Section 2: (Title)
        Image: (Description of the image)
        Narration: (Script)

        Section n: (Title)
        Image: (Description of the image)
        Narration: (Script)

        """,
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    storyline_text = response["choices"][0]["message"]["content"]

    # Now let's parse the storyline text into the required format
    sections = re.split(
        r"\n(?=Section \d+:)", storyline_text
    )  # Split sections at 'Section n:'

    storyline = []  # This will hold the parsed storyline

    for sec in sections:
        # Use regular expressions to parse the section
        title_match = re.search(r"Section \d+: (.+)", sec)
        image_match = re.search(r"Image: (.+)", sec)
        narration_match = re.search(r"Narration: (.+)", sec)

        # Check that each component was found in the section
        if title_match and image_match and narration_match:
            title = title_match.group(1).strip()
            image = image_match.group(1).strip()
            narration = narration_match.group(1).strip()

            # Append this section to the storyline list
            storyline.append({"Title": title, "Image": image, "Narration": narration})

    return storyline
