import requests
import json
import datetime
from time import sleep

month_dict = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}



class NotionReader:
    def __init__(self, telegram_api, telegram_chat, phone, token, databaseId,
                 debug = True, notify_user = False) -> None:
        self.debug = debug
        self.notify_user = notify_user
        self.token = token
        self.databaseId = databaseId
        self.URL = f"https://api.telegram.org/bot{telegram_api}/sendMessage?chat_id={telegram_chat}&text="


    def getCurrentDate(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def readNotionDb(self) -> dict:
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        readUrl = f"https://api.notion.com/v1/databases/{self.databaseId}/query"
        res = requests.post(readUrl, headers=headers)
        data = res.json()

        return data


    def createDbElement(self, name: str, dueDate: str) -> str:
        updateData = {
            "parent": {
                "database_id": self.databaseId
            },
            "properties": {
                "Sport": {
                    "checkbox": False,
                },
                "Meds A": {
                    "checkbox": False,
                },
                "Journal": {
                    "checkbox": False,
                },
                "V": {
                    "checkbox": False,
                },
                "W": {
                    "checkbox": False,
                },
                "Meds M": {
                    "checkbox": False,
                },
                "8h sleep": {
                    "checkbox": False,
                },
                "2h Stand": {
                    "checkbox": False,
                },
                "Title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                            "content": name
                            }
                        }
                    ]
                },
                "Date": {    
                    "date": {
                    "start": dueDate
                    }
                }
            }
        }
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": "Bearer " + self.token,
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json"
        }

        response = requests.post(url, json=updateData, headers=headers)

        return json.loads(response.text)
    

    def addNewDailyHabit(self) -> None:
        notionData = self.readNotionDb()
        print(self.createDbElement("Day " + str(len(notionData['results']) + 1), self.getCurrentDate()))


    def notifyDailyProgress(self) -> None:
        notionData = self.readNotionDb()
        for data in notionData["results"]:
            last_entry =  data['properties']
            if last_entry['Date']['date']['start'] == self.getCurrentDate():
                self.getDailyProgress(last_entry)


    def getDailyProgress(self, data: dict) -> dict:
        open_tasks = []
        for property in data.keys():
            if property != 'Date' and  property != 'Title':
                if data[property]['type'] == 'checkbox':
                    status = data[property]['checkbox']
                    if status == False:
                        open_tasks.append(property)
        
        if len(open_tasks) > 0:
            self.notifyUser(open_tasks)


    def notifyUser(self, open_tasks: list):
        statusMsg = 'There are still open tasks:'
        for open_task in open_tasks:
            statusMsg += f'\n - {open_task}'
        
        requests.get(self.URL+statusMsg).json()


if __name__ == "__main__":
    f = open("XXXXXXXXXXXXXX")
    data = json.load(f)
    f.close()
    phone = ''

    notion = NotionReader(  data['telegram']['api_token'],
                            data['telegram']['chat_id'],
                            phone,
                            data['notion']['token'],
                            data['notion']['database_id'],
                            True, 
                            True
                        )

    notion.updateNotionDeadlines()
