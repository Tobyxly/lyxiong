
from __future__ import print_function
import httplib2
import os
import json
from apiclient import errors
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import MySQLdb
import re

conn = MySQLdb.connect(user='root', password='luyuan', database='lyxiong', charset='utf8')
cursor = conn.cursor()

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None



def emoji_filter():  #正则过滤表情
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Gmail API Python Quickstart'

    emoji_pattern = re.compile("["
                               "\U0001F600-\U0001F64F"  # emoticons
                               "\U0001F300-\U0001F5FF"  # symbols & pictographs
                               "\U0001F680-\U0001F6FF"  # transport & map symbols
                               "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    # if not credentials or credentials.invalid:
    #     flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    #     flow.user_agent = APPLICATION_NAME
    #     if flags:
    #         credentials = tools.run_flow(flow, store, flags)
    #     else: # Needed only for compatibility with Python 2.6
    #         credentials = tools.run(flow, store)
    #     print('Storing credentials to ' + credential_path)
    return credentials

def ListThreadsWithLabels(service,user_id,label_ids=[]):
    try:
        response = service.users().threads().list(userId = user_id,labelIds = label_ids).execute()
        threads = []
        if 'threads' in response:
            threads.extend(response['threads'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().threads().list(userId = user_id,labelIds = label_ids,pageToken = page_token).execute()
            threads.extend(response['threads'])

        return threads
    except errors.HttpError as error:
        print('An error occurred: %s' %error)


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def GetMessage(service,user_id,msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id = msg_id).execute()
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' %error)


def GetService():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service


def GetMsgId(): #获取label为'INBOX'下每个thread_id所对应的多个msg_id
    service = GetService();
    threads = ListThreadsWithLabels(service, 'me', ['INBOX'])
    list_threads  =[]
    for item in threads:
        list_threads.append(item['id'])  #获取label为'INBOX'下每个thread id
    list_message = ListMessagesWithLabels(service, 'me', ['INBOX'])  #获取label为'INBOX'下每个thread_id和msg_id
    dict = {}  # 获取label为'INBOX'下每个thread_id所对应的多个msg_id
    for i in list_threads:
        dict[i] = []
        for item in list_message:
            if i == item['threadId']:
                dict[i].append(item['id'])
    return dict


def GetPurposedMessage(): #获取每个thread_id下的message信息，筛选后放入purposed_message字典,以此存入message_list列表
    service = GetService()
    dict = GetMsgId()
    message_list = []
    emoji_pattern = emoji_filter()
    for key in dict:
        for value in dict[key]:
            purposed_message = {}
            message = GetMessage(service, 'me', value)
            purposed_message['msg_id'] = message['id']
            purposed_message['threadId'] = message['threadId']
            purposed_message['content'] = emoji_pattern.sub('', message['snippet'])
            purposed_message['timestamps'] = int(message['internalDate'])
            purposed_message['receiver'] = message['payload']['headers'][0]['value']
            purposed_message['sender'] = message['payload']['headers'][1]['value']
            message_list.append(purposed_message)
    return message_list

def main():
    list_message = GetPurposedMessage()

    #连接数据库，循环写入
    with open('info.txt', 'w') as json_file:
        for item in list_message:     #获取每个thread_id下的message信息，筛选后放入purposed_message字典，并将其以json的形式写入文件
            json_file.write(json.dumps(item, ensure_ascii=False,indent = 6))
            cursor.execute('insert ignore into email_info(thread_id,msg_id,receiver,sender,content,timestamps) values(%s,%s,%s,%s,%s,%s)',
                           [item['threadId'],item['msg_id'],item['receiver'],item['sender'],item['content'],item['timestamps']])
            conn.commit()
    print('写入完成')

if __name__ == '__main__':
    main()