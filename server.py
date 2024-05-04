from flask import Flask,request
import flask
from dotenv import load_dotenv

load_dotenv()

import os

OPENAI_APIKEY=os.getenv("OPENAI_API_KEY")

from openai import OpenAI

#openai.organization = os.environ.get("OPENAI_ORGANIZATION")
client=OpenAI(api_key = OPENAI_APIKEY)

app = Flask(__name__, static_folder='.', static_url_path='')

# プロンプトの設定
client = OpenAI(
# This is the default and can be omitted
api_key=os.environ.get("OPENAI_API_KEY"),
)

@app.route('/')
def index():

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4-turbo",
    )

    # 生成されたテキストの取得
    for i, choice in enumerate(chat_completion.choices):
        print(f"\nresult {i}:")
        print(choice.message.content.strip())

    return flask.jsonify({
        "status": "I'm alive!",
        "OPENAIAPI_TestResult":chat_completion.choices[0].message.content
    })

@app.route("/eye")
def send_eyedata():

    eye_data = {"right": 0.5,"left":0.5}
    return flask.jsonify({
        "eyes": eye_data
    })

@app.route("/rewrite",methods=["POST"])
def rewrite_content():
    try:
        req=request.json
        raw_content=req.get("content")
    except:
        return flask.jsonify({
            "status" : "invalid param"
        })
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "以下の文章を書き換えてください。ただし、絶対に文字数に変化がないようにすること。¥n ================ ¥n"+raw_content,
        }
    ],
    model="gpt-4-turbo",
    )
    return flask.jsonify({
        "status":"Success",
        "content":chat_completion.choices[0].message.content
    })


@app.route("/rewrite", methods=["GET"])
def rewrite_content_qp():
    try:
        req=request.args
        raw_content=req.get("content")
    except:
        return flask.jsonify({
            "status" : "invalid param"
        })
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "以下の文章を書き換えてください。書き換える際には固有名詞はそのままにし、書き手の感想・感情・意見のみ真逆の意味合いにしてください。ただし、絶対に文字数に変化がないようにすること。¥n ================ ¥n"+raw_content,
        }
    ],
    model="gpt-4-turbo",
    )
    return flask.jsonify({
        "status":"Success",
        "content":chat_completion.choices[0].message.content.strip()
    })
        


if __name__ == "__main__":
    app.run(port=9090, debug=True)