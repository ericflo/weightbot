import datetime
import httplib2
import urllib

from xml.etree import ElementTree

class WeightBotException(Exception):
    pass

LOGIN_URL = 'https://weightbot.com/account/login'
HOME_URL = 'https://weightbot.com/'
EXPORT_URL = 'https://weightbot.com/export'

def _sanitize_html(html):
    # ElementTree barfs on things like &copy; so we have to strip them.
    return html.replace('&copy;', '')

def parse_date(date):
    year, month, day = date.split('-')
    return datetime.date(year=int(year), month=int(month), day=int(day))

class WeightBot(object):
    def __init__(self, email, password, httplib2_kwargs={}):
        self.email = email
        self.password = password 
        self.http = httplib2.Http(**httplib2_kwargs)
    
    def get_auth_token(self, data):
        html = _sanitize_html(data)
        tree = ElementTree.fromstring(html)
        authenticity_token = None
        for item in tree.findall('.//input'):
            name = item.get('name')
            if name == 'authenticity_token':
                authenticity_token = item.get('value')
                break
        return authenticity_token
    
    def get_csv_data(self):
        resp, content = self.http.request(LOGIN_URL, 'GET')
        auth_token = self.get_auth_token(content)
        if auth_token is None:
            raise WeightBotException('Could not get authenticity data '
                'from %s' % (LOGIN_URL,))
        body = {
            'email': self.email,
            'password': self.password,
            'authenticity_token': auth_token,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': resp['set-cookie'],
        }
        resp, content = self.http.request(LOGIN_URL, 'POST', headers=headers,
            body=urllib.urlencode(body))
        del headers['Content-Type']
        if 'set-cookie' in resp:
            headers['Cookie'] = resp['set-cookie']
        resp, content = self.http.request(HOME_URL, 'GET', headers=headers)
        if 'set-cookie' in resp:
            headers['Cookie'] = resp['set-cookie']
        auth_token = self.get_auth_token(content)
        if auth_token is None:
            raise WeightBotException('Could not get authenticity data '
                'from %s' % (HOME_URL,))
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        body = {'authenticity_token': auth_token}
        resp, content = self.http.request(EXPORT_URL, 'POST', headers=headers,
            body=urllib.urlencode(body))
        return content
    
    def get_data(self):
        csv_data = self.get_csv_data()
        data = []
        for i, line in enumerate(csv_data.splitlines()):
            if i == 0:
                continue
            try:
                date, kgs, lbs = line.split(',')
            except ValueError:
                continue
            data.append({
                'date': parse_date(date.strip()),
                'kilograms': float(kgs.strip()),
                'pounds': float(lbs.strip()),
            })
        return data