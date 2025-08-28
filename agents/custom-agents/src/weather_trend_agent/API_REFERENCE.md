# Weather Trend Agent - API Reference

## Overview

The Weather Trend Agent provides comprehensive historical weather data using the Open-Meteo API. This agent can fetch weather information by location name or coordinates, supporting both historical data and forecasts.

## 🌤️ Available Tools

### 1. Geocoding Location
**Tool**: `geocode_location`

Converts location names to coordinates using Open-Meteo's geocoding service.

**Parameters**:
- `location_name` (str): Name of the location (e.g., "London", "New York", "Tokyo")

**Returns**:
```json
{
  "status": "success",
  "location_name": "London",
  "coordinates": {
    "latitude": 51.5074,
    "longitude": -0.1278
  },
  "details": {
    "name": "London",
    "country": "United Kingdom",
    "admin1": "England",
    "timezone": "Europe/London"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "open-meteo-geocoding"
}
```

**Example Usage**:
```
User: "What are the coordinates for London?"
Agent: Uses geocode_location("London") to get coordinates and location details.
```

### 2. Historical Weather by Coordinates
**Tool**: `get_historical_weather_by_coordinates`

Fetches historical weather data using latitude and longitude coordinates.

**Parameters**:
- `latitude` (float): Location latitude (-90 to 90)
- `longitude` (float): Location longitude (-180 to 180)
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format
- `hourly_variables` (list, optional): List of hourly variables to fetch
- `daily_variables` (list, optional): List of daily variables to fetch

**Returns**:
```json
{
  "status": "success",
  "location": {
    "latitude": 51.5074,
    "longitude": -0.1278
  },
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-07"
  },
  "weather_data": {
    "hourly": {
      "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
      "temperature_2m": [5.2, 4.8],
      "precipitation": [0.0, 0.1]
    },
    "daily": {
      "time": ["2024-01-01", "2024-01-02"],
      "temperature_2m_max": [8.5, 7.2],
      "temperature_2m_min": [2.1, 1.8]
    }
  },
  "variables": {
    "hourly": ["temperature_2m", "precipitation", "relativehumidity_2m", "windspeed_10m"],
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "open-meteo-archive"
}
```

**Example Usage**:
```
User: "What was the weather in London from January 1st to January 7th, 2024?"
Agent: Uses get_historical_weather_by_coordinates with London coordinates and date range.
```

### 3. Historical Weather by Location Name
**Tool**: `get_historical_weather_by_location`

Fetches historical weather data using location name (automatically geocodes first).

**Parameters**:
- `location_name` (str): Name of the location (e.g., "London", "New York")
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format
- `hourly_variables` (list, optional): List of hourly variables to fetch
- `daily_variables` (list, optional): List of daily variables to fetch

**Returns**:
```json
{
  "status": "success",
  "location": {
    "name": "London",
    "coordinates": {
      "latitude": 51.5074,
      "longitude": -0.1278
    },
    "country": "United Kingdom",
    "timezone": "Europe/London"
  },
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-07"
  },
  "weather_data": { /* Same as above */ },
  "variables": { /* Same as above */ },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "open-meteo-archive"
}
```

**Example Usage**:
```
User: "Show me the weather history for Tokyo last week"
Agent: Uses get_historical_weather_by_location with "Tokyo" and appropriate date range.
```

### 4. Weather Summary by Date
**Tool**: `get_weather_summary_by_date`

Gets a concise weather summary for a specific date.

**Parameters**:
- `latitude` (float): Location latitude (-90 to 90)
- `longitude` (float): Location longitude (-180 to 180)
- `date` (str): Date in YYYY-MM-DD format

**Returns**:
```json
{
  "status": "success",
  "location": {
    "latitude": 51.5074,
    "longitude": -0.1278
  },
  "date": "2024-01-15",
  "summary": {
    "max_temperature": 8.5,
    "min_temperature": -2.1,
    "total_precipitation": 5.2,
    "max_wind_speed": 25.0
  },
  "full_data": { /* Complete weather data */ },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "open-meteo-archive"
}
```

**Example Usage**:
```
User: "What was the weather like in New York on January 15th, 2024?"
Agent: Uses get_weather_summary_by_date with New York coordinates and the specific date.
```

### 5. Forecast Weather
**Tool**: `get_forecast_weather`

Gets weather forecast for a location.

**Parameters**:
- `latitude` (float): Location latitude (-90 to 90)
- `longitude` (float): Location longitude (-180 to 180)
- `days` (int): Number of forecast days (1-16, default: 7)
- `hourly_variables` (list, optional): List of hourly variables to fetch

**Returns**:
```json
{
  "status": "success",
  "location": {
    "latitude": 51.5074,
    "longitude": -0.1278
  },
  "forecast_days": 7,
  "weather_data": {
    "hourly": {
      "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
      "temperature_2m": [6.2, 5.8],
      "precipitation": [0.0, 0.0]
    }
  },
  "variables": {
    "hourly": ["temperature_2m", "precipitation", "relativehumidity_2m", "windspeed_10m"]
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "open-meteo-forecast"
}
```

**Example Usage**:
```
User: "What's the weather forecast for Sydney for the next 5 days?"
Agent: Uses get_forecast_weather with Sydney coordinates and 5 days forecast.
```

### 6. Available Weather Variables
**Tool**: `get_available_weather_variables`

Lists all available weather variables for Open-Meteo API.

**Parameters**: None

**Returns**:
```json
{
  "status": "success",
  "variables": {
    "hourly_variables": [
      "temperature_2m",
      "temperature_80m",
      "relativehumidity_2m",
      "precipitation",
      "windspeed_10m",
      /* ... many more */
    ],
    "daily_variables": [
      "temperature_2m_max",
      "temperature_2m_min",
      "precipitation_sum",
      "sunrise",
      "sunset",
      /* ... many more */
    ]
  },
  "description": "Available weather variables for Open-Meteo API",
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "open-meteo-documentation"
}
```

**Example Usage**:
```
User: "What weather variables are available?"
Agent: Uses get_available_weather_variables to show all available data points.
```

## 📊 Weather Variables Reference

### Hourly Variables
- `temperature_2m` - 2-meter temperature (°C)
- `temperature_80m` - 80-meter temperature (°C)
- `temperature_120m` - 120-meter temperature (°C)
- `relativehumidity_2m` - 2-meter relative humidity (%)
- `dewpoint_2m` - 2-meter dewpoint temperature (°C)
- `apparent_temperature` - Apparent temperature (°C)
- `precipitation` - Total precipitation (mm)
- `rain` - Rain (mm)
- `snowfall` - Snowfall (mm)
- `weathercode` - Weather condition code
- `pressure_msl` - Mean sea level pressure (hPa)
- `surface_pressure` - Surface pressure (hPa)
- `cloudcover` - Total cloud cover (%)
- `windspeed_10m` - 10-meter wind speed (km/h)
- `winddirection_10m` - 10-meter wind direction (°)
- `windgusts_10m` - 10-meter wind gusts (km/h)

### Daily Variables
- `temperature_2m_max` - Maximum 2-meter temperature (°C)
- `temperature_2m_min` - Minimum 2-meter temperature (°C)
- `apparent_temperature_max` - Maximum apparent temperature (°C)
- `apparent_temperature_min` - Minimum apparent temperature (°C)
- `precipitation_sum` - Total precipitation (mm)
- `rain_sum` - Total rain (mm)
- `snowfall_sum` - Total snowfall (mm)
- `precipitation_hours` - Number of hours with precipitation
- `weathercode` - Weather condition code
- `sunrise` - Sunrise time
- `sunset` - Sunset time
- `windspeed_10m_max` - Maximum 10-meter wind speed (km/h)
- `windgusts_10m_max` - Maximum 10-meter wind gusts (km/h)
- `winddirection_10m_dominant` - Dominant 10-meter wind direction (°)

## 🌍 Data Coverage

### Historical Data
- **Time Range**: 1940 to present
- **Global Coverage**: Worldwide
- **Data Resolution**: Hourly and daily
- **Update Frequency**: Real-time

### Forecast Data
- **Forecast Range**: Up to 16 days
- **Global Coverage**: Worldwide
- **Data Resolution**: Hourly
- **Update Frequency**: Every 6 hours

## 📅 Date Format

All dates should be provided in ISO 8601 format: `YYYY-MM-DD`

**Examples**:
- `2024-01-01` - January 1st, 2024
- `2023-12-31` - December 31st, 2023
- `2024-02-29` - February 29th, 2024 (leap year)

## 🎯 Common Use Cases

### 1. Historical Weather Analysis
```
User: "What was the weather like in Paris during the summer of 2023?"
Agent: Uses historical weather tools to fetch data for Paris from June to August 2023.
```

### 2. Weather Comparison
```
User: "Compare the weather in London and Tokyo for the same week last year"
Agent: Fetches historical data for both cities and provides comparison.
```

### 3. Climate Trends
```
User: "Show me temperature trends for New York over the past month"
Agent: Retrieves daily temperature data and presents trends.
```

### 4. Travel Planning
```
User: "What's the weather forecast for my trip to Rome next week?"
Agent: Gets forecast data for Rome for the upcoming week.
```

### 5. Weather Summary
```
User: "Give me a weather summary for Tokyo on my birthday last year"
Agent: Provides a concise summary of weather conditions for that specific date.
```

## ⚠️ Error Handling

The agent handles various error scenarios:

1. **Location Not Found**: Returns error message when geocoding fails
2. **Invalid Coordinates**: Validates latitude (-90 to 90) and longitude (-180 to 180)
3. **Invalid Dates**: Ensures dates are in correct format and within valid range
4. **API Errors**: Handles network issues and API service problems
5. **Data Unavailable**: Manages cases where historical data is not available

## 🔗 Data Sources

- **Open-Meteo API**: Free weather data service
- **Geocoding**: Open-Meteo Geocoding API
- **Historical Data**: Open-Meteo Archive API
- **Forecast Data**: Open-Meteo Forecast API

## 📈 Performance

- **Response Time**: Typically < 2 seconds
- **Rate Limits**: Unlimited (free tier)
- **Data Accuracy**: High-quality meteorological data
- **Availability**: 99.9% uptime

---

*This Weather History Agent provides comprehensive weather data access through Open-Meteo's free API service, enabling users to explore historical weather patterns and forecasts worldwide.*
