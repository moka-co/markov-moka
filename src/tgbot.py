import logging
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from markov_component import MarkovFacade

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def markov(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: accept as input from the user, a word or two (or something like that) that are used as keys for the markov model
    # TODO: accept as input from the user, the maximum limit of words (or maybe set it with a command?)
    # TODO: Interface with mymarkov.py and get the trained markov_model, pass it the story and generate it.
    print("Test")
    markovFacade = MarkovFacade()

    story = markovFacade.get_story()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=story)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    token=None
    if (len(sys.argv)==1):
        print("Error token required")
        quit()
    
    token=sys.argv[1]

    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    markov_handler = CommandHandler('markov', markov)
    application.add_handler(start_handler)
    application.add_handler(markov_handler)
    
    application.run_polling()