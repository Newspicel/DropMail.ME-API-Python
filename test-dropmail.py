import dropmail

dropmailmanager = dropmail.DropMailManager(deamon=False)

session = dropmailmanager.createMail(lambda x: print(x))
print(session)