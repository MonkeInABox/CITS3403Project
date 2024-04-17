import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3Cr3t-KeY-T3mp-plZ-rePlac3'