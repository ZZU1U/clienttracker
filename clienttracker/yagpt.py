import requests

request = {
  "model": "string",

  "generationOptions": {
    "partialResults": True,
    "temperature": 0.5,
    "maxTokens": 300,
  },


  "instructionText": "напиши текст для поздравления друга",

  "requestText": "мой друг добрый, ему будет 12 лет, он любит мультфильм тачки",
}


print(requests.post(url='https://llm.api.cloud.yandex.net/llm/v1alpha/instruct', json=str(request)))
