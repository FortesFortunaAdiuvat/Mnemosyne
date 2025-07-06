import ollama
import fabric
from youtube_transcript_api import YouTubeTranscriptApi

class Mnemosyne:
    def __init__(self):
        self.fabric_client = fabric.Client()
        self.ollama_client = ollama.Client()

    def get_video_transcript(self, video_id):
        """Fetches the transcript of a YouTube video given its ID."""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([entry['text'] for entry in transcript])
        except Exception as e:
            return f"Error fetching transcript: {str(e)}"

    def summarize_text(self, text):
        """Summarizes the text using Ollama."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Summarize this: {text}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error summarizing text: {str(e)}"

    def summarize_youtube_video(self, video_url):
        """Extracts transcript and summarizes a YouTube video."""
        video_id = video_url.split("v=")[-1]
        transcript = self.get_video_transcript(video_id)
        if transcript.startswith("Error"):
            return transcript
        return self.summarize_text(transcript)

# Example usage
if __name__ == "__main__":
    mnemosyne = Mnemosyne()
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    summary = mnemosyne.summarize_youtube_video(video_url)
    print(summary)