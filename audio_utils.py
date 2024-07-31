import wave
import pyaudio
import aiofile
import nest_asyncio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

def record_audio(output_filename, silence_threshold=1000, chunk_size=1024, rate=16000, silence_duration=3):
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print("Recording...")
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk_size,
                    input=True)
    frames = []  # Initialize array to store frames

    silent_chunks = 0
    while True:
        data = stream.read(chunk_size)
        frames.append(data)

        # Convert byte data to array of integers
        audio_data = wave.struct.unpack("%dh" % (len(data) / 2), data)
        max_amplitude = max(audio_data)

        # Check for silence
        if max_amplitude < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0

        # If silence has lasted for the specified duration, stop recording
        if silent_chunks > (rate / chunk_size * silence_duration):
            break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Recording complete")

class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream):
        super().__init__(transcript_result_stream)
        self.transcript = ""

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                self.transcript += alt.transcript
                print(alt.transcript)

async def real_time_transcribe(audio_filename):
    client = TranscribeStreamingClient(region="us-west-2")

    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )

    async def write_chunks():
        async with aiofile.AIOFile(audio_filename, 'rb') as afp:
            reader = aiofile.Reader(afp, chunk_size=1024 * 16)
            async for chunk in reader:
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
        await stream.input_stream.end_stream()

    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())
    return handler.transcript