from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from telegram import Update
import random, time
import requests
from bs4 import BeautifulSoup
import tempfile
from pytube import YouTube
from keep_alive import keep_awake

TOKEN = "6676727193:AAEe3_0acH4MgkE_qAvaaNaY2BKISGDW0ac"
BOT_USERNAME = "@the_requestbot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Welcome to the Request bot, enter /help to get a list of my commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("""Here are my commands:
/start - Starts the bot
/help - Shows this message
/request [link] - sends a request to a site
/image [link] - Downloads an image
/video [link] - Downloads a video
/yt_video [link] - Downloads a Youtube video
/text [link] - Downloads a text file
""")


request = None
async def request_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global request
  param = update.message.text.split("/request")[-1]

  # send a request and if that doesn't work, use a try/except to catch the error
  try:
    request = requests.get(param)
    await update.message.reply_text("Making request...")
    await update.message.reply_text(f"Request made to {param},  \n\nRequest status: {request}")
    await update.message.reply_text(f"Enter /site_content to get the site content or use /get_tag [tag_name] to get a specific tag")

  except Exception as e:
    await update.message.reply_text(f"That didn't quite work, You got the following error: {e}")



# use beautifulsoup to prettify and get text

async def get_site_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if request is not None:
    soup = BeautifulSoup(request.content, "html.parser")
    output = soup.prettify()


  else:
    output = "Please make a request first, use /request [link] to do this or /help to go to help."

  try:
    await update.message.reply_text(output)
  except Exception as e:
    await update.message.reply_text(f"There appears to be an issue. Error message: {e}\n\n i'll try to halve the output.")

    try:
      
      group_size = 400
      
      for i in range(0, len(output), group_size):
          if i + group_size < len(output):
              await update.message.reply_text(output[i:i + group_size])
          else:
              await update.message.reply_text(output[i:])
    except:
      await update.message.reply_text("It appears that didn't work either, please try something else...")


async def get_site_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
  tag = update.message.text.split("/get_tag")[-1]

  try:
    if request is not None:
      soup = BeautifulSoup(request.content, "html.parser")
      tags = soup.find_all(tag)
      if len(tags) > 0:
        for tag in tags:
          await update.message.reply_text(tag)
      else:
        await update.message.reply_text(f"No tags found with the tag name {tag}")
  except Exception as e:
    await update.message.reply_text(f"oops! Something went terribly wrong, maybe you entered an invalid tag? \n\n Error message: {e}")

  finally:
    await update.message.reply_text("That's that! use /help to see the help menu.")


async def download_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = update.message.text.split("/text")[-1]
  try:
    text = requests.get(text).content.decode("utf-8")
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as temp_file:
    # Write some content to the temporary file
      temp_file.write(text)
      temp_file.seek(0)  # Reset the file pointer to the beginning

      # Read and print the content of the temporary file
      await update.message.reply_document(temp_file)
  except Exception as e:
    await update.message.reply_text(f"Well that went horribly wrong., see the error message: {e}")

async def download_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
  image = update.message.text.split("/image")[-1]
  try:
    image = requests.get(image).content
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='wb+', suffix='.png', delete=False) as temp_file:
    # Write some content to the temporary file
      temp_file.write(image)
      temp_file.seek(0)  # Reset the file pointer to the beginning

      # Read and print the content of the temporary file
      await update.message.reply_photo(temp_file)
  except Exception as e:
    await update.message.reply_text(f"Well that went horribly wrong., see the error message: {e}")

async def download_youtube_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
  video_url = update.message.text.split("/video")[-1]
  try:
        # Create a YouTube object
        yt = YouTube(video_url)

        await update.message.reply_text("Downloading video...")

        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        # Download the video to a temporary file
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4', delete=False) as temp_file:
            # Download the video content
            video_content = requests.get(stream.url).content
            # Write the video content to the temporary file
            temp_file.write(video_content)
            temp_file.seek(0)  # Reset the file pointer to the beginning

            # Send the video as a reply
            await update.message.reply_video(video=temp_file)
  except Exception as e:
        await update.message.reply_text(f"Well that went horribly wrong. See the error message: {e}")


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
  video = update.message.text.split("/video")[-1]
  try:
    video = requests.get(video).content
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4', delete=False) as temp_file:
    # Write some content to the temporary file
      temp_file.write(video)
      temp_file.seek(0)  # Reset the file pointer to the beginning

      # Read and print the content of the temporary file
      await update.message.reply_video(temp_file)
  except Exception as e:
    await update.message.reply_text(f"Well that went horribly wrong., see the error message: {e}")


def main():
  print("Starting bot...")
  app = Application.builder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start_command))
  app.add_handler(CommandHandler("help", help_command))

  app.add_handler(CommandHandler("request", request_command))
  app.add_handler(CommandHandler("site_content", get_site_content))

  app.add_handler(CommandHandler("get_tag", get_site_tags))

  app.add_handler(CommandHandler("text", download_text))
  app.add_handler(CommandHandler("video", download_video))
  app.add_handler(CommandHandler("yt_video", download_youtube_video))
  app.add_handler(CommandHandler("image", download_image))

  print("Bot active!")

  app.run_polling()


if __name__ == "__main__":
  keep_awake()
  main()