# NOESIS Backend

A real-time OSINT backend to detect, verify, and report civil unrest (protests, riots, strikes) using public data from Twitter, Reddit, Telegram, and News APIs.

## Features

- **Multi-Source Data Collection**: Twitter, Reddit, Telegram, and News APIs
- **NLP Processing**: Protest relevance classification, sentiment analysis, NER, geolocation
- **Verification System**: Multi-source verification with confidence scoring
- **Real-time Alerts**: Telegram bot and email notifications
- **REST API**: Complete API for frontend integration
- **Moderation Tools**: Admin controls for false positive management

## Quick Start

### 1. Environment Setup

Create a `.env` file with your API keys:

```env
# Database (SQLite - no setup required)
DATABASE_URL=sqlite:///./noesis.db

# Twitter API v2
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=NOESIS_Bot/1.0

# Telegram API (Optional - for Telegram bot alerts)
# Note: python-telegram-bot has compatibility issues with Python 3.13
# If you need Telegram alerts, consider using Python 3.11 or 3.12
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# GNews API
GNEWS_API_KEY=your_gnews_api_key

# Geocoding: Uses OpenStreetMap Nominatim (free, no API key needed)

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

No setup required! The system uses SQLite which creates a `noesis.db` file automatically.

### 4. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Incidents
- `GET /incidents/` - Get incidents with filtering
- `GET /incidents/latest` - Get latest verified incidents
- `GET /incidents/{incident_id}` - Get incident details
- `GET /incidents/stats/summary` - Get incident statistics

### Collection
- `POST /collection/run-cycle` - Manually trigger data collection
- `GET /collection/status` - Get collection system status

### Alerts
- `POST /alerts/subscribe` - Subscribe to alerts
- `POST /alerts/unsubscribe` - Unsubscribe from alerts

### Moderation
- `POST /moderate/flag` - Flag false positive
- `POST /moderate/confirm` - Confirm incident
- `POST /moderate/merge` - Merge duplicate incidents

## Data Flow

1. **Collection**: Raw data collected from Twitter, Reddit, Telegram, and News APIs
2. **Processing**: NLP pipeline processes posts for relevance, sentiment, entities, and geolocation
3. **Verification**: Posts are clustered and verified based on multi-source confirmation
4. **Alerting**: Verified incidents trigger Telegram and email alerts
5. **API**: REST endpoints provide data access for frontend applications

## Architecture

```
app/
├── api/               # FastAPI endpoints
├── models/            # SQLAlchemy models
├── services/          # NLP, verification, orchestration
├── collectors/        # Data collection modules
├── alerts/            # Alert services
└── utils/             # Database and utilities
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. 