import json, sys, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from graphqlclient import GraphQLClient

import config


#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)

logger = logging.getLogger(__name__)

client = GraphQLClient('https://pontoon.mozilla.org/graphql')

def start(bot, update):
    update.message.reply_text('Hi')

def echo(bot, update):
    result = client.execute('''
    {
        locale(code: "%s") {
            name,
            totalStrings,
            missingStrings,
            translatedStrings,
            approvedStrings
            localizations {
                project{
                    name,
                    totalStrings
                }
                totalStrings,
                missingStrings
            }
        }
    }

    ''' % update.message.text
    )
    response = json.loads(result)
    locale_data = response["data"]["locale"]
    update.message.reply_text(
        '''Locale: %s 
        Total Strings: %s 
        Missing Strings: %s 
        Translated Strings: %s 
        Approved Strings: %s'''
        % 
        (
        locale_data["name"], 
        locale_data["totalStrings"], 
        locale_data["missingStrings"], 
        locale_data["translatedStrings"], 
        locale_data["approvedStrings"]
        )
    )

def main():
    #token
    updater = Updater(config.TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()




