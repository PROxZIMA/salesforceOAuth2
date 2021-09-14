# salesforceOAuth2

A django project which integrates Salesforce using its REST API to fetch the list of Users, Accounts, and Contacts from salesforce and store it in the database.

1) To run the application use: `python manage.py runserver localhost:8000` as `localhost:8000` is used as callback url for user authorization

2) `settings.SF_CONSUMER_KEY` and `settings.SF_CONSUMER_SECRET` are already there in settings. If new API is created the you must edit above keys

3) This application uses [`OAuth 2.0 Web Server Flow`](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_web_server_flow.htm&type=5) to authorize user.
