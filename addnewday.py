from notion import *

f = open("XXXXXXXXXXXX")
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

notion.addNewDailyHabit()