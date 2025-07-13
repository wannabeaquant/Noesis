# NOESIS - OSINT Civil Unrest Detection System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)

NOESIS is a real-time OSINT (Open Source Intelligence) system designed to detect and monitor civil unrest events globally. It combines advanced NLP processing, multi-source data collection, and interactive visualization to provide comprehensive situational awareness.

## 🌟 Features

### 🔍 **Real-time Monitoring**
- **Multi-source Data Collection**: Twitter, Reddit, News APIs, Telegram
- **Live Incident Detection**: Continuous monitoring of social media and news sources
- **Geographic Intelligence**: Automatic location detection and mapping
- **Severity Assessment**: AI-powered risk evaluation and classification

### 🧠 **Advanced AI Processing**
- **NLP Pipeline**: Sentiment analysis and protest detection
- **Verification System**: Multi-source verification for incident accuracy
- **Clustering Algorithm**: Groups related incidents for better analysis
- **Language Support**: Multi-language processing capabilities

### 📊 **Interactive Dashboard**
- **Real-time Map**: Global incident visualization with interactive markers
- **Source Verification**: Direct links to original sources for fact-checking
- **Filtering System**: Filter by severity, status, and location
- **Live Updates**: Automatic refresh and real-time data streaming

### 🔔 **Alert System**
- **Email Notifications**: Configurable alert delivery
- **Telegram Bot**: Real-time messaging for critical incidents
- **Customizable Thresholds**: Set alert conditions based on severity and location

## 🏗️ Architecture

```
NOESIS/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # REST API endpoints
│   │   ├── collectors/     # Data collection modules
│   │   ├── services/       # Core business logic
│   │   ├── models/         # Database models
│   │   ├── alerts/         # Notification system
│   │   └── utils/          # Utility functions
│   ├── data/               # Configuration and dictionaries
│   └── tests/              # Backend tests
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API integration
│   │   └── hooks/          # Custom React hooks
│   └── public/             # Static assets
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Git**

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NOESIS
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Initialize database**
   ```bash
   python create_db.py
   ```

5. **Start the backend server**
   ```bash
   python start.py
   ```
   
   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Interactive API: `http://localhost:8000/redoc`

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:5173`

## 📖 Usage

### Dashboard Features

1. **Global Map View**
   - Interactive map showing all detected incidents
   - Color-coded markers by severity (Red=High, Yellow=Medium, Green=Low)
   - Click markers to view incident details and sources

2. **Incident List**
   - Toggle between "Recent Incidents" (20) and "All Incidents" (50)
   - Expandable incident cards with detailed information
   - Real-time source verification links

3. **Filtering System**
   - Filter by severity level (High/Medium/Low)
   - Filter by verification status (Verified/Pending)
   - Geographic filtering capabilities

4. **Source Verification**
   - Direct links to original sources
   - Modal view for multiple sources
   - Domain name display for easy identification

### API Endpoints

#### Incidents
- `GET /incidents/` - Get all incidents with filtering
- `GET /incidents/latest` - Get recent incidents
- `GET /incidents/dashboard` - Get dashboard statistics
- `GET /incidents/{incident_id}` - Get specific incident

#### Collection
- `POST /collection/trigger` - Trigger data collection cycle
- `GET /collection/status` - Get collection status

#### Alerts
- `POST /alerts/subscribe` - Subscribe to alerts
- `GET /alerts/subscribers` - Get alert subscribers

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./noesis.db

# API Keys (optional for demo)
TWITTER_API_KEY=your_twitter_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
NEWS_API_KEY=your_news_api_key

# Alert Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Data Sources

The system supports multiple data sources:

- **Twitter**: Real-time tweet monitoring
- **Reddit**: Subreddit monitoring for protest discussions
- **News APIs**: RSS feeds and news article monitoring
- **Telegram**: Channel monitoring for real-time updates

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Data Flow

1. **Collection**: Data collectors gather information from multiple sources
2. **Processing**: NLP pipeline analyzes text for protest indicators
3. **Verification**: Multi-source verification confirms incident accuracy
4. **Storage**: Incidents stored in database with metadata
5. **Visualization**: Frontend displays data on interactive map
6. **Alerts**: Notification system sends alerts for critical incidents

## 🔒 Security Features

- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive input sanitization
- **CORS Configuration**: Proper cross-origin resource sharing
- **Error Handling**: Graceful error handling and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the robust backend framework
- **React** for the interactive frontend
- **Leaflet** for the mapping functionality
- **spaCy** for natural language processing
- **OpenStreetMap** for map data

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs`
- Review the code comments for implementation details

---

**NOESIS** - Empowering situational awareness through intelligent OSINT analysis. 