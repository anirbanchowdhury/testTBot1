"""Readme :  pip install python-telegram-bot --upgrade"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from config import BOT_TOKEN, API_KEY,IDS_ALLOWED

def movie_handler(update, context):
    """ Get the userId + firstname + get/store results"""
    id = int(update.message.from_user.id)
    if len(IDS_ALLOWED) >0 and id not in IDS_ALLOWED:
        print(id)
        update.message.reply_text("Sorry, i dont know you")
        return

    print(id)
    first_name = update.message.chat.first_name
    opening_line = f"""Hi {first_name}! \nLet's play together :)"""
    update.message.reply_text(opening_line)

    print("\n====== entered movie_handler ======")
    chat_id = update.message.chat_id

    print("====== movie_handler update.message.text: " + update.message.text)
    # TODO No.1:
    # get the movie name entered by the user from the variable update.message.text
    # and store it in the variable movie_name
    movie_name = update.message.text[7:].strip()
    print("====== movie_name: " + movie_name)

    # TODO No.2:
    # Given a API, use the API to retrieve information related to movie name
    constructed_url = "http://www.omdbapi.com/?apikey="+API_KEY + movie_name
    print("====== constructed_url: " + constructed_url)
    contents = requests.get(constructed_url).json()
    print("====== contents: " + str(contents))

    # TODO No.3:
    # Retrieve the field Response from the contents
    response = contents["Response"]
    print("====== response: " + response)

    # TODO No.4:
    # Given successful query will have the response as True, unsuccessul query will have response as False
    # write a if else condition
    # for failed query: send back a message to notify user that there is no information found
    # for success query: send back the Title and Year
    if response == "False":
        context.bot.send_message(chat_id=chat_id, text="No movie available for this title: " + movie_name)
    else:
        title = contents["Title"]
        year = contents["Year"]
        context.bot.send_message(chat_id=chat_id, text="Title: " + title + ". Year: " + year)

        # TODO No.5:
        # add on to the response True branch that we have written
        # return the Poster field as photo to the user
        if contents["Poster"] != "N/A":
            context.bot.send_photo(chat_id=chat_id, photo=contents["Poster"])
        else:
            context.bot.send_message(chat_id=chat_id, text="No poster available for this one")

        # TODO No.6:
        # Open ended question. Return whichever field in whichever format you want.
        # teachers can go through the example below
        """
        for key, value in contents.items():
            if (key not in ["Response", "Poster"]):
                constructed_text = key + ": " + str(value)
                context.bot.send_message(chat_id=chat_id, text=constructed_text)
        """

def fallback_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command. Please try with: ")
    context.bot.send_message(chat_id=update.effective_chat.id, text="/movie <movie_name>")


def main():
    print("====== starting bot program ======")

    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # example dog_picture_handler to be demonstrated by teacher
    #dispatcher.add_handler(CommandHandler("dog", dog_picture_handler))

    # movie_handler to be filled in by student
    dispatcher.add_handler(CommandHandler("movie", movie_handler))

    # Optional content - fallback handler
    dispatcher.add_handler(MessageHandler(Filters.all, fallback_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()