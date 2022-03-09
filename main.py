#!/usr/bin/env python


import os
import sys

import argparse
import pathlib

from html import escape as html_escape

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)

from nbt import nbt
from mojang import MojangAPI

searchterm = ""


def playerHas(path, search):
    try:
        nbtfile = nbt.NBTFile(path, "rb")
        if "Inventory" not in nbtfile:
            print(path)
            return False
        for i in nbtfile["Inventory"]:
            name = i["id"]

            # Strip the default prefix
            if name[:10] == "minecraft:":
                name = name[10:]

            if name == search:
                return True

        return False
    except:
        print("Oopsy Whoopsy, the bot has done a fucky wucky")
        return False


def doSearch(world_folder, searchterm):
    results = []
    for file in os.listdir(world_folder):
        if file.endswith(".dat") and len(file) == 40:
            uuid = file[0:36]
            if playerHas(os.path.join(world_folder, file), searchterm):
                try:
                    player_name = MojangAPI.get_username(uuid)
                except:
                    player_name = uuid
                results.append(player_name)
    return results


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help I'm trapped in a telegram bot!")


def search_command(update: Update, context: CallbackContext) -> None:
    """Run a search for the given ID."""
    if len(context.args) > 1 or len(context.args) == 0:
        update.message.reply_text("@%s Please enter a single ID!" % html_escape(update.effective_user.username))
        return

    search_term = context.args[0]

    if search_term[:10] == "minecraft:":
        search_term = search_term[10:]
    
    result = doSearch(world_folder, search_term)

    if result:
        msg = "<b>These players currently have </b><code>%s</code><b> in their inventory:</b>" % html_escape(search_term)
        for r in result:
            msg += "\n‣ %s" % r
        update.message.reply_html(msg)
    else:
        update.message.reply_html("<b>No players with </b><code>%s</code><b> found</b>" % html_escape(search_term))


def main(token) -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("whostole", search_command))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--token", help="telegram bot token", required=True)
    parser.add_argument("-w", "--world", help="path to world", type=pathlib.Path, required=True)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        print("No playerdata folder specified!")
        sys.exit(64)  # EX_USAGE
    world_folder = args.world

    searchterm = sys.argv[2]

    # clean path name, eliminate trailing slashes:
    world_folder = world_folder / "playerdata"
    if not os.path.exists(world_folder):
        print("No such folder as " + world_folder)
        sys.exit(72)  # EX_IOERR

    main(args.token)
