import requests
from flask import Flask, request, jsonify, render_template
from transformers import pipeline

# Flask 애플리케이션 생성
app = Flask(__name__)

# Summarization 모델 로드
summarizer = pipeline("summarization")

# Google API 키 및 검색 엔진 ID
GOOGLE_API_KEY = "AIzaSyBAXTnNVndwBz8MctOqYivP7etqeOmFWNA"
SEARCH_ENGINE_ID = "36e2c0f8098af4c3e"

# 지식 베이스 저장
data_store = {}

@app.route("/")
def home():
    """메인 페이지 렌더링"""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """사용자 질문 처리 및 응답"""
    user_input = request.get_json().get("prompt", "").lower()

    # 데이터 스토어에서 응답 검색
    if user_input in data_store:
        return jsonify({"response": data_store[user_input]})

    return jsonify({"response": "아직 학습되지 않은 질문입니다. 다시 검색해주세요."})

@app.route("/api/search_learn", methods=["POST"])
def search_and_learn():
    """Google 검색 및 요약"""
    query = request.get_json().get("query", "")

    if not query:
        return jsonify({"error": "검색어를 입력하세요."}), 400

    # Google Custom Search API 호출
    try:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query
        }
        response = requests.get(search_url, params=params)
        search_results = response.json()

        # 검색 결과 확인
        items = search_results.get("items", [])
        if not items:
            return jsonify({"error": "검색 결과가 없습니다."}), 404

        # 첫 번째 검색 결과 가져오기
        top_result = items[0]
        title = top_result.get("title")
        snippet = top_result.get("snippet")
        link = top_result.get("link")

        # 요약 생성
        summary = summarizer(snippet, max_length=50, min_length=25, do_sample=False)
        summarized_text = summary[0]["summary_text"]

        # 데이터 스토어에 저장
        data_store[query] = {
            "title": title,
            "summary": summarized_text,
            "link": link
        }

        return jsonify({
            "query": query,
            "title": title,
            "snippet": snippet,
            "link": link,
            "summary": summarized_text,
            "message": "검색 결과를 학습했습니다."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
