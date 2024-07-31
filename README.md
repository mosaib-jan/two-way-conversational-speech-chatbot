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

## License
This project is licensed under the MIT License.
