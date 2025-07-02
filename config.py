import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:01Thiago!@db.lmautjxltjmiywsivrhf.supabase.co:5432/postgres?sslmode=require&options=--inet4")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
