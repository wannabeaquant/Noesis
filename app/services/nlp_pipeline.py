from typing import Dict, List
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import geotext
import requests
import os
from langdetect import detect, DetectorFactory
import json

# Set seed for consistent language detection
DetectorFactory.seed = 0

class NLPPipeline:
    def __init__(self):
        # Load models
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Load protest slang dictionary
        try:
            with open("data/protest_slang_dict.json", "r", encoding='utf-8') as f:
                self.protest_slang = json.load(f)
        except FileNotFoundError:
            # Fallback if file doesn't exist
            self.protest_slang = {
                "en": ["protest", "riot", "strike", "tear gas"],
                "hi": ["andolan", "hartal", "vidroh"],
                "bn": ["birodh", "andolon"],
                "ur": ["احتجاج", "ہڑتال"]
            }
        except UnicodeDecodeError:
            # Fallback if encoding issues
            print("Warning: Could not read protest_slang_dict.json due to encoding issues, using fallback")
            self.protest_slang = {
                "en": ["protest", "riot", "strike", "tear gas"],
                "hi": ["andolan", "hartal", "vidroh"],
                "bn": ["birodh", "andolon"],
                "ur": ["احتجاج", "ہڑتال"]
            }
        
        # Load language map
        try:
            with open("data/language_map.json", "r", encoding='utf-8') as f:
                self.language_map = json.load(f)
        except FileNotFoundError:
            # Fallback if file doesn't exist
            self.language_map = {
                "en": "English",
                "hi": "Hindi",
                "bn": "Bengali",
                "ur": "Urdu"
            }
        except UnicodeDecodeError:
            # Fallback if encoding issues
            print("Warning: Could not read language_map.json due to encoding issues, using fallback")
            self.language_map = {
                "en": "English",
                "hi": "Hindi",
                "bn": "Bengali",
                "ur": "Urdu"
            }
        
        # Initialize relevance classifier (using a simple keyword-based approach)
        self.protest_keywords = []
        for lang_keywords in self.protest_slang.values():
            self.protest_keywords.extend(lang_keywords)
        
        # Use Nominatim (OpenStreetMap) for geocoding - no API key needed
        self.geocoding_service = "nominatim"
        
        # Load spaCy English model for NER (if available)
        try:
            self.spacy_nlp = spacy.load('en_core_web_sm')
        except Exception as e:
            print(f"spaCy model not available: {e}")
            self.spacy_nlp = None

        # AI-based zero-shot classifier for protest relevance
        try:
            self.unrest_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        except Exception as e:
            print(f"Zero-shot classifier not available: {e}")
            self.unrest_classifier = None

    def process(self, post: Dict) -> Dict:
        """Process a post through the full NLP pipeline"""
        content = post.get("content", "")
        
        # 1. Language detection (no translation for now - simplified)
        language = self.detect_language(content)
        
        # 2. Protest relevance classification
        protest_score = self.classify_protest_relevance(content)
        
        # 3. Named Entity Recognition
        entities = self.extract_entities(content)
        
        # 4. Sentiment analysis
        sentiment_score = self.analyze_sentiment(content)
        
        # 5. Geolocation extraction
        location_lat, location_lng = self.extract_geolocation(content, post.get("location_raw", ""))
        
        return {
            "raw_post_id": post.get("id"),
            "protest_score": protest_score,
            "sentiment_score": sentiment_score,
            "location_lat": location_lat,
            "location_lng": location_lng,
            "language": language,
            "platform": post.get("platform"),
            "link": post.get("link"),
            "entities": entities,
            "status": "unverified"
        }

    def detect_language(self, text: str) -> str:
        """Detect language of the text"""
        try:
            if not text or len(text.strip()) == 0:
                return "en"
            # Clean text and handle encoding issues
            clean_text = self.clean_text(text[:100])
            return detect(clean_text)
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en"  # Default to English

    def clean_text(self, text: str) -> str:
        """Clean text and handle encoding issues"""
        try:
            # Handle different encodings
            if isinstance(text, bytes):
                text = text.decode('utf-8', errors='ignore')
            
            # Handle None or non-string types
            if not isinstance(text, str):
                text = str(text)
            
            # Remove or replace problematic characters more aggressively
            import re
            # Remove control characters and non-printable characters
            text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
            # Remove characters that can't be encoded properly
            text = re.sub(r'[^\x20-\x7E\u00A0-\uFFFF]', ' ', text)
            # Replace multiple spaces and newlines with single space
            text = re.sub(r'\s+', ' ', text)
            # Remove any remaining problematic characters
            text = ''.join(char for char in text if ord(char) < 65536)
            
            return text.strip()
        except Exception as e:
            print(f"Text cleaning error: {e}")
            return "text"

    def classify_protest_relevance(self, text: str) -> float:
        """Classify if text is protest-related (0.0 to 1.0) using zero-shot classification if available, else fallback to keyword logic."""
        try:
            clean_text = self.clean_text(text)
            if self.unrest_classifier:
                result = self.unrest_classifier(
                    clean_text,
                    candidate_labels=["protest", "riot", "civil unrest", "normal news", "sports", "entertainment"],
                    multi_label=True
                )
                # Return the score for the most relevant unrest label
                scores = [score for label, score in zip(result['labels'], result['scores']) if label in ["protest", "riot", "civil unrest"]]
                return max(scores) if scores else 0.0
            else:
                # Fallback to keyword logic
                text_lower = clean_text.lower()
                keyword_count = sum(1 for keyword in self.protest_keywords if keyword.lower() in text_lower)
                words = clean_text.split()
                if len(words) == 0:
                    return 0.0
                keyword_density = keyword_count / len(words)
                if keyword_count > 1:
                    keyword_density *= 1.5
                return min(keyword_density * 10, 1.0)
        except Exception as e:
            print(f"AI protest classification error: {e}")
            return 0.0

    def extract_entities(self, text: str) -> Dict:
        """Extract named entities (locations, organizations, persons)"""
        entities = {
            "locations": [],
            "organizations": [],
            "persons": []
        }
        
        try:
            # Clean text first
            clean_text = self.clean_text(text)
            
            # Extract locations using geotext
            try:
                geo = geotext.GeoText(clean_text)
                entities["locations"] = list(set(geo.cities + geo.countries))
            except Exception as e:
                print(f"Geotext error: {e}")
            
            # Simple organization extraction (police, government, etc.)
            org_keywords = ["police", "government", "army", "military", "party", "ministry"]
            for keyword in org_keywords:
                if keyword.lower() in clean_text.lower():
                    entities["organizations"].append(keyword.title())
        except Exception as e:
            print(f"Entity extraction error: {e}")
        
        return entities

    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment using VADER"""
        try:
            clean_text = self.clean_text(text)
            scores = self.sentiment_analyzer.polarity_scores(clean_text)
            return scores["compound"]  # Returns -1 to 1
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return 0.0

    def extract_geolocation(self, text: str, location_raw: str) -> tuple:
        """Extract latitude and longitude from text or raw location, using multiple methods"""
        try:
            clean_text = self.clean_text(text)
            locations = set()
            # 1. geotext cities/countries
            try:
                geo = geotext.GeoText(clean_text)
                locations.update(geo.cities)
                locations.update(geo.countries)
            except Exception as e:
                print(f"Geotext location extraction error: {e}")
            # 2. spaCy NER (if available)
            if self.spacy_nlp:
                try:
                    doc = self.spacy_nlp(clean_text)
                    for ent in doc.ents:
                        if ent.label_ in ["GPE", "LOC"]:
                            locations.add(ent.text)
                except Exception as e:
                    print(f"spaCy NER error: {e}")
            # 3. location_raw fallback
            if location_raw:
                clean_location = self.clean_text(location_raw)
                locations.add(clean_location)
            # Try geocoding all found locations, return first valid
            for loc in locations:
                latlng = self.geocode_location(loc)
                if latlng and latlng[0] is not None and latlng[1] is not None:
                    return latlng
        except Exception as e:
            print(f"Geolocation extraction error: {e}")
        return None, None

    def geocode_location(self, location: str) -> tuple:
        """Convert location string to lat/lng using Nominatim (OpenStreetMap)"""
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": location,
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            }
            
            # Add User-Agent header (required by Nominatim)
            headers = {
                "User-Agent": "NOESIS_Bot/1.0 (https://github.com/your-repo)"
            }
            
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lng = float(data[0]["lon"])
                return lat, lng
        
        except Exception as e:
            print(f"Geocoding error: {e}")
        
        return None, None 