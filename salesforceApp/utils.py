import requests
from salesforceApp.models import User, UserData, AccountData, ContactData
from django.utils.crypto import get_random_string


def Oauth2User(token_data):
    '''
    Accepts an OAuth token data and retrieves the Salesforce User, creating one if it doesn't exist
    '''
    sf_id_url = token_data.get("id")
    instance_url = token_data.get('instance_url')
    access_token = token_data.get("access_token")

    # Retrieves the Salesforce User
    response = requests.get(sf_id_url, headers={"Authorization": f"Bearer {access_token}"})
    assert (response.status_code == 200), f"Could not retrieve user from Salesforce: {response.reason}"
    salesforce_user = response.json()

    salesforce_id = salesforce_user.get("user_id"),
    email = salesforce_user.get("email")
    password = get_random_string(length=16)

    # Returns an existing user or creates a new one
    user = User.objects.filter(username=salesforce_id).first()
    if not user:
        user = User.objects.create_user(salesforce_id, email, password, instance_url=instance_url, access_token=access_token)
    else:
        user.instance_url = instance_url
        user.access_token = access_token
        user.save()

    return user


def sf_get_data(request, action, params={}):
    '''
    Helper function to make calls to Salesforce REST API.
    Parameters: action (the URL), URL params.
    '''
    user = User.objects.filter(username=request.user.username).values('instance_url', 'access_token')[0]
    instance_url, access_token = user['instance_url'], user['access_token']
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    r = requests.request('GET',
                         instance_url + action,
                         headers=headers,
                         params=params,
                         timeout=30)
    if r.status_code < 300:
        return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))



# Utilities for managing data


def users_data(request):
    '''
    Get user data by calling Salesforce REST API and updates the table
    '''
    users = sf_get_data(request, '/services/data/v52.0/query/',
                        {'q': 'select FIELDS(ALL) from user limit 5'})

    data_list = [
        UserData(
            user_id=data['Id'],
            username=data['Username'],
            name=f"{data['FirstName']} {data['LastName']}",
            company_name=data['CompanyName'],
            city= data['City'],
            phone_no=data['Phone'],
            email=data['Email'],
            isactive=data['IsActive']
        )
        for data in users['records']
    ]

    UserData.objects.all().delete()
    UserData.objects.bulk_create(data_list)


def account_data(request):
    '''
    Get accounts data by calling Salesforce REST API and updates the table
    '''
    accounts = sf_get_data(request, '/services/data/v52.0/query/',
                           {'q': 'select FIELDS(ALL) from account limit 5'})
    data_list = [
        AccountData(
            account_id=data['Id'],
            name=data['Name'],
            photourl=data['PhotoUrl'],
            billingaddress=data['BillingAddress'],
            account_number=data['AccountNumber']
        )
        for data in accounts['records']
    ]

    AccountData.objects.all().delete()
    AccountData.objects.bulk_create(data_list)


#filtering contact data


def contact_data(request):
    '''
    Get contacts data by calling Salesforce REST API and updates the table
    '''
    contacts = sf_get_data(request, '/services/data/v52.0/query/',
                           {'q': 'select FIELDS(ALL) from contact limit 5'})
    data_list = [
        ContactData(
            contact_id=data['Id'],
            accountid=data['AccountId'],
            name=data['Name'],
            mailingstreet=data['MailingStreet'],
            phone_no=data['Phone'],
            birth_day=data['Birthdate'],
            lead_source=data['LeadSource'],
            email=data['Email'],
            department=data['Department'],
            photourl=data['PhotoUrl']
        )
        for data in contacts['records']
    ]

    ContactData.objects.all().delete()
    ContactData.objects.bulk_create(data_list)


def insert_data(request):
    '''
    Helper function to fetch and save Users, Accounts, and Contacts data
    '''
    users_data(request)
    account_data(request)
    contact_data(request)