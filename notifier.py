from desktop_notifier import DesktopNotifier, Urgency, Button, ReplyField
from playsound import playsound

notifier = DesktopNotifier(
    app_name="pydl"
)

def finished(title):
    notifier.send_sync(title="pydl - Finished", message=f"pydl has finished downloading {title}!")
    playsound('notif-sound.wav')

def error(title):
    notifier.send_sync(title="pydl - Error", message=f"pydl requires user input to continue downloading {title}!")
    playsound('error-sound.wav')