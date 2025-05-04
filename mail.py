import os
import random
import string
import time
import telebot
from telebot import types

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class FakeEmailBot:
    def __init__(self):
        clear_screen()
        print("Telegram Fake Email Bot Setup")
        print("----------------------------")
        self.token = input("Please enter your Telegram bot token: ")
        self.bot = telebot.TeleBot(self.token)
        self.user_emails = {}  # Stores user IDs and their fake emails
        self.email_inbox = {}  # Simulates email storage
        
        # Register handlers
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(commands=['new_email'])(self.generate_email)
        self.bot.message_handler(commands=['check_mail'])(self.check_email)
        self.bot.message_handler(commands=['simulate_mail'])(self.simulate_email)
        
    def generate_fake_email(self, user_id):
        """Generate a persistent fake email for each user"""
        if user_id in self.user_emails:
            return self.user_emails[user_id]
            
        domains = ["mailinator.com", "tempmail.com", "fakeinbox.com", "10minutemail.com"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(domains)
        email = f"{username}@{domain}"
        self.user_emails[user_id] = email
        self.email_inbox[email] = []
        return email
    
    def send_welcome(self, message):
        welcome_msg = (
            " Fake Email Bot\n\n"
            "I can generate functional-looking fake email addresses for you!\n\n"
            "Commands:\n"
            "/new_email - Generate your fake email\n"
            "/check_mail - Check your inbox\n"
            "/simulate_mail - Simulate receiving an email"
        )
        self.bot.reply_to(message, welcome_msg)
    
    def generate_email(self, message):
        email = self.generate_fake_email(message.from_user.id)
        reply = (
            f" Your new fake email:\n\n"
            f" {email}\n\n"
            f"You can check this inbox at:\n"
            f"https://www.mailinator.com/v3/index.jsp?zone=public&query={email.split('@')[0]}\n\n"
            f"Use /check_mail to see received messages"
        )
        self.bot.reply_to(message, reply)
    
    def check_email(self, message):
        user_id = message.from_user.id
        if user_id not in self.user_emails:
            self.bot.reply_to(message, "You don't have an email yet. Use /new_email first.")
            return
            
        email = self.user_emails[user_id]
        messages = self.email_inbox.get(email, [])
        
        if not messages:
            reply = f" Your inbox ({email}) is empty\n\nUse /simulate_mail to test receiving a message"
        else:
            reply = f" You have {len(messages)} messages in {email}:\n\n"
            for idx, msg in enumerate(messages, 1):
                reply += f"{idx}. From: {msg['sender']}\nSubject: {msg['subject']}\n\n"
        
        self.bot.reply_to(message, reply)
    
    def simulate_email(self, message):
        user_id = message.from_user.id
        if user_id not in self.user_emails:
            self.bot.reply_to(message, "You don't have an email yet. Use /new_email first.")
            return
            
        email = self.user_emails[user_id]
        fake_senders = [
            "support@amazon.com",
            "noreply@google.com",
            "hello@spotify.com",
            "service@paypal.com"
        ]
        fake_subjects = [
            "Your subscription is expiring soon",
            "Password reset requested",
            "New login detected",
            "Please confirm your email",
            "Your invoice is ready"
        ]
        
        new_email = {
            "sender": random.choice(fake_senders),
            "subject": random.choice(fake_subjects),
            "body": "This is a simulated email message.\n\nYou can reply to this email if needed."
        }
        
        self.email_inbox[email].append(new_email)
        reply = (
            f" New email received in {email}!\n\n"
            f"From: {new_email['sender']}\n"
            f"Subject: {new_email['subject']}\n\n"
            f"Use /check_mail to view your inbox"
        )
        self.bot.reply_to(message, reply)
    
    def start(self):
        clear_screen()
        print("Bot is running...")
        print("Visit your bot in Telegram and send /start")
        self.bot.polling()

if __name__ == "__main__":
    bot = FakeEmailBot()
    bot.start()
