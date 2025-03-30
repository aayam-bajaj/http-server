class Config:
    # Local MongoDB Configuration
    MONGO_URI = "mongodb://localhost:27017/crowd_monitoring"
    
    # No TLS/SSL needed for local development
    SECRET_KEY = "miniproject"  # Only needed for session encryption
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max payload