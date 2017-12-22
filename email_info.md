## 通过GMAIL接口获取邮件信息(PYTHON)##

##### 其中用到了GMAIL提供的三种数据结构：Threads, Messages, Labels#####

#### 1. labels: ####

##### 就是邮箱中定义的标签,有INBOX,SPAM,SENT,DRAFT等各种类型，我们只需要查看收件箱的内容，此处只用到INXOB即可。#####

#### 2. Messages:####

##### Message就是指一条信息，通过查看它的属性和操作，可以知道获得了这个对象你可以获得的相关信息和进行的操作#####

##### 	2.1 #### 
####Messages对象提供了list方法，返回一个字典包含了两个属性#####

##### 		id: 邮件的id号 threadId:此邮件所对应的thread id号#####


##### Gmail API官网提供获取不同label下上述属性的方法：#####

``````python
#user_id为获取信息的邮箱账户,service为授权的Gmail API服务
def ListMessagesWithLabels(service, user_id, label_ids=[]):
``````



##### 2.2 Messages对象提供了get方法, 返回了多个属性如 message id, internalDate(时间戳)，snippet, payload字典(其中包含header属性,用于获取邮件的收发人)#####


``````python
def GetMessage(service,user_id,msg_id):
``````



#### 3. Threads:####

##### Threads是指会话的一次(和另外一个账户进行会话的过程)，每一个Threads是可以有多个Messages的#####

##### 	Threads对象提供了list方法，返回了一个字典包含了三个属性#####

##### 		id: thread的id号		snippet:邮件信息的一部分		#####

##### 		historyId:修改此线程的最后一个历史记录的ID #####

##### Gmail API官网提供获取不同label下上述属性的方法：#####

`````` python
def ListThreadsWithLabels(service, user_id, label_ids=[]):
``````



##### 通过以上方法我们可以获得指定邮箱中每个thread下的邮件信息：#####

##### 1. 获取label为'INBOX'下每个thread id#####

##### 2.获取label为'INBOX'下每个thread_id和msg_id#####

##### 3.获取label为'INBOX'下每个thread_id所对应的多个msg_id

##### 4.循环获取每个thread_id下的message信息，筛选后放入purposed_message字典,依次存入message_list列表

###### 若需添加或更改message信息，只需更改下面部分代码获取想要的message属性即可。######

``````python
            purposed_message = {}
            message = GetMessage(service, 'me', value)
            purposed_message['msg_id'] = message['id']
            purposed_message['threadId'] = message['threadId']
            purposed_message['content'] = emoji_pattern.sub('', message['snippet'])#用了一个正则表达式过滤content中的表情
            purposed_message['timestamps'] = int(message['internalDate'])
            purposed_message['receiver'] = message['payload']['headers'][0]['value']
            purposed_message['sender'] = message['payload']['headers'][1]['value']
            message_list.append(purposed_message)

``````











  







