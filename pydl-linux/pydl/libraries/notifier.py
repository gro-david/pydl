# type: ignore
# to send notifications
from notifypy import Notify

# to get the paths to the audio files
from libraries import get_app_path


notification = Notify(default_notification_application_name="pydl")


def finished(title):
    notification.audio = f"{get_app_path.main()}/sounds/notif-sound.wav"
    notification.title = "pydl - Finished"
    notification.message = f'pydl has finished downloading "{title}"!'
    notification.send()
    


def error(title):
    notification.audio = f"{get_app_path.main()}/sounds/error-sound.wav"
    notification.title = "pydl - Error"
    notification.message = f'pydl has encountered an error while downloading "{title}"!'
    notification.send()