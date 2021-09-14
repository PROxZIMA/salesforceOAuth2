import requests
import urllib

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from salesforceApp.models import AccountData, UserData, ContactData
import salesforceApp.utils as utils


# Create your views here.
def index(request):
    return render(request, 'index.html')


def viewData(request):
    utils.insert_data(request)

    if request.method == 'GET':
        data = {
            'users_data': [UserData.objects.all(), UserData._meta.get_fields()[1:]],
            'accounts_data': [AccountData.objects.all(), AccountData._meta.get_fields()[1:]],
            'contact_data': [ContactData.objects.all(), ContactData._meta.get_fields()[1:]],
        }

        return render(request, 'data.html', context=data)


def oauth2(request):
    '''
    View for initiating OAuth with Salesforce
    '''
    url = 'https://login.salesforce.com/services/oauth2/authorize'

    args = {
        'client_id': settings.SF_CONSUMER_KEY,
        'redirect_uri': settings.OAUTH_REDIRECT_URI,
        'response_type': 'code',
        'scope': settings.SCOPES,
    }

    response = redirect(f'{url}?{urllib.parse.urlencode(args)}')

    return response


def oauth2_callback(request):
    '''
    View behind the callback URI provided to Salesforce
    '''
    code = request.GET.get('code')

    url = 'https://login.salesforce.com/services/oauth2/token'

    if not code:
        return redirect('index')

    data = {
        'client_id': settings.SF_CONSUMER_KEY,
        'client_secret': settings.SF_CONSUMER_SECRET,
        'redirect_uri': settings.OAUTH_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': code,
    }

    # Getting access token
    response = requests.post(
        url,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=data)

    user = utils.Oauth2User(response.json())

    login(request, user)

    return redirect(settings.LOGIN_REDIRECT_URL)