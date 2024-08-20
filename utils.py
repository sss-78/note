import anthropic
import os
import bcrypt
import base64
import httpx

def call():
    api_key = os.environ['ANTHROPIC_API_KEY']

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="Just respond concisely",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give me a detailed overview of the krebs cycle? Include main ideas and sample questions."
                    }
                ]
            }
        ]
    )
    return message.content[0].text


def upload():
    image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
    image1_media_type = "image/jpeg"
    image1_data = base64.b64encode(httpx.get(image1_url).content).decode("utf-8")

    image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
    image2_media_type = "image/jpeg"
    image2_data = base64.b64encode(httpx.get(image2_url).content).decode("utf-8")

    api_key = os.environ['ANTHROPIC_API_KEY']
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Describe this image."
                    }
                ],
            }
        ],
    )
    print(message.content[0].text)
    pass

def hash(s):
    password = s.encode('utf-8')
    
    # Adding the salt to password
    salt = bcrypt.gensalt()

    # Hashing the password
    hashed = bcrypt.hashpw(password, salt)

    return hashed.decode('utf-8')

def validate_password(password_input, password_actual):
    return bcrypt.checkpw(password_input.encode('utf-8'), password_actual.encode('utf-8'))


