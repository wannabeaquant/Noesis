from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict
import math
from app.utils.geocoding import GeocodingService

class VerificationService:
    def __init__(self):
        self.time_window = timedelta(minutes=60)  # 60-minute clustering window (loosened)
        self.distance_threshold = 200  # 200km radius for location clustering (loosened)
        self.geocoding_service = GeocodingService()

    def verify(self, processed_posts: List[Dict]) -> List[Dict]:
        """Verify and cluster processed posts into incidents"""
        # Filter posts with lower protest scores (loosened)
        relevant_posts = [post for post in processed_posts if post.get("protest_score", 0) > 0.15]
        
        # Group posts by location and time
        clusters = self.cluster_posts(relevant_posts)
        
        # Create incidents from clusters
        incidents = []
        for cluster in clusters:
            if len(cluster) >= 1:  # Allow single posts to form an incident (loosened)
                incident = self.create_incident(cluster)
                incidents.append(incident)
        
        return incidents

    def cluster_posts(self, posts: List[Dict]) -> List[List[Dict]]:
        """Cluster posts by location and time proximity"""
        clusters = []
        processed = set()
        
        for i, post in enumerate(posts):
            if i in processed:
                continue
            
            cluster = [post]
            processed.add(i)
            
            # Find posts within time and location proximity
            for j, other_post in enumerate(posts[i+1:], i+1):
                if j in processed:
                    continue
                
                if self.are_posts_proximate(post, other_post):
                    cluster.append(other_post)
                    processed.add(j)
            
            if len(cluster) > 0:
                clusters.append(cluster)
        
        return clusters

    def are_posts_proximate(self, post1: Dict, post2: Dict) -> bool:
        """Check if two posts are proximate in time and location"""
        # Check time proximity
        time1 = datetime.fromisoformat(post1.get("timestamp", "").replace("Z", "+00:00"))
        time2 = datetime.fromisoformat(post2.get("timestamp", "").replace("Z", "+00:00"))
        
        if abs((time1 - time2).total_seconds()) > self.time_window.total_seconds():
            return False
        
        # Check location proximity
        lat1, lng1 = post1.get("location_lat"), post1.get("location_lng")
        lat2, lng2 = post2.get("location_lat"), post2.get("location_lng")
        
        if lat1 and lng1 and lat2 and lng2:
            distance = self.calculate_distance(lat1, lng1, lat2, lng2)
            return distance <= self.distance_threshold
        
        # If no coordinates, check if they're from the same platform (basic clustering)
        return post1.get("platform") == post2.get("platform")

    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c

    def create_incident(self, cluster: List[Dict]) -> Dict:
        """Create an incident from a cluster of posts"""
        # Calculate average location
        lats = [post.get("location_lat") for post in cluster if post.get("location_lat")]
        lngs = [post.get("location_lng") for post in cluster if post.get("location_lng")]
        
        avg_lat = sum(lats) / len(lats) if lats else None
        avg_lng = sum(lngs) / len(lngs) if lngs else None
        
        # Determine severity based on sentiment and number of sources
        avg_sentiment = sum(post.get("sentiment_score", 0) for post in cluster) / len(cluster)
        platform_diversity = len(set(post.get("platform") for post in cluster))
        
        if platform_diversity >= 2 or avg_sentiment < -0.3:
            severity = "high"
            status = "verified"
        elif platform_diversity >= 1 and len(cluster) >= 3:
            severity = "medium"
            status = "medium"
        else:
            severity = "low"
            status = "unverified"
        
        # Create title from most relevant post
        most_relevant = max(cluster, key=lambda x: x.get("protest_score", 0))
        
        return {
            "title": f"Civil unrest reported in {self.get_location_name(avg_lat, avg_lng)}",
            "description": f"Multiple sources report civil unrest. {len(cluster)} posts across {platform_diversity} platforms.",
            "sources": [post.get("link") for post in cluster if post.get("link")],
            "location": self.get_location_name(avg_lat, avg_lng),
            "location_lat": avg_lat,
            "location_lng": avg_lng,
            "severity": severity,
            "status": status,
            "confidence_score": self.calculate_confidence(cluster),
            "platform_diversity": platform_diversity,
            "source_count": len(cluster)
        }

    def get_location_name(self, lat: float, lng: float) -> str:
        """Get location name from coordinates using reverse geocoding"""
        if lat is None or lng is None:
            return "Unknown Location"
        
        # Try to get human-readable place name
        place_name = self.geocoding_service.get_place_name(lat, lng)
        if place_name and place_name != "Unknown Location":
            return place_name
        
        # Fallback to coordinates if geocoding fails
        return f"Location ({lat:.2f}, {lng:.2f})"

    def calculate_confidence(self, cluster: List[Dict]) -> int:
        """Calculate confidence score (0-100)"""
        platform_diversity = len(set(post.get("platform") for post in cluster))
        post_count = len(cluster)
        avg_protest_score = sum(post.get("protest_score", 0) for post in cluster) / len(cluster)
        
        # Base score from protest relevance
        confidence = int(avg_protest_score * 50)
        
        # Boost for multiple sources
        if post_count >= 3:
            confidence += 20
        elif post_count >= 2:
            confidence += 10
        
        # Boost for platform diversity
        if platform_diversity >= 2:
            confidence += 20
        elif platform_diversity >= 1:
            confidence += 10
        
        return min(confidence, 100) 