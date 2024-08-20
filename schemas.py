import anthropic
import os
from flask import Flask, render_template, request
import json
import psycopg2
from typing import Optional
from pydantic import BaseModel

class RequestFormDataModel(BaseModel):
    username: str
    email: str
    password: str

class RequestBodyDataModel(BaseModel):
    username: str
    email: str
    password: str

class UserResponseModel(BaseModel):
    username: str
    email: str

class RequestFormLoginDataModel(BaseModel):
    username: str
    password: str

