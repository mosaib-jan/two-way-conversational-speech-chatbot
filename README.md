# Two Way speech based conversational chatbot

## Overview
Appointment Bot is an interactive bot application that uses AWS services for speech-to-text, text-to-speech, and conversational AI. The application includes a GUI built with Tkinter and provides real-time transcription and responses.

## Features
- Real-time audio recording and transcription
- Interaction with AWS Bedrock for conversational AI
- AWS Polly for text-to-speech synthesis
- GUI for user interaction

## Setup

### Prerequisites
- Python 3.x
- AWS account with access to Bedrock and Polly services

### Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd appointment-bot
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set environment variables:
    Create a `.env` file in the project root with the following content:
    ```env
    BEDROCK_REGION=us-east-1
    POLLY_REGION=us-east-1
    MODEL_ID=your-model-id
    ```
    Load the environment variables:
    ```bash
    export $(cat .env | xargs)  # On Windows, set the variables manually
    ```

5. Run the application:
    ```bash
    python main.py
    ```

## Usage
- Enter your first message in the provided text box and click "Start Conversation".
- The bot will respond with synthesized speech.
- The conversation will continue with real-time audio recording and transcription.
- To end the conversation, click "End Conversation".

## File Details

### `main.py`
- Entry point of the application.
- Initializes the GUI and starts the conversation process.

### `audio_utils.py`
- Contains functions for audio recording and transcription using AWS Transcribe.
  - `record_audio(output_filename, silence_threshold, chunk_size, rate, silence_duration)`: Records audio and detects silence to stop recording.
  - `real_time_transcribe(audio_filename)`: Performs real-time transcription on recorded audio.

### `aws_utils.py`
- Contains functions for interacting with AWS Bedrock and Polly.
  - `invoke_model_with_stream(conversation_history)`: Invokes the Bedrock model with the conversation history and streams the response.
  - `synthesize_speech(text)`: Uses AWS Polly to convert text to speech and play the audio.

### `gui.py`
- Sets up the graphical user interface using Tkinter.
  - `start_conversation(user_input, canvas, circle)`: Starts the conversation by handling user input, bot response, and text-to-speech.
  - `end_conversation()`: Ends the conversation and exits the application.

## Important Notes
- Ensure that you have the necessary AWS credentials configured. You can set them up using the AWS CLI or environment variables.
- Make sure to handle the sensitive information securely and never commit your `.env` file to version control.
- If you need to modify any AWS-related configurations, update the `aws_utils.py` file accordingly.

## Requirements
List of dependencies:
- aiofile
- amazon-transcribe
- boto3
- nest-asyncio
- playsound
- pyaudio
- tk

## License
This project is licensed under the MIT License.
