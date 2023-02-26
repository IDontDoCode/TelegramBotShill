

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random

# Set up the Telegram bot
updater = Updater(token='6008309342:AAH0h0BAS-kjf3BErJcZrH1n-qY3J61DNew', use_context=True)
dispatcher = updater.dispatcher

# Define a global list to store the ticket counts
ticket_counts = {}

# Define a function to handle the /reset command
def reset(update, context):
    global ticket_counts
    ticket_counts = {}
    update.message.reply_text('Ticket counts reset.')

# Define a function to handle the /tickets command
def tickets(update, context):
    user_id = update.message.from_user.id
    if user_id in ticket_counts:
        num_tickets = ticket_counts[user_id]
        update.message.reply_text(f'You have {num_tickets} tickets.')
    else:
        update.message.reply_text('You have no tickets.')

def link_message(update, context):
    message = update.message
    user_id = message.from_user.id
    if user_id not in ticket_counts:
        ticket_counts[user_id] = 0
    ticket_counts[user_id] += 1
    context.bot_data[message.message_id] = user_id

def message_deleted(update, context):
    deleted_message_id = update.message.message_id
    if deleted_message_id in context.bot_data:
        user_id = context.bot_data[deleted_message_id]
        if user_id in ticket_counts:
            ticket_counts[user_id] -= 1
            if ticket_counts[user_id] <= 0:
                del ticket_counts[user_id]

# Define a function to handle the /pickwinner command
def pick_winner(update, context):
    global ticket_counts
    winner_id = random.choice(list(ticket_counts.keys()))
    num_tickets = ticket_counts[winner_id]
    update.message.reply_text(f'The winner is {winner_id} with {num_tickets} tickets!')
    ticket_counts = {}

# Set up the command handlers
dispatcher.add_handler(CommandHandler('reset', reset))
dispatcher.add_handler(CommandHandler('tickets', tickets))
dispatcher.add_handler(CommandHandler('pickwinner', pick_winner))

# Set up the message handler
dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'http(s)?://\S+'), link_message))

# Start the bot
updater.start_polling()