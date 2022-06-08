from flask import Flask, request
import utils.crawling_dataV2 as crawling
import utils.preprocessing_data as preprocessing
import utils.modelling as modelling

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, This is Digital Marketing Application!"

@app.route("/buzzerfinder", methods=['POST'])
def getData():
    keyword = request.form.get('keyword')

    #from crawling_dataV2.py
    data = crawling.get_data(keyword)

    #from preprocessing.py
    clean_data = preprocessing.preprocessing(data)

    #from modelling.py
    result = modelling.modelling(clean_data)

    result - result[:10]

    return {
        "data": [
            result
        ]
    }

if __name__ == '__main__':
  app.run(debug=True)    