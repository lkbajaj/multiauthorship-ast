import requests

# Load token
with open('ads-key.txt', 'r') as file:
    token = file.read().strip()

headers = {'Authorization': f'Bearer {token}'}

# A deliberately minimal query
url = 'https://api.adsabs.harvard.edu/v1/search/query'
params = {
    'q': 'year:2020 AND bibstem:ApJ',
    'fl': 'bibcode',
    'rows': 1
}

response = requests.get(url, headers=headers, params=params)

print(f"Status Code: {response.status_code}")
print(f"Reason: {response.reason}")
print("Response Text (first 300 chars):\n", response.text[:300])