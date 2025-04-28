# message.py
# Message class: sending messages between users, employers, and admin



class Message:
    def __init__(self, sender_email, receiver_email, content):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.content = content

