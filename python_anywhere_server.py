from flask import Flask,request, jsonify
import flask


import os


from openai import OpenAI


app = Flask(__name__, static_folder='.', static_url_path='')

# プロンプトの設定
client = OpenAI(
# 環境上で手打ち
api_key="API_KEY",
)

prompts = ["入力テキストの感想・感情・意見を真逆の意味合いに書き換えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を楽観的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を悲観的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を自己拡張的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を理想主義的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を批判的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を諦念的、現実主義的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を自責的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの感想・感情・意見など主観的な部分を他責的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの文体を論文で記述するような文体にしてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"入力テキストの文体をポエム・詩のように感情的に、情緒的に書き替えてください。但し、口調・固有名詞と客観的事実は変更しないでください。",
"""以下の文章において、書き手の主観的な感想や意見が含まれている部分を特定し、それらをより客観的で事実に基づいた表現に書き換えてください。感情的な言葉や個人的な判断を避け、中立的な立場から観察可能な事実のみを述べるようにしてください。ただし、以下の点に注意してください:

1. 客観的な事実や情報は変更しないでください。
2. 文章の全体的な構造、長さ、および文体は可能な限り維持してください。
3. 専門用語や固有名詞はそのまま使用してください。
4. 数値データや統計情報は正確に保持してください。
5. 引用や参照がある場合は、それらを保持してください。
6. 文章のトーンや論理の流れを大きく変えないようにしてください。
7. 主観的表現を客観的に書き換える際は、可能な限り具体的なデータや事例を用いてください。
8. 曖昧な表現や一般化を避け、具体的かつ明確な表現を心がけてください。
9. 必要に応じて、情報源や根拠を追加してください。
10. 書き換えた後、元の文章と比較して変更した箇所を簡潔に説明し、その理由を述べてください。

この作業を通じて、文章の客観性と信頼性を高めることを目指してください。"""

]

def process_string(input_string):
    # 1. 最後の===の位置を見つける
    last_separator_index = input_string.rfind('===')
    
    if last_separator_index != -1:
        # 2. ===以降の部分文字列を抽出
        result = input_string[last_separator_index + 3:]
        
        # 3. 改行文字を削除
        result = result.strip()
        
        return result
    else:
        # ===が見つからない場合は元の文字列をそのまま返す
        return input_string.strip()


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


@app.route('/mutate3',methods=['POST'])
def mutate_text_3():
    try:
        req=request.json
        window_id = req.get("clientId")
        raw_contents = req.get("targetText") # "。"で分割し、文字列の配列に変換
        text_index = req.get("mutatedLength")
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
                        "content": prompts[int(window_id)]+"\n**ただし、入力文が書きかけや空など、誤りだと思われる場合は余計なものは付け足さず、そのまま入力文を返すこと。**" + "¥n ================ ¥n" + raw_content,
                    }
                ],
                model="gpt-4-turbo",
            )
            mutated_text = chat_completion.choices[0].message.content.strip()
            mutated_texts.append(mutated_text)

    response = {
        'result': {
            'mutatedText': mutated_texts,  # 変換後のテキストの配列
            'mutatedLength': text_index  # テキストのインデックスの配列
        }
    }

    return jsonify(response), 200

@app.route('/mutate4', methods=['POST'])
def mutate_text_4():
    try:
        req=request.json
        window_id = req.get("clientId")
        raw_contents = req.get("targetText") # "。"で分割し、文字列の配列に変換
        text_index = req.get("mutatedLength")
    except:
        return flask.jsonify({
            "status":"invalid param"
            })

    # 分割された文字列の配列に対してテキスト変換処理を行う
    mutated_texts = []
    for raw_content in raw_contents:
        if raw_content.strip() and (raw_content.endswith("。") or raw_content.endswith("．")):  # 空の文字列をスキップ
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompts[int(window_id)]+ "¥n ================ ¥n" + raw_content,
                    }
                ],
                model="gpt-4-turbo",
            )
            mutated_text = chat_completion.choices[0].message.content.strip()
            mutated_texts.append(process_string(mutated_text))

    response = {
        'result': {
            'mutatedText': mutated_texts,  # 変換後のテキストの配列
            'mutatedLength': text_index  # テキストのインデックスの配列
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