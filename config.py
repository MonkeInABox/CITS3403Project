import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3Cr3t-KeY-T3mp-plZ-rePlac3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    POSTS_PER_PAGE = 3
    RECAPTCHA_PUBLIC_KEY = "6LdpN8ApAAAAADm-N-ukFFHYR1jjsuFCuzY7o2yv"
    RECAPTCHA_PRIVATE_KEY = "6LdpN8ApAAAAAOfh7IfhskbyqU35uhqet9yoMaSi"