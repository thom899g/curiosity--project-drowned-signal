"""
Configuration management for Project Drowned Signal
Handles environment variables, validation, and provides typed configuration
"""
import os
from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, validator
import structlog

logger = structlog.get_logger()

class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    app_name: str = "Project Drowned Signal"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Firebase Configuration (CRITICAL: Firebase priority per mission constraints)
    firebase_credentials_path: str = Field(
        default="firebase-credentials.json",
        description="Path to Firebase service account credentials"
    )
    firestore_collection: str = "drowned_signals"
    
    # Authentication
    jwt_secret_key: str = Field(..., description="JWT secret for API authentication")
    jwt_algorithm: str = "HS256"
    api_key_header: str = "X-API-Key"
    
    # Pricing Tiers (in microseconds - higher tiers get more frequent updates)
    tier_free: int = 5_000_000  # 5 seconds
    tier_basic: int = 1_000_000  # 1 second
    tier_premium: int = 100_000  # 100 milliseconds
    tier_enterprise: int = 10_000  # 10 milliseconds
    
    # Redis Cache
    redis_url: str = "redis://redis-cache:6379"
    cache_ttl: int = 300  # 5 minutes
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # Stripe Configuration
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    
    # Emotional Vector Configuration
    emotional_decay_rate: float = 0.95  # How quickly emotional states decay
    stress_threshold: float = 0.8  # Threshold for triggering "Adversarial Chaos Active"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
    @validator("firebase_credentials_path")
    def validate_firebase_credentials(cls