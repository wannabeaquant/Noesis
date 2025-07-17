#!/usr/bin/env python3
"""
Test script for real-world NOESIS setup
"""

import asyncio
import os
from dotenv import load_dotenv
from app.services.simple_collector import SimpleRealTimeCollector

# Load environment variables
load_dotenv()

async def test_setup():
    """Test the real-world setup"""
    print("🌍 Testing NOESIS Real-World Setup")
    print("=" * 50)
    
    # Check API keys
    print("\n📋 API Key Status:")
    twitter_key = os.getenv('TWITTER_BEARER_TOKEN')
    news_key = os.getenv('NEWS_API_KEY')
    weather_key = os.getenv('WEATHER_API_KEY')
    
    print(f"Twitter API: {'✅ Configured' if twitter_key else '❌ Not configured'}")
    print(f"News API: {'✅ Configured' if news_key else '❌ Not configured'}")
    print(f"Weather API: {'✅ Configured' if weather_key else '❌ Not configured'}")
    
    # Test data collection
    print("\n🔍 Testing Data Collection...")
    collector = SimpleRealTimeCollector()
    
    try:
        data = await collector.collect_all_data()
        print(f"✅ Successfully collected {len(data)} data points")
        
        if data:
            print("\n📊 Sample Data:")
            for i, point in enumerate(data[:3]):
                print(f"{i+1}. {point.source}: {point.content[:60]}...")
                print(f"   Sentiment: {point.sentiment_score:.2f}")
                print(f"   Confidence: {point.confidence:.2f}")
                print()
        else:
            print("⚠️  No data collected (this is normal if no API keys are configured)")
            
    except Exception as e:
        print(f"❌ Error during data collection: {e}")
    
    # Rate limit info
    print("\n⏱️  Rate Limits (Free Tiers):")
    print("Twitter: 300 requests per 15 minutes")
    print("News: 100 requests per day")
    print("Weather: 60 requests per minute")
    print("Reddit: No limits (public API)")
    
    print("\n🎯 Next Steps:")
    if not any([twitter_key, news_key, weather_key]):
        print("1. Get API keys from the services mentioned above")
        print("2. Create a .env file with your API keys")
        print("3. Run this test again")
    else:
        print("1. Your setup is working!")
        print("2. Start the backend: uvicorn main:app --reload")
        print("3. Visit http://localhost:8000/docs")

if __name__ == "__main__":
    asyncio.run(test_setup()) 