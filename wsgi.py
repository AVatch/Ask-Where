#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/Ask-Where/")

from app import app as application
from os.path import dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

application.secret_key = os.environ.get('SECRET')