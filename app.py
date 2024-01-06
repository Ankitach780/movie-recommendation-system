from flask import Flask, render_template,request
import requests
import joblib
app=Flask(__name__)
new=joblib.load(open("movies.pkl",'rb'))
similarity=joblib.load(open("similarity.pkl",'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url,timeout=10)
    if response.status_code == 200:
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500" + poster_path
            return full_path
        else:
            return "https://image.tmdb.org/t/p/w500/nby91GNVXQAv1NmKvqlpEEdhcMQ.jpg"  
    else:
        return "URL_TO_ERROR_IMAGE"

@app.route('/',methods=['Get','Post'])
def index():
    movie_ids = list(new['movie_id'].values)
    return render_template('index.html',
                            movie_title=list(new['title'].values),
                            image=list(fetch_poster(movie_id) for movie_id in movie_ids[:15]))
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movie',methods=['post'])
def recommended():
    user_input = request.form.get('user_input')
    index = new[new['title'] == user_input].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    data=[]

    for i in distances[1:6]:
        item=[]
        movie_id =  new.iloc[i[0]].movie_id
        item.append(fetch_poster(movie_id))
        item.append(new.iloc[i[0]].title)
        data.append(item)
    return render_template('recommend.html',data=data)
    
if __name__=='__main__':
    app.run(debug=True)
