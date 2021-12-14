import uuid
import requests
import threading
import time

class DropMailManager:

    def __init__(self, deamon=True):
        self.TOKEN = str(uuid.uuid4())
        self.MAILCONSUMERS = {}
        self.__checkMailsThread = threading.Thread(target=self.__autoMailsCheck, daemon=deamon)
        self.__checkMailsThread.start()
        self.__deamon = deamon

    def __autoMailsCheck(self):
        self.checkMails()
        time.sleep(1)

        self.__checkMailsThread = threading.Thread(target=self.__autoMailsCheck, daemon=self.__deamon)
        self.__checkMailsThread.start()

        
    def checkMails(self):
        r = requests.get("https://dropmail.me/api/graphql/" + self.TOKEN + "?query=query%20%7Bsessions%20%7Bid%2C%20expiresAt%2C%20mails%20%7BrawSize%2C%20fromAddr%2C%20toAddr%2C%20downloadUrl%2C%20text%2C%20headerSubject%7D%7D%7D")
        for session in r.json().get("data").get("sessions"):
            for mail in session.get("mails"):
                id = session.get("id")
                if id in self.MAILCONSUMERS:
                    self.MAILCONSUMERS[id](mail)
        
        
    def createMail(self, mailConsumer):
        r = requests.get("https://dropmail.me/api/graphql/"+ self.TOKEN+"?query=mutation%20%7BintroduceSession%20%7Bid%2C%20expiresAt%2C%20addresses%20%7Baddress%7D%7D%7D")
        introduceSession = r.json().get("data").get("introduceSession")
        id = introduceSession.get("id")
        self.MAILCONSUMERS[id] = mailConsumer
        return {"id": id, "address": introduceSession.get("addresses")[0].get("address")}

    def deleteMail(self, id):
        del self.MAILCONSUMERS[id]

