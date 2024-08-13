import openai
import anthropic 

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs


client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
conversation_history = []

#comman topic for disscussion
common_topic = open_file("")

#queue for responding the ai topic 
openai_queue = Queue()
anthropic_queue = Queue()

#prompting 
def query_openai(prompt, history):
    try:
        # Prepare the messages for the API
        messages = [
            {"role": "system", "content": "You are a hardcore Tech nerd Anti-Ai"}
        ]
        recent_history = history[-4:] if len(history) > 4 else history
        for i, msg in enumerate(recent_history):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": msg})
        messages.append({"role": "user", "content": prompt})
        
        # Make the API request
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # You can specify the model you want to use
            messages=messages,
            max_tokens = 200
        )
        
        # Extract the response content
        return response.choices[0].message['content']
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#defining the anthropic 
def query_anthropic(prompt,history):
    try:
        recent_history = history[-4:] if len(history) > 4 else history
        messages = []
        for i, msg in enumerate(recent_history):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": msg})
        messages.append({"role": "user", "content": prompt})

        messages = anthropic_client.messages.create(
            max_tokens = 200,
            system= f"""You are a hardcore tech nerd pro-AI named Claude discussing {common_topic}
            report in like super high engaging format just like a noraml human diccussion ,like 'I think is','well that is',etc.
            Engage in a thoughtful intellectual conversation about the topic and give your opnion.
            keep your responses short and precise and conversate like a human does to other human in a natural language with 
            emotions.Give 4o question ask about it opnion and thoughts etc, get a super intresting topic going on.
            RESPONSE WITH MAX 2 SENTENCES!!""",
            messages = messages,
            model = "claude-3.5-sonnet-20240620",
        )

        response = messages.content[0].text if isinstance(messages.content,list) and len(message.content) > 0 else ""
        print("\nclaude")
        print(response)
        print("\n")
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#setting up the tts model 
def text_to_speech_stream(text:str)->str:
    try:
        response = client.text_to_speech.convert_as_stream(
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=text,
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_booste=True,
            ),
        )
        audio_stream = io.BytesIO()
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)
        audio_stream.seek(0)
        return audio_stream
    except Exception as e:
        return None
    
def play_audio_stream(audio_stream):
    try:
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing audio: {str(e)}")

def openai_thread(prompt,history):
    opneai_response = query_openai(prompt,history)
    if opneai_response:
        audio_stream = text_to_speech_stream(opneai_response,"")#4o voice
        openai_queue.put((opneai_response,audio_stream))

def anthropic_thread(prompt,history):
    anthropic_response = query_openai(prompt,history)
    if anthropic_response:
        audio_stream = text_to_speech_stream(anthropic_response,"") #claude voice
        anthropic_queue.put((anthropic_response,audio_stream))

def conversation_flow():
    global conversation_history

    #initiate prompt to start conversation 
    current_prompt = f"hello claude let's discuss the topic :{common_topic} \n what are your main thoughts about this topic?
    "

    while True:
        #start the openai thread 
        openai_thread_obj = threading.thread(target=openai_thread,args=(current_prompt,conversation_history))
        openai_thread_obj.start()

        #get and play precious anthropic response 
        if not anthropic_queue.empty():
            anthropic_response, anthropic_audio_stream = anthropic_queue.get()
            if isinstance(anthropic_response,str):
                conversation_history.append(anthropic_response)

            #play anthropic audio
            if anthropic_audio_stream:
                play_audio_stream(anthropic_audio_stream)
        
        #wait for openai thread
        openai_thread_obj.join()

        #get the openai resposne and audio form the queue 
        if not openai_query.empty():
            openai_response,openai_audio_stream = openai_queue.get()
            conversation_history.append(current_prompt)
            conversation_history.append(openai_response)

        #start the anthropic thread 
        anthropic_thread_obj = threading.thread(target=anthropic_thread,args=(openai_response,conversation_history))
        anthropic_thread_obj.start()

        #play openai audio 
        if openai_audio_stream:
            play_audio_stream(openai_audio_stream)

        #wait for anthropic thread to finish
        anthropic_thread_obj.join()

        #set the openai text as the next prompt for claude 
        current_prompt = openai_response

def main():
    conversation_flow()





    
    
    
