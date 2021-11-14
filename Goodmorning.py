import email
import datetime
import imaplib
import re
#from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


import requests, json

class ProductiveMorning:
    def __init__(self, city, startOfDay=None):
        self.startOfDay = startOfDay
        self.ToDoList = []
        self.city = city
        self.API_KEY = 'de808bb34559ff7fccbbea34ab70e065'
        self.tempature = None
        self.report = None
        self.today = datetime.date.today()
        self.Deadlines = {}
        self.unsername = None
        self.code = None

    def getSchedule(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])



    def setUpEmail(self,username,code):
        self.username = username
        self.code = code

    def getEmails(self):
        '''
        This function uses a provided email name and passcode to display all of the users unread emails.
        '''
        gmail_host = 'imap.gmail.com'
        mail = imaplib.IMAP4_SSL(gmail_host)
        mail.login(self.username, self.code)
        mail.select()
        typ,data = mail.search(None, 'UNSEEN')
        if data[0].split() == []:
            print('Whoa- you have no unread emails. Hawt damn!')
        else:
            print('Here are all of your emails! Enjoy... ')
            for num in data[0].split():
                typ, data = mail.fetch(num, '(RFC822)')
                txt = data[0][1]
                subject = "Subject: .*[\\r\n]".encode('utf-8')
                sender = "From:.*>".encode('utf-8')
                match_sub = re.search(subject,txt)
                match_send = re.search(sender,txt)
                subject = match_sub.group()[9:-2].decode("utf-8")
                sender  = match_send.group()[6::].decode("utf-8")
                print(sender,subject)


    def setDeadline(self):
        assigment = input('what is the upcoming deadline?')
        deadline = input('when is it due? (NOTE: PLEASE USE YYYY-MM-DD)')
        if assignment not in self.Deadlines.keys():
            self.Deadlines[assignment] = deadline
        else:
            print(assigment + 'already has a set deadline of' + str(self.Deadlines[assignment]))


    def getWeather(self):
        # this function uses an AP to access the weather for the give city
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        URL = BASE_URL + "q=" + self.city + "&appid=" + self.API_KEY
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            self.temperature = main['temp']
            self.report = data['weather']
            self.temperature = round((self.temperature-273.15)*9/5+32)
        print('Todays weather is ' + self.report[0]['description'] + '.')
        print('The tempature is ' + str(self.temperature) + ' deegrees fareinheit.')

    def getToDoList(self):
        # this function presents the current to-do list for a user to view
        print('your to-do list is...')
        for x in range(1, len(self.ToDoList) + 1):
            print(str(x) + ': ' + self.ToDoList[x - 1])

    def addToDoList(self, toDo):
        # this function will add one activity to the users to-do list.
        # if the item is already in the list it will inform the user.
        if toDo not in self.ToDoList:
            self.ToDoList.append(toDo)
            print(toDo + ' has been successfully added to your to do list!')
        else:
            print(toDo + ' is already included in todays to do list')

    def removeToDoList(self, done):
        # this function removes activites from an existing to-do list
        # if the activity is not on the to-do list, all activities are printed for the user to see
        # the user is given the option to select any activity on the lsit or state none
        try:
            self.ToDoList.remove(done)
            print(done + ' has been removed!Good work!')
        except ValueError:
            print('Task not in list. What is the number of the task you meant?')
            for x in range(1, len(self.ToDoList) + 1):
                print(str(x) + ': ' + self.ToDoList[x - 1])
            print(str(len(self.ToDoList) + 1) + ': None')
            task = int(input())
            if task != len(self.ToDoList) + 1:
                done = self.ToDoList[task - 1]
                self.ToDoList.remove(done)
                print(done + ' has been removed!Good work!')
            else:
                print('Nothing has been removed from your list')

    def greeting(self):
        today = datetime.date.today()
        print('First off- Good morning! Todays date is ' + str(self.today) + '.')
        self.getWeather()
        print('\n')
        self.getToDoList()
        print('\n')
        self.getEmails()
        print('\n')
        self.getSchedule()
