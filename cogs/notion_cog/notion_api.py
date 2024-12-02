import requests

class NotionAPI:
    def __init__(self, token, database_id):
        self.token = token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def get_stocks(self):
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['results']
        return None

    def get_page_id_by_name(self, stock_name):
        stocks = self.get_stocks()
        if not stocks:
            return None
        for stock in stocks:
            name = stock['properties']['Name']['title'][0]['text']['content']
            if name == stock_name:
                return stock['id']
        return None

    def update_stock_prices(self, page_id, prices):
        data = {
            "properties": {
                "Open Price": {"number": prices['open']},
                "High Price": {"number": prices['high']},
                "Low Price": {"number": prices['low']},
                "Close Price": {"number": prices['close']}
            }
        }
        url = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.patch(url, headers=self.headers, json=data)
        return response.status_code == 200

    def add_stock(self, stock_name):
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": stock_name}}]
                },
                "Open Price": {"number": None},
                "High Price": {"number": None},
                "Low Price": {"number": None},
                "Close Price": {"number": None}
            }
        }
        url = "https://api.notion.com/v1/pages"
        response = requests.post(url, headers=self.headers, json=data)
        return response.status_code == 200
