import uvicorn
from app.utils.database import create_tables
from dotenv import load_dotenv
import os

def main():
    # Load environment variables
    load_dotenv()
    
    # Create database tables
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")
    
    # Start the FastAPI server
    print("Starting NOESIS Backend server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 