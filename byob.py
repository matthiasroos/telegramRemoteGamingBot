
import os
import random
import time
import typing

import telegram.ext


class BringYourOwnBook:

    def __init__(self):
        self.cards = []
        self.rules_text = 'Jeder hat vier Bücher vor sich, nummeriert mit 1-4. Auf den Befehl /card wird ein ' \
                          'zufälliger Prompt gezogen, zusammen mit einer zufälligen Zahl zwischen 1 und 4, ' \
                          'die das zu nutzende Buch angibt. Hat man eine passende Stelle gefunden, so schreibt ' \
                          'man /stop. Die anderen haben daraufhin noch eine ' \
                          'Minute Zeit. Der Bot sagt, wann die Minute vorbeit ist. Sollte man danach nichts ' \
                          'passendes haben, so ist eine ' \
                          'zufällige Seite aufzuschlagen und eine zufällige Zeile zu wählen.'

    def load_card_list(self) -> typing.List[str]:
        with open('BringYourOwnBook_deu.txt') as f:
            card_list = f.read().splitlines()
        return card_list

    def start(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        self.cards = self.load_card_list()
        random.seed(None)
        random.shuffle(self.cards)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Willkommen zu Bring Your Own Book!')
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.rules_text)

    def rules(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.rules_text)

    def card(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        if self.cards:
            text = self.cards[0]
            self.cards.remove(text)
            random.seed(None)
            number = random.randint(1, 4)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"'{text}' aus Buch {number}")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Der Stapel ist leer')

    def stop(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Noch eine Minute...')
        time.sleep(60)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Die Zeit ist um.')

    def main(self, ):
        updater = telegram.ext.Updater(token=os.getenv('TELEGRAM_TOKEN'), use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(handler=telegram.ext.CommandHandler(command='start', callback=self.start))
        dispatcher.add_handler(handler=telegram.ext.CommandHandler(command='rules', callback=self.rules))
        dispatcher.add_handler(handler=telegram.ext.CommandHandler(command='card', callback=self.card))
        dispatcher.add_handler(handler=telegram.ext.CommandHandler(command='stop', callback=self.stop))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':

    byod = BringYourOwnBook()
    byod.main()
