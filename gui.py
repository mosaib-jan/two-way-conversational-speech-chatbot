import threading
import asyncio
from tkinter import END
from audio_utils import record_audio, real_time_transcribe
from aws_utils import invoke_model_with_stream, synthesize_speech

def start_conversation(user_input, canvas, circle):
    conversation_history = []

    first_input = user_input.get("1.0", END).strip()
    conversation_history.append({
        "role": "user",
        "content": [{"type": "text", "text": first_input}]
    })

    def bot_response():
        while True:
            bedrock_output = invoke_model_with_stream(conversation_history)
            if bedrock_output is None:
                break

            conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": bedrock_output}]
            })

            canvas.itemconfig(circle, fill='green')
            synthesize_speech(bedrock_output)
            canvas.itemconfig(circle, fill='red')

            audio_filename = "recorded_audio.wav"
            record_audio(audio_filename)
            transcript_text = asyncio.run(real_time_transcribe(audio_filename))

            if "ok goodbye" in transcript_text.lower():
                print("Conversation ended by user.")
                break

            conversation_history.append({
                "role": "user",
                "content": [{"type": "text", "text": transcript_text}]
            })

    threading.Thread(target=bot_response).start()

def end_conversation():
    import sys
    sys.exit()