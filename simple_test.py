import requests
from dotenv import load_dotenv
load_dotenv()
import os

print('Testing Product Hunt API...')
query = '''
query TodayPosts($perPage: Int!) {
  posts(order: RANKING, postedAfter: null, postedBefore: null, first: $perPage) {
    edges {
      node {
        name
        tagline
        url
        votesCount
      }
    }
  }
}
'''
headers = {"Authorization": f"Bearer {os.getenv('PH_TOKEN')}", "Content-Type": "application/json"}
try:
    res = requests.post(
        "https://api.producthunt.com/v2/api/graphql",
        json={"query": query, "variables": {"perPage": 3}},
        headers=headers,
        timeout=30
    )
    print("Response status:", res.status_code)
    data = res.json().get("data", {}).get("posts", {}).get("edges", [])
    print(f"Found {len(data)} products")
    if data:
        for i, p in enumerate(data[:2]):
            print(f"{i+1}. {p['node']['name']} - {p['node']['tagline']}")
except Exception as e:
    print(f"Error: {e}")
