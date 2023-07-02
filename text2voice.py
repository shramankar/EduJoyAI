import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from common import next_story_directory
load_dotenv() 
print(os.getenv('SPEECH_KEY'))
story = [{'image': 'A black hole, depicted as a dark sphere with a bright ring of light around it.',
  'narration': "A black hole is a place in space where gravity pulls so much that even light can not get out. The gravity is so strong because matter has been squeezed into a tiny space. This can happen when a star is dying. Because no light can get out, people can't see black holes. They are invisible. Space telescopes with special tools can help find black holes."},
 {'image': 'A star, collapsing under its own gravity',
  'narration': 'Stars are like big balls of gas. They are held together by gravity. When a star dies, it starts to collapse. If the star is big enough, it will collapse so much that it forms a black hole.'}]
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
print(os.environ.get('SPEECH_KEY'), os.environ.get('SPEECH_REGION'))
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
current_directory = os.getcwd() 
AUDIO_DIR = current_directory + '\\' + 'audio'
CUR_AUDIO_DIR, _= next_story_directory(base_dir = AUDIO_DIR, 
                                     name = 'story')
                
for idx, script in enumerate(story, start=1):
    narration = script["narration"]
    print(CUR_AUDIO_DIR, f"narration{idx}.wav")
    filename = os.path.join(CUR_AUDIO_DIR, f"narration{idx}.wav")
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    speech_config.speech_synthesis_voice_name='en-US-AriaNeural	' # The language of the voice that speaks (change this)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(narration).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(narration))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")