import praw
from typing import List, Dict
import os
from datetime import datetime

class RedditCollector:
    def __init__(self, client_id: str = None, client_secret: str = None, user_agent: str = None):
        self.client_id = client_id or os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = user_agent or os.getenv("REDDIT_USER_AGENT", "NOESIS_Bot/1.0")
        
        if not (self.client_id and self.client_secret and self.user_agent):
            print("Reddit API credentials (client_id, client_secret, user_agent) are required for real data. Using mock data.")
            self.reddit = None
        else:
            try:
                self.reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    user_agent=self.user_agent
                )
            except Exception as e:
                print(f"Error initializing Reddit client: {e}")
                self.reddit = None

    def collect(self) -> List[Dict]:
        """Collect recent Reddit posts about protests and civil unrest"""
        posts = []
        
        try:
            # Check if API credentials are available
            if not self.reddit:
                print("Reddit API credentials not configured, using mock data")
                return self._get_mock_data()
            
            # Search for protest-related keywords
            keywords = ["protest", "riot", "strike", "demonstration", "civil unrest", "tear gas"]
            
            for keyword in keywords:
                try:
                    # Search in relevant subreddits
                    subreddits = ["news", "worldnews", "politics", "protests"]
                    
                    for subreddit in subreddits:
                        try:
                            # Search for posts
                            search_results = self.reddit.subreddit(subreddit).search(
                                keyword, 
                                sort='new', 
                                time_filter='day',
                                limit=10
                            )
                            
                            for submission in search_results:
                                try:
                                    # Sanitize text content
                                    content = self._sanitize_text(submission.title + " " + (submission.selftext or ""))
                                    if not content:
                                        continue
                                    
                                    post = {
                                        "platform": "reddit",
                                        "content": content,
                                        "author": str(submission.author) if submission.author else "unknown",
                                        "timestamp": datetime.fromtimestamp(submission.created_utc).isoformat(),
                                        "location_raw": "",
                                        "link": f"https://reddit.com{submission.permalink}",
                                        "extra": {
                                            "subreddit": subreddit,
                                            "score": submission.score,
                                            "num_comments": submission.num_comments
                                        }
                                    }
                                    
                                    posts.append(post)
                                    print(f"Collected Reddit post: {content[:100]}...")
                                    
                                except Exception as e:
                                    print(f"Error processing Reddit submission: {e}")
                                    continue
                                    
                        except Exception as e:
                            print(f"Error searching subreddit {subreddit}: {e}")
                            continue
                            
                except Exception as e:
                    print(f"Error searching for keyword {keyword}: {e}")
                    continue
            
            print(f"Successfully collected {len(posts)} Reddit posts")
            
        except Exception as e:
            print(f"Error collecting Reddit data: {e}")
            print("Using mock data instead")
            posts = self._get_mock_data()
        
        return posts

    def _sanitize_text(self, text: str) -> str:
        """Sanitize text to prevent encoding issues"""
        if not text:
            return ""
        
        try:
            # Handle bytes
            if isinstance(text, bytes):
                text = text.decode('utf-8', errors='ignore')
            
            # Handle None or non-string types
            if not isinstance(text, str):
                text = str(text)
            
            # Remove problematic characters
            import re
            # Remove control characters and non-printable characters
            text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
            # Remove characters that can't be encoded properly
            text = re.sub(r'[^\x20-\x7E\u00A0-\uFFFF]', ' ', text)
            # Replace multiple spaces and newlines
            text = re.sub(r'\s+', ' ', text)
            # Remove any remaining problematic characters
            text = ''.join(char for char in text if ord(char) < 65536)
            
            return text.strip()
        except Exception as e:
            print(f"Text sanitization error: {e}")
            return ""

    def _get_mock_data(self) -> List[Dict]:
        """Generate mock Reddit data for testing"""
        from datetime import datetime, timedelta
        
        mock_posts = [
            {
                "platform": "reddit",
                "content": "Large demonstration reported in city center. Multiple sources confirming.",
                "author": "reddit_user",
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                "location_raw": "City Center",
                "link": "https://reddit.com/r/news/comments/123456",
                "extra": {"subreddit": "news", "score": 150, "num_comments": 25}
            },
            {
                "platform": "reddit",
                "content": "Protest organizers announce new rally location. Police monitoring situation.",
                "author": "activist_user",
                "timestamp": (datetime.utcnow() - timedelta(hours=3)).isoformat(),
                "location_raw": "Downtown",
                "link": "https://reddit.com/r/politics/comments/123457",
                "extra": {"subreddit": "politics", "score": 89, "num_comments": 12}
            }
        ]
        
        print("Using mock Reddit data")
        return mock_posts 