from flask import Flask, request, jsonify, render_template
import models.youtube as youtube
import models.sentiment_analyzer as sa
from urllib.parse import urlparse


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    summary = None
    comments = []
    video_url = ""
    video_id = ""
    video_comments = None

    if request.method == 'POST':
        video_url = request.form.get('site_url')
        domain = urlparse(video_url).hostname

        match domain:
            case "www.youtube.com":
                video_id = video_url.split("v=")[1]
                video_comments = youtube.get_comments(video_id)
            case "www.instagram.com":
                messages.append("Instagram!")
                messages.append("Todo")
            case _:
                messages.append("Site not supported!")

        if video_comments:
            predictions = sa.predict_sentiment(video_comments)

            postive_cnt = predictions.count("Positive")
            negative_cnt = predictions.count("Negative")
            neutral_cnt = predictions.count("Neutral")

            summary = {
                "positive": postive_cnt,
                "negative": negative_cnt,
                "neutral": neutral_cnt,
                "total_comments": len(video_comments),
                "ratio": round((postive_cnt / len(video_comments)) * 100, 2)
            }
            comments = list(zip(video_comments, predictions))

    
    return render_template(
        'index.html', 
        summary=summary, 
        comments=comments, 
        video_url=video_url, 
        video_id=video_id,
        messages=messages
    )

if __name__ == '__main__':
    app.run(debug=True)