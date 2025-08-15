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
    
    def generate_video_script(self, prompt, video_length=60):
        """Generates a video script using Ollama."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"{prompt}" }]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating video script: {str(e)}"
        
    def generate_video_from_script(self, script, video_length=60):
        """Generates a video from a script using Ollama."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Create a video from this script: {script}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating video: {str(e)}"
        
    def generate_video_thumbnail(self, video_id):
        """Generates a thumbnail for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a thumbnail for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating thumbnail: {str(e)}"
        
    def generate_video_title(self, video_id):
        """Generates a title for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a title for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating title: {str(e)}"
        
    def generate_video_description(self, video_id):
        """Generates a description for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a description for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating description: {str(e)}"
        
    def generate_video_tags(self, video_id):
        """Generates tags for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate tags for video ID: {video_id}"}]
            )
            return response['message']['content'].split(',')
        except Exception as e:
            return f"Error generating tags: {str(e)}"
        
    def generate_video_keywords(self, video_id):
        """Generates keywords for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate keywords for video ID: {video_id}"}]
            )
            return response['message']['content'].split(',')
        except Exception as e:
            return f"Error generating keywords: {str(e)}"
        
    def generate_video_caption(self, video_id):
        """Generates a caption for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a caption for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating caption: {str(e)}"
        
    def generate_video_transcript(self, video_id):
        """Generates a transcript for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a transcript for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating transcript: {str(e)}"
        
    def generate_video_keywords_and_tags(self, video_id):
        """Generates keywords and tags for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate keywords and tags for video ID: {video_id}"}]
            )
            content = response['message']['content']
            keywords, tags = content.split('|')
            return {
                "keywords": keywords.split(','),
                "tags": tags.split(',')
            }
        except Exception as e:
            return f"Error generating keywords and tags: {str(e)}"
        
    def generate_x_post(self, script, video_id):
        """Generates a post for X (formerly Twitter) based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a post for X based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating X post: {str(e)}"
        
    def generate_youtube_post(self, script, video_id):
        """Generates a post for YouTube based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a YouTube post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating YouTube post: {str(e)}"
        
    def generate_facebook_post(self, script, video_id):
        """Generates a post for Facebook based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a Facebook post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating Facebook post: {str(e)}"
        
    def generate_instagram_post(self, script, video_id):
        """Generates a post for Instagram based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate an Instagram post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating Instagram post: {str(e)}"
        
    def generate_linkedin_post(self, script, video_id):
        """Generates a post for LinkedIn based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a LinkedIn post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating LinkedIn post: {str(e)}"
        
    def generate_tiktok_post(self, script, video_id):
        """Generates a post for TikTok based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a TikTok post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating TikTok post: {str(e)}"
        
    def generate_snapchat_post(self, script, video_id):
        """Generates a post for Snapchat based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a Snapchat post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating Snapchat post: {str(e)}"
        
    def generate_pinterest_post(self, script, video_id):
        """Generates a post for Pinterest based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a Pinterest post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating Pinterest post: {str(e)}"
        
    def generate_reddit_post(self, script, video_id):
        """Generates a post for Reddit based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a Reddit post based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating Reddit post: {str(e)}"
        
    def generate_website_blog_post(self, script, video_id):
        """Generates a blog post for a website based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a blog post for a website based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating website blog post: {str(e)}"
        
    def generate_email_content(self, script, video_id):
        """Generates email content based on a video script."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate email content based on this script: {script} for video ID: {video_id}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating email content: {str(e)}"
        
    def generate_youtube_comment(self, video_id, comment_text):
        """Generates a comment for a YouTube video."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a comment for video ID: {video_id} with text: {comment_text}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating YouTube comment: {str(e)}"
        
    def generate_youtube_reply(self, comment_id, reply_text):
        """Generates a reply to a YouTube comment."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a reply to comment ID: {comment_id} with text: {reply_text}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating YouTube reply: {str(e)}"
        
    def generate_x_comment(self, post_id, comment_text):
        """Generates a comment for a post on X (formerly Twitter)."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a comment for post ID: {post_id} with text: {comment_text}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating X comment: {str(e)}"
        
    def generate_x_reply(self, comment_id, reply_text):
        """Generates a reply to a comment on X (formerly Twitter)."""
        try:
            response = self.ollama_client.chat(
                model="mistral",
                messages=[{"role": "user", "content": f"Generate a reply to comment ID: {comment_id} with text: {reply_text}"}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating X reply: {str(e)}"
        


# Example usage
if __name__ == "__main__":
    mnemosyne = Mnemosyne()
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    summary = mnemosyne.summarize_youtube_video(video_url)
    print(summary)