import csv
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    params = {
        'grant_type': 'client_credentials',
        'client_id': SNOVIO_CLIENT_ID,
        'client_secret': SNOVIO_CLIENT_SECRET
    }
    response = requests.post('https://api.snov.io/v1/oauth/access_token', data=params)
    return response.json()['access_token']

def get_decision_makers(company, website):
    token = get_access_token()
    params = {
        'access_token': token,
        'domain': website,
        'type': 'all',
        'limit': 3,
        'lastId': 0,
        'positions[]': ['CEO','Head of sales','CBDO','Sales lead','Head of Customer','Chief revenue officer','Director of sales','Head of Business Development','Director of business development','Chief sales officer','Chief of Sales', 'Chief of business development', 'Chief business development officer','Marketing Director','CMO','Chief Marketing Officer', 'Head of Marketing', 'Head of Lead Generation']
    }
    response = requests.get('https://api.snov.io/v2/domain-emails-with-info', params=params)
    emails = response.json().get('emails', [])
    try:
        if not emails:
            params = {
                'access_token': token,
                'domain': website,
                'type': 'generic',
                'limit': 3,
                'lastId': 0,
            }
            response = requests.get('https://api.snov.io/v2/domain-emails-with-info', params=params)
            emails = response.json().get('emails', [])
    except NameError:
        return []
    return [{'Company': company, 'Website': website, 'Type': email.get('type', ''), 'FirstName': email.get('firstName', ''), 'LastName': email.get('lastName', ''), 'Email': email.get('email', ''), 'sourcePage': email.get('sourcePage', ''), 'Position': email.get('position', '')} for email in emails if email.get("status") == "verified"]

def main():
    with open('D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\ClutchCollector\\company_website_test.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        companies_websites = [row for row in reader]

    with open('D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\ClutchCollector\\decision_makers.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Company', 'Website', 'Type', 'FirstName', 'LastName', 'Position', 'Email', 'sourcePage'])
        writer.writeheader()

        for company, website in companies_websites:
            decision_makers = get_decision_makers(company, website)
            if decision_makers:
                writer.writerows(decision_makers)
            else:
                writer.writerow({'Company': company, 'Website': website})

if __name__ == "__main__":
    main()
