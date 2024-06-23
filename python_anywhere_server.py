from flask import Flask,request, jsonify
import flask


import os


from openai import OpenAI


app = Flask(__name__, static_folder='.', static_url_path='')

# プロンプトの設定
client = OpenAI(
# 環境上では下手打ちで入力（bad）
api_key="APIKEY",
)

prompts = ["入力テキストの感想・感情・意見を真逆の意味合いに書き換えてください。ただし固有名詞はそのままにし、元の文字数を厳密に維持してください。",
"入力テキストの感想・感情・意見など主観的な部分を楽観的に書き替えてください。但し、固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を悲観的に書き替えてください。但し、固有名詞と客観的事実は変更しないでください。",
"入力テキストの文体を論文で記述するような文体にしてください。但し、固有名詞と客観的事実は変更しないでください。",
"入力テキストの文体をポエム・詩のように感情的に、情緒的に書き替えてください。但し、固有名詞と客観的事実は変更しないでください。"
]

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-API-KEY')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


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
    return jsonify({
        "status":"Success",
        "content":chat_completion.choices[0].message.content.strip()
    })

@app.route('/mutate', methods=['POST'])
def mutate_text():
    try:
        req=request.json
        window_id = req.get("clientId")
        raw_content = req.get("targetText")
        text_index = req.get("textIndex")
    except:
        return flask.jsonify({
            "status":"invalid param"
            })

    # ここでtarget_textに対してテキスト変換処理を行う
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompts[int(window_id)]+"¥n ================ ¥n"+raw_content,
        }
    ],
    model="gpt-4-turbo",
    )
    mutated_text=chat_completion.choices[0].message.content.strip()

    response = {
        'result':{
            'modifiedText': mutated_text,
            'textIndex': text_index
            }
    }

    return jsonify(response),200

@app.route('/mutate2', methods=['POST'])
def mutate_text_2():
    try:
        req=request.json
        window_id = req.get("clientId")
        raw_contents = req.get("targetText").split("。") # "。"で分割し、文字列の配列に変換
        text_index = req.get("textIndex")
    except:
        return flask.jsonify({
            "status":"invalid param"
            })

    # 分割された文字列の配列に対してテキスト変換処理を行う
    mutated_texts = []
    for raw_content in raw_contents:
        if raw_content.strip():  # 空の文字列をスキップ
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompts[int(window_id)] + "¥n ================ ¥n" + raw_content+"。",
                    }
                ],
                model="gpt-4-turbo",
            )
            mutated_text = chat_completion.choices[0].message.content.strip()
            mutated_texts.append(mutated_text)

    response = {
        'result': {
            'mutatedText': mutated_texts,  # 変換後のテキストの配列
            'textIndex': text_index  # テキストのインデックスの配列
        }
    }

    return jsonify(response), 200


@app.route('/mutate', methods=['GET'])
def get_mutate_text():
    try:
        req=request.args
        window_id = req.get("clientId")
        raw_content = req.get("text")
    except:
        return flask.jsonify({
            "status":"invalid param"
            })

    # ここでtarget_textに対してテキスト変換処理を行う
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompts[int(window_id)]+"¥n ================ ¥n"+raw_content,
        }
    ],
    model="gpt-4-turbo",
    )
    mutated_text=chat_completion.choices[0].message.content.strip()

    response = {
        'result':{
            'modifiedText': mutated_text
            }
    }

    return jsonify(response),200



if __name__ == "__main__":
    app.run(port=9090, debug=True)