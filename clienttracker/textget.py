import requests
r = requests.post(
    "https://api.deepai.org/api/text-generator",
    data={
        'text': 'YOUR_TEXT_URL',
    },
    headers={'api-key': 'YOUR_API_KEY'}
)
print(r.json())
