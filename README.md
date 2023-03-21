# Notion Habit Tracker + Telegram Notifications

This Python project creates daily a new row in your habit tracker DB and notifies you `X` times a day about your progress.
 
## Setup

To use this project, you will need to set up a Notion integration and obtain access tokens. You will also need to create a Notion database with the appropriate properties.

1. Clone this repository to your local machine.
3. Obtain your Notion API key and database ID. See [Notion's documentation](https://developers.notion.com/docs/getting-started#step-2-share-a-database-with-your-integration) for more information.
4. Create a `credentials.json` file in the project's root directory with the following structure:
   ```json
    {
        "telegram": {
            "api_token": "XXXXXXX",
            "chat_id": "XXXXXXX",
            "phone": "XXXXXXX"
        },
        "notion": {
            "token": "secret_XXXXXXX",
            "database_id": "XXXXXXX"
        }
    }
    ```
5. Replace all `XXXXXXX` with your own values obtained from Notion, Moodle and Telegram.
6. Adjust the `createDbElement` function in the `notion.py` file with your DB properties if you want different ones.
7. Run the `addnewday.py` once a day to add a new row to your database.
8. Run the `notifyprogress.py` each time you want to get notified.

## Usage

To run the project, simply execute either `addnewday.py` or `notifyprogress.py` file in your environment. I have setup a schedlued task on my homeserver to execute `addnewday.py` once everyday and `notifyprogress.py` three times a day on 10:00 am, 3:00 pm and 8:00 pm.

The program will use requests to to get the necessary information to notify you or create a new entry in the DB with the provided username and password in credentials.json.

The extracted deadlines will be uploaded to a Notion database as a ToDo List with properties for Date, Title, and Course Name.

## Dependencies
- Python 3.6+
- Requests