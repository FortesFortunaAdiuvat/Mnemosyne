from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeController:
    def __init__(self):
        pass

    def upload_video_to_youtube(self, video_file, title, description, tags):
        """Uploads a video to YouTube."""
        try:
            # This is a placeholder for actual YouTube upload logic
            # You would typically use the Google API client here
            response = self.fabric_client.run(f"youtube-upload --title='{title}' --description='{description}' --tags='{','.join(tags)}' {video_file}")
            return f"Video uploaded successfully: {response}"
        except Exception as e:
            return f"Error uploading video: {str(e)}"
        
    def get_most_viewed_videos(self, channel_id, max_results=5):
        """Fetches the most viewed videos from a YouTube channel."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/search"
            parameters = {
                "part": "snippet",
                "channelId": channel_id,
                "maxResults": max_results,
                "order": "viewCount"
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            return f"Error fetching most viewed videos: {str(e)}"
        
    def get_most_liked_videos(self, channel_id, max_results=5):
        """Fetches the most liked videos from a YouTube channel."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/search"
            parameters = {
                "part": "snippet",
                "channelId": channel_id,
                "maxResults": max_results,
                "order": "rating"
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            return f"Error fetching most liked videos: {str(e)}"
        
    def get_channel_info(self, channel_id):
        """Fetches information about a YouTube channel."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/channels"
            parameters = {
                "part": "snippet,statistics",
                "id": channel_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])[0] if response.get('items') else None
        except Exception as e:
            return f"Error fetching channel info: {str(e)}"
    
    def get_video_details(self, video_id):
        """Fetches details of a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "snippet,contentDetails,statistics",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])[0] if response.get('items') else None
        except Exception as e:
            return f"Error fetching video details: {str(e)}"
        
    def get_video_comments(self, video_id, max_results=100):
        """Fetches comments from a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/commentThreads"
            parameters = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": max_results
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            return f"Error fetching video comments: {str(e)}"
        
    def get_video_statistics(self, video_id):
        """Fetches statistics of a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "statistics",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])[0]['statistics'] if response.get('items') else None
        except Exception as e:
            return f"Error fetching video statistics: {str(e)}"
        
    def get_video_likes(self, video_id):
        """Fetches the number of likes for a YouTube video."""
        try:
            stats = self.get_video_statistics(video_id)
            return stats.get('likeCount', 0) if stats else 0
        except Exception as e:
            return f"Error fetching video likes: {str(e)}"
        
    def get_video_dislikes(self, video_id):
        """Fetches the number of dislikes for a YouTube video."""
        try:
            stats = self.get_video_statistics(video_id)
            return stats.get('dislikeCount', 0) if stats else 0
        except Exception as e:
            return f"Error fetching video dislikes: {str(e)}"
    
    def get_video_views(self, video_id):
        """Fetches the number of views for a YouTube video."""
        try:
            stats = self.get_video_statistics(video_id)
            return stats.get('viewCount', 0) if stats else 0
        except Exception as e:
            return f"Error fetching video views: {str(e)}"
        
    def get_video_duration(self, video_id):
        """Fetches the duration of a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "contentDetails",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            if response.get('items'):
                duration = response['items'][0]['contentDetails']['duration']
                return duration
            return None
        except Exception as e:
            return f"Error fetching video duration: {str(e)}"
        
    def get_video_published_at(self, video_id):
        """Fetches the published date of a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "snippet",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            if response.get('items'):
                published_at = response['items'][0]['snippet']['publishedAt']
                return published_at
            return None
        except Exception as e:
            return f"Error fetching video published date: {str(e)}"
        
    def get_video_thumbnail(self, video_id):
        """Fetches the thumbnail URL of a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "snippet",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            if response.get('items'):
                thumbnail_url = response['items'][0]['snippet']['thumbnails']['default']['url']
                return thumbnail_url
            return None
        except Exception as e:
            return f"Error fetching video thumbnail: {str(e)}"
        
    def get_video_tags(self, video_id):
        """Fetches the tags of a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "snippet",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            if response.get('items'):
                tags = response['items'][0]['snippet'].get('tags', [])
                return tags
            return []
        except Exception as e:
            return f"Error fetching video tags: {str(e)}"
        
    def get_video_categories(self):
        """Fetches the categories of YouTube videos."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videoCategories"
            parameters = {
                "part": "snippet",
                "regionCode": "US"  # Change as needed
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            return f"Error fetching video categories: {str(e)}"
        
    def get_video_related_videos(self, video_id, max_results=5):
        """Fetches related videos for a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/search"
            parameters = {
                "part": "snippet",
                "relatedToVideoId": video_id,
                "type": "video",
                "maxResults": max_results
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            return f"Error fetching related videos: {str(e)}"
        
    def get_video_playlists(self, video_id):
        """Fetches playlists that a YouTube video belongs to."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/playlists"
            parameters = {
                "part": "snippet",
                "videoId": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            return f"Error fetching video playlists: {str(e)}"
        
    def get_video_live_status(self, video_id):
        """Checks if a YouTube video is live."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "liveStreamingDetails",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            if response.get('items'):
                live_details = response['items'][0].get('liveStreamingDetails', {})
                return 'live' in live_details
            return False
        except Exception as e:
            return f"Error checking live status: {str(e)}"
        
    def get_video_comments_count(self, video_id):
        """Fetches the number of comments on a YouTube video."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/videos"
            parameters = {
                "part": "statistics",
                "id": video_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            if response.get('items'):
                stats = response['items'][0]['statistics']
                return int(stats.get('commentCount', 0))
            return 0
        except Exception as e:
            return f"Error fetching video comments count: {str(e)}"
        
    def get_video_comments_replies(self, comment_id):
        """Fetches replies to a YouTube comment."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/comments"
            parameters = {
                "part": "snippet",
                "parentId": comment_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            return response.get('items', [])
        except Exception as e:
            return f"Error fetching comment replies: {str(e)}"
        
    def get_video_comments_replies_count(self, comment_id):
        """Fetches the number of replies to a YouTube comment."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            return len(replies)
        except Exception as e:
            return f"Error fetching comment replies count: {str(e)}"
        
    def get_video_comments_likes(self, comment_id):
        """Fetches the number of likes on a YouTube comment."""
        try:
            endpoint = "https://www.googleapis.com/youtube/v3/comments"
            parameters = {
                "part": "snippet",
                "id": comment_id
            }
            request = self.fabric_client.create_request(endpoint, params=parameters)
            response = request.execute()
            if response.get('items'):
                snippet = response['items'][0]['snippet']
                return int(snippet.get('likeCount', 0))
            return 0
        except Exception as e:
            return f"Error fetching comment likes: {str(e)}"
        
    def get_video_comments_replies_likes(self, comment_id):
        """Fetches the number of likes on replies to a YouTube comment."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            total_likes = 0
            for reply in replies:
                total_likes += self.get_video_comments_likes(reply['id'])
            return total_likes
        except Exception as e:
            return f"Error fetching comment replies likes: {str(e)}"
        
    def get_video_comments_replies_count_and_likes(self, comment_id):
        """Fetches the number of replies and likes on a YouTube comment."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            replies_count = len(replies)
            total_likes = 0
            for reply in replies:
                total_likes += self.get_video_comments_likes(reply['id'])
            return {
                "replies_count": replies_count,
                "total_likes": total_likes
            }
        except Exception as e:
            return f"Error fetching comment replies count and likes: {str(e)}"
    
    def get_video_comments_replies_count_and_likes_by_user(self, comment_id, user_id):
        """Fetches the number of replies and likes on a YouTube comment by a specific user."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            user_replies_count = 0
            user_likes_count = 0
            for reply in replies:
                if reply['snippet']['authorChannelId'] == user_id:
                    user_replies_count += 1
                    user_likes_count += self.get_video_comments_likes(reply['id'])
            return {
                "user_replies_count": user_replies_count,
                "user_likes_count": user_likes_count
            }
        except Exception as e:
            return f"Error fetching comment replies count and likes by user: {str(e)}"
        
    def get_video_comments_replies_count_and_likes_by_user_and_date(self, comment_id, user_id, start_date, end_date):
        """Fetches the number of replies and likes on a YouTube comment by a specific user within a date range."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            user_replies_count = 0
            user_likes_count = 0
            for reply in replies:
                if (reply['snippet']['authorChannelId'] == user_id and 
                    start_date <= reply['snippet']['publishedAt'] <= end_date):
                    user_replies_count += 1
                    user_likes_count += self.get_video_comments_likes(reply['id'])
            return {
                "user_replies_count": user_replies_count,
                "user_likes_count": user_likes_count
            }
        except Exception as e:
            return f"Error fetching comment replies count and likes by user and date: {str(e)}"
        
    def get_video_comments_replies_count_and_likes_by_user_and_date_and_content(self, comment_id, user_id, start_date, end_date, content):
        """Fetches the number of replies and likes on a YouTube comment by a specific user within a date range and containing specific content."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            user_replies_count = 0
            user_likes_count = 0
            for reply in replies:
                if (reply['snippet']['authorChannelId'] == user_id and 
                    start_date <= reply['snippet']['publishedAt'] <= end_date and 
                    content.lower() in reply['snippet']['textDisplay'].lower()):
                    user_replies_count += 1
                    user_likes_count += self.get_video_comments_likes(reply['id'])
            return {
                "user_replies_count": user_replies_count,
                "user_likes_count": user_likes_count
            }
        except Exception as e:
            return f"Error fetching comment replies count and likes by user, date, and content: {str(e)}"
        
    def get_video_comments_replies_count_and_likes_by_user_and_date_and_content_and_replies(self, comment_id, user_id, start_date, end_date, content):
        """Fetches the number of replies and likes on a YouTube comment by a specific user within a date range, containing specific content, and also counts replies."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            user_replies_count = 0
            user_likes_count = 0
            for reply in replies:
                if (reply['snippet']['authorChannelId'] == user_id and 
                    start_date <= reply['snippet']['publishedAt'] <= end_date and 
                    content.lower() in reply['snippet']['textDisplay'].lower()):
                    user_replies_count += 1
                    user_likes_count += self.get_video_comments_likes(reply['id'])
                    # Count replies to this reply
                    reply_replies = self.get_video_comments_replies(reply['id'])
                    user_replies_count += len(reply_replies)
            return {
                "user_replies_count": user_replies_count,
                "user_likes_count": user_likes_count
            }
        except Exception as e:
            return f"Error fetching comment replies count and likes by user, date, content, and replies: {str(e)}"
        
    def get_video_comments_replies_count_and_likes_by_user_and_date_and_content_and_replies_and_replies_likes(self, comment_id, user_id, start_date, end_date, content):
        """Fetches the number of replies and likes on a YouTube comment by a specific user within a date range, containing specific content, counting replies, and also counting likes on those replies."""
        try:
            replies = self.get_video_comments_replies(comment_id)
            user_replies_count = 0
            user_likes_count = 0
            for reply in replies:
                if (reply['snippet']['authorChannelId'] == user_id and 
                    start_date <= reply['snippet']['publishedAt'] <= end_date and 
                    content.lower() in reply['snippet']['textDisplay'].lower()):
                    user_replies_count += 1
                    user_likes_count += self.get_video_comments_likes(reply['id'])
                    # Count replies to this reply and their likes
                    reply_replies = self.get_video_comments_replies(reply['id'])
                    user_replies_count += len(reply_replies)
                    for r_reply in reply_replies:
                        user_likes_count += self.get_video_comments_likes(r_reply['id'])
            return {
                "user_replies_count": user_replies_count,
                "user_likes_count": user_likes_count
            }
        except Exception as e:
            return f"Error fetching comment replies count and likes by user, date, content, replies, and replies likes: {str(e)}"
        
