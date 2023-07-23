#importing libraries
from flask import Flask ,render_template,request
from joblib import load
import pandas as pd
app = Flask(__name__)

# Loading the model using joblib
model=load(open('./static/InfantHealthRiskModel.joblib', 'rb'))

#Mapping the Risk
Risk = {1:'Normal',2:'Moderate Risk',3:'High Risk'}

# HAndling the requests made to root page   
@app.route("/",methods=["GET","POST"])


def index():
    if request.method=="POST":
        print('The form data: ', request.form)
        data = dict(map(lambda item: (item[0],[float(item[1])]),request.form.items()))
        print('Transformed data: ', data)
        df = pd.DataFrame(data=data)
        y_label=model.predict(df)
        print('Prediction: ',y_label)
        prediction=y_label[0]

        cleanData = dict(map(lambda item: (item[0],float(item[1][0])),data.items()))
        return render_template("prediction.html", data=cleanData, prediction=Risk[prediction])
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)