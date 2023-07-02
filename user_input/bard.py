import google.generativeai as palm
import base64
import json
import os

storyline = ""
palm_api_key = os.getenv("PALM_API_KEY")

palm.configure(api_key=palm_api_key)
# Configure the model
model = "models/text-bison-001"
temperature = 0.7
candidate_count = 1
top_k = 40  # @param {isTemplate: true}
top_p = 0.95  # @param {isTemplate: true}
max_output_tokens = 1024  # @param {isTemplate: true}
text_b64 = ""  # @param {isTemplate: true}
stop_sequences_b64 = "W10="  # @param {isTemplate: true}
safety_settings_b64 = "W3siY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX0RFUk9HQVRPUlkiLCJ0aHJlc2hvbGQiOjF9LHsiY2F0ZWdvcnkiOiJIQVJNX0NBVEVHT1JZX1RPWElDSVRZIiwidGhyZXNob2xkIjoxfSx7ImNhdGVnb3J5IjoiSEFSTV9DQVRFR09SWV9WSU9MRU5DRSIsInRocmVzaG9sZCI6Mn0seyJjYXRlZ29yeSI6IkhBUk1fQ0FURUdPUllfU0VYVUFMIiwidGhyZXNob2xkIjoyfSx7ImNhdGVnb3J5IjoiSEFSTV9DQVRFR09SWV9NRURJQ0FMIiwidGhyZXNob2xkIjoyfSx7ImNhdGVnb3J5IjoiSEFSTV9DQVRFR09SWV9EQU5HRVJPVVMiLCJ0aHJlc2hvbGQiOjJ9XQ=="  # @param {isTemplate: true}

# Convert the prompt text param from a bae64 string to a string.
text = base64.b64decode(text_b64).decode("utf-8")

# Convert the stop_sequences and safety_settings params from base64 strings to lists.
stop_sequences = json.loads(base64.b64decode(stop_sequences_b64).decode("utf-8"))
safety_settings = json.loads(base64.b64decode(safety_settings_b64).decode("utf-8"))

defaults = {
    "model": model,
    "temperature": temperature,
    "candidate_count": candidate_count,
    "top_k": top_k,
    "top_p": top_p,
    "max_output_tokens": max_output_tokens,
    "stop_sequences": stop_sequences,
    "safety_settings": safety_settings,
}


def bard(text):
    response = palm.generate_text(**defaults, prompt=text)
    return response
