# Django imports

from django.shortcuts import redirect, render

# rest_framework imports

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# model and other related imports

# ----------------------------------machine_learning imports

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ---------------------------------Python inbuilt, ownfile and some other libs import

import re
import json
import pandas as pd
from api.assets.sentiment_app import clean_text, CleanTokenize
from ..models import Sentiment
from .serializers import SentimentSerializer

#-------------------------------------------------------------#

# Creating an APIVIew
class SentimentAPI(APIView):
    def get(self, request):
        try:
            predict = Sentiment.objects.all()
            predict_serialiser = SentimentSerializer(predict,many=True)
            return Response(data=predict_serialiser.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            max_len = 150
            trunc_type = 'post'
            padding = 'post'
            model = load_model('api/res/model/sentiment_version_2.h5')
            print('Model loaded successfully.')
            with open('api/res/assets/tokenizer_version_2.json') as t:
                datas = json.load(t)
                tokenizer = tokenizer_from_json(datas)
                print('Tokenizer loaded successfully.')
            cleaned_review = CleanTokenize([request.data.get('review')])
            test_sequences = tokenizer.texts_to_sequences(cleaned_review)
            test_padded = pad_sequences(test_sequences, maxlen=max_len, padding=padding)
            prob = model.predict(test_padded)
            if prob[0][0] <= 0.2:
                result = 1
            elif prob[0][0] <= 0.4:
                result = 2
            elif prob[0][0] <= 0.6:
                result = 3
            elif prob[0][0] <= 0.8:
                result = 4
            else:
                result = 5
            # Saving data to db Model
            result_data = {
                'review': request.data.get('review'),
                'rating': result
            }
            serializer = SentimentSerializer(data=result_data)
            if serializer.is_valid():
                serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as V:
            return Response(data=V, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        pass