#!/usr/bin/env python3
"""
Test script for the Weather & News MCP Server
Run this to verify the server APIs are working correctly
"""

import asyncio
from main import fetch_weather, fetch_news, geocode_location


async def test_weather():
    """Test weather API"""
    print("🌤️  Testing Weather API...")
    print("-" * 50)

    # Test with coordinates (Tokyo)
    print("\n1. Testing with coordinates (Tokyo: 35.6762, 139.6503)")
    try:
        weather = await fetch_weather(35.6762, 139.6503, forecast_days=3)
        current = weather.get("current", {})
        print(f"   ✅ Temperature: {current.get('temperature_2m')}°C")
        print(f"   ✅ Wind Speed: {current.get('wind_speed_10m')} km/h")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test geocoding
    print("\n2. Testing geocoding (London)")
    try:
        location = await geocode_location("London")
        print(f"   ✅ Found: {location['name']}, {location['country']}")
        print(f"   ✅ Coordinates: {location['latitude']}, {location['longitude']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


async def test_news():
    """Test news API"""
    print("\n\n📰 Testing News API...")
    print("-" * 50)

    # Test search query
    print("\n1. Testing search query (technology)")
    try:
        news = await fetch_news(query="technology", page_size=3)
        if news.get("status") == "error":
            print(f"   ⚠️  {news.get('message')}")
            print("   💡 Tip: Set NEWSAPI_KEY environment variable for full access")
        else:
            articles = news.get("articles", [])
            print(f"   ✅ Found {len(articles)} articles")
            if articles:
                print(f"   ✅ First article: {articles[0].get('title')[:60]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test top headlines
    print("\n2. Testing top headlines (US)")
    try:
        news = await fetch_news(country="us", page_size=3)
        if news.get("status") == "error":
            print(f"   ⚠️  {news.get('message')}")
        else:
            articles = news.get("articles", [])
            print(f"   ✅ Found {len(articles)} articles")
            if articles:
                print(f"   ✅ First headline: {articles[0].get('title')[:60]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")


async def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("Testing Weather & News MCP Server")
    print("=" * 50)

    await test_weather()
    await test_news()

    print("\n" + "=" * 50)
    print("✅ Testing complete!")
    print("=" * 50)
    print("\nTo use this server with Claude Desktop:")
    print("1. Add the server config to claude_desktop_config.json")
    print("2. (Optional) Set NEWSAPI_KEY environment variable")
    print("3. Restart Claude Desktop")
    print("\nSee README.md for detailed instructions.")


if __name__ == "__main__":
    asyncio.run(main())
