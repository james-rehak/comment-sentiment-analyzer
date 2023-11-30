from flask import Flask, request, jsonify, render_template
import models.youtube as youtube
import models.sentiment_analyzer as sa


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    comments = []
    video_url = ""
    video_id = ""

    if request.method == 'POST':
        # todo make switch for different sites
        video_url = request.form.get('site_url')
        video_id = video_url.split("v=")[1]

        video_comments = youtube.get_comments(video_id)
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
        print(comments)
    
    return render_template(
        'index.html', 
        summary=summary, 
        comments=comments, 
        video_url=video_url, 
        video_id=video_id
    )

if __name__ == '__main__':
    app.run(debug=True)