import requests

def search_google_cse(query, num_pages=3):
    api_key = "AIzaSyANdUjucaFBHFnJWdzKVgSf3HNXi-A2hI0"
    cse_id = "70cea2d6bd6dc4340"
    search_url = "https://www.googleapis.com/customsearch/v1"

    for page in range(1, num_pages + 1):
        start_index = (page - 1) * 10 + 1
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query,
            'start': start_index
        }

        response = requests.get(search_url, params=params)
        results = response.json()

        print(f"Page {page}:")
        for item in results.get("items", []):
            title = item.get("title")
            link = item.get("link")
            print(f"Title: {title}\nURL: {link}\n")

# Example usage
search_query = '(startup OR company) AND (funding OR investment OR "raised funds" OR "secured financing" OR "seed round" or "pre-seed round" or "round A") AND ($ OR USD OR million OR billion) AND 2024 AND march'

search_google_cse(search_query)
