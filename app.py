from dotenv import load_dotenv
load_dotenv()


###
# 画面に入力フォームを1つ用意し、入力フォームから送信したテキストをLangChainを使ってLLMにプロンプトとして渡し、回答結果が画面上に表示されるようにしてください。
#ラジオボタンでLLMに振る舞わせる専門家の種類を選択できるようにし、料理を選択した場合は料理の領域の専門家として、また育児を選択した場合は育児の領域の専門家としてLLMに振る舞わせるよう、選択値に応じてLLMに渡すプロンプトのシステムメッセージを変えてください。また用意する専門家の種類はご自身で考えてください。
#「入力テキスト」と「ラジオボタンでの選択値」を引数として受け取り、LLMからの回答を戻り値として返す関数を定義し、利用してください。
#Webアプリの概要や操作方法をユーザーに明示するためのテキストを表示してください。
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
def get_expert_response(input_text, expert_type):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    # プロンプトテンプレートの定義
    if expert_type == "料理":
        system_message = "あなたは料理の専門家です。"
    elif expert_type == "育児":
        system_message = "あなたは育児の専門家です。"
    else:
        system_message = "あなたは一般的なアドバイザーです。"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input_text}")
    ])

    # チェーンの作成
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # 入力テキストを使ってLLMからの応答を取得
    response = chain.run(input_text=input_text)
    
    return response
# Streamlitアプリの設定
st.set_page_config(page_title="専門家相談アプリ", layout="wide")
st.title("専門家相談アプリ") 
st.write("""
このアプリでは、専門家に相談することができます。以下の手順でご利用ください。
1. 専門家の種類を選択してください。
2. 質問を入力してください。
3. 「送信」ボタンをクリックしてください。
""")

# 入力フォームの作成
with st.form(key="expert_form"):
    expert_type = st.radio("専門家の種類を選択してください:", ["料理", "育児"])
    user_input = st.text_input(label="質問を入力してください:")
    submit_button = st.form_submit_button("送信")

if submit_button:
    response = get_expert_response(user_input, expert_type)
    st.write("専門家の回答:")
    st.write(response)