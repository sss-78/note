from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from storage import login

database, user, password, host, port = login['database'], login['user'], login['password'], login['host'], login['port']

def get_connection():
    try:        
        conn = psycopg2.connect(database=login['database'], user=login['user'], 
                                password=login['password'], host=login['host'], port=login['port'])
        cursor = conn.cursor()
        print('Connected to Database')
        return conn
    except:
        print('Connection failed')
    
    return None

def connect_and_execute(query_string):
    try:        
        conn = psycopg2.connect(database=login['database'], user=login['user'], 
                                password=login['password'], host=login['host'], port=login['port'])
        cursor = conn.cursor()
        print('Connected to Database')

        cursor.execute(query_string)
        conn.commit()
    except Exception as e:
        print('Connection failed')
        print(e)
    finally:
        cursor.close()
        conn.close()

def create_users_table():
    query = f'''
            CREATE TABLE users (
                id SERIAL PRIMARY KEY, 
                username VARCHAR (50) UNIQUE NOT NULL, 
                email VARCHAR (255) UNIQUE NOT NULL,
                password VARCHAR (255) NOT NULL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
            );
            '''
    connect_and_execute(query)
    print('created users table')

def create_posts_table():
    query = f'''
            CREATE TABLE posts (
                id SERIAL PRIMARY KEY, 
                username VARCHAR (50) UNIQUE NOT NULL, 
                email VARCHAR (255) UNIQUE NOT NULL,
                password VARCHAR (50) NOT NULL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
            );
            '''
    connect_and_execute(query)
    print('created posts table')

def add_user(username, email, password):
    try:
        conn = get_connection()
        record_values = (username, email, password)
        query = f'''
                INSERT INTO users(username, email, password)
                VALUES (%s, %s, %s); 
                '''
        
        if conn:
            cursor = conn.cursor()
            cursor.execute(query, record_values)
            
            conn.commit() 
            cursor.close()
            conn.close()

            print('added user')

    except Exception as e:
        print(e)
    
    def validate_login(username, password):
        try:
            conn = get_connection()
            record_values = (username, password)
            query = f'''
                    select * from users where username=%s and password=%s;
                    '''
            
            if conn:
                cursor = conn.cursor()
                cursor.execute(query, record_values)

                user = cursor.fetchone()
                
                conn.commit() 
                cursor.close()
                conn.close()

                print('found user')
                return user

        except Exception as e:
            print(e)
        
        return None

        
    
    
    



