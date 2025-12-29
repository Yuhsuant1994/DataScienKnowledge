#!/usr/bin/env python3
"""
MCP Server with Weather and News APIs
Provides tools for fetching weather data and latest news articles
"""

import asyncio
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Initialize the MCP server
app = Server("weather-news-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the MCP server."""
    return [
        Tool(
            name="get_weather",
            description="Get current weather and forecast for a location using coordinates (latitude, longitude) or city name",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location (-90 to 90)"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location (-180 to 180)"
                    },
                    "city": {
                        "type": "string",
                        "description": "City name (alternative to lat/lon). Will use geocoding to find coordinates."
                    },
                    "forecast_days": {
                        "type": "integer",
                        "description": "Number of forecast days (1-7). Default is 3.",
                        "minimum": 1,
                        "maximum": 7
                    }
                },
                "oneOf": [
                    {"required": ["latitude", "longitude"]},
                    {"required": ["city"]}
                ]
            }
        ),
        Tool(
            name="get_news",
            description="Get latest news articles by topic, country, or search query. Uses NewsAPI.org",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query or keywords (e.g., 'technology', 'bitcoin', 'climate change')"
                    },
                    "category": {
                        "type": "string",
                        "description": "News category",
                        "enum": ["business", "entertainment", "general", "health", "science", "sports", "technology"]
                    },
                    "country": {
                        "type": "string",
                        "description": "2-letter ISO country code (e.g., 'us', 'gb', 'de'). Default is 'us'."
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of articles to return (1-100). Default is 10.",
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="search_location",
            description="Search for location coordinates by city name or address",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or address to search for"
                    }
                },
                "required": ["location"]
            }
        )
    ]


async def geocode_location(location: str) -> dict[str, Any]:
    """Geocode a location string to coordinates using Open-Meteo geocoding API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"}
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            raise ValueError(f"Location '{location}' not found")

        result = data["results"][0]
        return {
            "name": result.get("name"),
            "country": result.get("country"),
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude"),
            "timezone": result.get("timezone")
        }


async def fetch_weather(latitude: float, longitude: float, forecast_days: int = 3) -> dict[str, Any]:
    """Fetch weather data from Open-Meteo API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
                "forecast_days": forecast_days,
                "timezone": "auto"
            }
        )
        response.raise_for_status()
        return response.json()


async def fetch_news(query: str | None = None, category: str | None = None,
                    country: str = "us", page_size: int = 10) -> dict[str, Any]:
    """
    Fetch news from NewsAPI.org
    Note: For production use, you'll need to set NEWSAPI_KEY environment variable
    For demo purposes, this uses the public API with limited access
    """
    import os

    api_key = os.getenv("NEWSAPI_KEY", "demo")  # Use 'demo' for testing or set your API key

    async with httpx.AsyncClient() as client:
        # Use different endpoints based on parameters
        if query:
            # Everything endpoint for search queries
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "pageSize": page_size,
                "sortBy": "publishedAt",
                "apiKey": api_key
            }
        else:
            # Top headlines endpoint for category/country
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "country": country,
                "pageSize": page_size,
                "apiKey": api_key
            }
            if category:
                params["category"] = category

        response = await client.get(url, params=params)

        # Handle API key issues gracefully
        if response.status_code == 401:
            return {
                "status": "error",
                "message": "NewsAPI key not configured. Set NEWSAPI_KEY environment variable. Get free key at https://newsapi.org/register"
            }

        response.raise_for_status()
        return response.json()


def format_weather_response(weather_data: dict[str, Any], location_info: dict[str, Any] | None = None) -> str:
    """Format weather data into a readable string."""
    current = weather_data.get("current", {})
    daily = weather_data.get("daily", {})

    # Weather code descriptions (WMO codes)
    weather_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }

    result = []

    if location_info:
        result.append(f"Location: {location_info.get('name')}, {location_info.get('country')}")
        result.append(f"Coordinates: {location_info.get('latitude'):.4f}°, {location_info.get('longitude'):.4f}°\n")

    result.append("🌤️  CURRENT WEATHER")
    result.append(f"Temperature: {current.get('temperature_2m')}°C (feels like {current.get('apparent_temperature')}°C)")
    result.append(f"Conditions: {weather_codes.get(current.get('weather_code'), 'Unknown')}")
    result.append(f"Humidity: {current.get('relative_humidity_2m')}%")
    result.append(f"Wind Speed: {current.get('wind_speed_10m')} km/h")
    result.append(f"Precipitation: {current.get('precipitation')} mm\n")

    result.append("FORECAST")
    for i, date in enumerate(daily.get("time", [])):
        weather_code = daily["weather_code"][i]
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        precip = daily["precipitation_sum"][i]

        result.append(f"{date}: {weather_codes.get(weather_code, 'Unknown')}")
        result.append(f"  🌡️  {temp_min}°C - {temp_max}°C | 💧 {precip}mm")

    return "\n".join(result)


def format_news_response(news_data: dict[str, Any]) -> str:
    """Format news data into a readable string."""
    if news_data.get("status") == "error":
        return f"error: {news_data.get('message')}"

    articles = news_data.get("articles", [])
    total = news_data.get("totalResults", 0)

    if not articles:
        return "No news articles found."

    result = [f"Found {total} articles (showing {len(articles)}):\n"]

    for i, article in enumerate(articles, 1):
        result.append(f"{i}. {article.get('title')}")
        result.append(f"   Source: {article.get('source', {}).get('name')}")
        result.append(f"   Published: {article.get('publishedAt', 'Unknown')}")
        if article.get('description'):
            result.append(f"   {article['description'][:150]}...")
        result.append(f"   URL: {article.get('url')}\n")

    return "\n".join(result)


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    try:
        if name == "get_weather":
            # Handle city-based lookup or direct coordinates
            if "city" in arguments:
                location_info = await geocode_location(arguments["city"])
                latitude = location_info["latitude"]
                longitude = location_info["longitude"]
            else:
                latitude = arguments["latitude"]
                longitude = arguments["longitude"]
                location_info = None

            forecast_days = arguments.get("forecast_days", 3)

            weather_data = await fetch_weather(latitude, longitude, forecast_days)
            formatted_response = format_weather_response(weather_data, location_info)

            return [TextContent(type="text", text=formatted_response)]

        elif name == "get_news":
            query = arguments.get("query")
            category = arguments.get("category")
            country = arguments.get("country", "us")
            page_size = arguments.get("page_size", 10)

            news_data = await fetch_news(query, category, country, page_size)
            formatted_response = format_news_response(news_data)

            return [TextContent(type="text", text=formatted_response)]

        elif name == "search_location":
            location = arguments["location"]
            location_info = await geocode_location(location)

            result = [
                f"Location: {location_info['name']}, {location_info['country']}",
                f"Latitude: {location_info['latitude']}",
                f"Longitude: {location_info['longitude']}",
                f"Timezone: {location_info['timezone']}"
            ]

            return [TextContent(type="text", text="\n".join(result))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
