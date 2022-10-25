from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
import pickle


#loading model
model=pickle.load(open(r'C:\Users\claud\Desktop\ds\ds_producao\api\rossmann\model\xgb_tuned.pkl','rb'))

#initializa API
app=Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])

def rossmann_predict():
    test_jason=request.get_json()
    
    if test_jason:
        if isinstance(test_jason, dict):  # para linha unica      
      	    test_raw=pd.DataFrame (test_jason, index=[0]) 
        else:#para multiplas linhas
            test_raw=pd.DataFrame (test_jason,columns=test_jason[0].keys())
            
        #instatiate Rossmann class
        pipeline = Rossmann()
        #data cleaning
        df1=pipeline.data_cleaning(test_raw)
        
        #feature engineering
        df2=pipeline.feature_engineering(df1)
        
        #data preparation
        df3=pipeline.data_preparation(df2)
        
        #prediction
        df_response=pipeline.get_prediction(model,test_raw,df3)
        
        return df_response
        
    else:
        return Response ('{}', status =200, mimetype='applycation/json')

if __name__ == '__main__':
    app.run( '192.168.0.112:5000' )