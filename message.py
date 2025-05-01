# message.py
# Message class: sending messages between users, employers, and admin



class Message:
    def __init__(self, sender_email, receiver_email, content):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.content = content

    def display(self):
        return f"From: {self.sender_email}\nTo: {self.receiver_email}\nMessage: {self.content}"


def save_messages_to_file():
    return None


def load_messages_from_file():
    return None
