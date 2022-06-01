from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import pytesseract
import argparse
import cv2
import numpy as np
import urllib.request

updater = Updater("",
				use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Image to test bot. Please upload a image file contain text")


def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)


def image_text(update: Update, context: CallbackContext):
	if update.message.photo:
		file_id = update.message.photo[-1].file_id
		newFile=context.bot.get_file(file_id)
		resp = urllib.request.urlopen(newFile.file_path)
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.COLOR_BGR2RGB)
		text = pytesseract.image_to_string(image)
	update.message.reply_text(
		f"Text Extracted From Image")
	update.message.reply_text(
		f"{text}")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_text))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands
updater.start_polling()
