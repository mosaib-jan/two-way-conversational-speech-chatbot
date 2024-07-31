import os
import tempfile
import boto3
import json
from botocore.exceptions import ClientError
from playsound import playsound

# Initialize clients with environment variables
bedrock_client = boto3.client("bedrock-runtime", region_name=os.getenv("BEDROCK_REGION", "us-east-1"))
polly_client = boto3.client('polly', region_name=os.getenv("POLLY_REGION", "us-east-1"))

def invoke_model_with_stream(conversation_history):
    model_id = os.getenv("MODEL_ID", "your-model-id")

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": conversation_history,
    }

    request = json.dumps(native_request)

    try:
        streaming_response = bedrock_client.invoke_model_with_response_stream(
            modelId=model_id, body=request
        )

        response_text = ""
        for event in streaming_response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if chunk["type"] == "content_block_delta":
                response_text += chunk["delta"].get("text", "")
                print(chunk["delta"].get("text", ""), end="")
        
        return response_text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return None

def synthesize_speech(text):
    try:
        response = polly_client.synthesize_speech(VoiceId='Ruth', OutputFormat='mp3', Text=text, Engine='neural')
        if "AudioStream" in response:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(response["AudioStream"].read())
                tmp_file_path = tmp_file.name

            playsound(tmp_file_path)
        else:
            print("Could not stream audio")
    except (ClientError, Exception) as e:
        print(f"ERROR: Polly synthesis failed. Reason: {e}")