# type: ignore
# to send notifications
from notifypy import Notify

# to get the paths to the audio files
from libraries import get_app_path
import os


notification = Notify(default_notification_application_name="pydl")


def finished(title):
    os.path.join(get_app_path.main(), os.path.join("sounds", "notif-sound.wav"))
    notification.title = "pydl - Finished"
    notification.message = f'pydl has finished downloading "{title}"!'
    notification.send()
    


def error(title):
    os.path.join(get_app_path.main(), os.path.join("sounds", "error-sound.wav"))
    notification.title = "pydl - Error"
    notification.message = f'pydl has encountered an error while downloading "{title}"!'
    notification.send()