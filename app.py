import psutil
import telnetlib
import time
import json

''' READ CONFIG '''
with open('conf.json', 'r') as fp:
    obj = json.load(fp)
    fp.close()

''' SET GLOBAL VARIABLES '''
PREV_PIDS = psutil.pids()
RESTRICTED_APPLICATIONS = obj['programs']
RESTRICTED_APP_PIDS = []
IS_PAUSED = False

''' START MAIN LOOP '''
while True:
    ''' SET LOCAL VARIABLES '''
    is_running_restricted_application = False
    do_action = False

    ''' GET LIST OF RUNNING PIDS '''
    running_pids = psutil.pids()

    ''' IDENTIFY NEW PIDS '''
    new_pids = list(set(running_pids) - set(PREV_PIDS))

    ''' LOOP THROUGH EACH NEW PID '''
    if new_pids:
        for pid in new_pids:
            try:
                if psutil.Process(pid).name() in RESTRICTED_APPLICATIONS:
                    is_running_restricted_application = True
                    RESTRICTED_APP_PIDS.append(pid)
            except psutil.NoSuchProcess:
                continue

    ''' UPDATE LIST OF PIDS '''
    PREV_PIDS = running_pids

    ''' DETERMINE IF KNOWN RESTRICTED APPLICATIONS ARE STILL RUNNING '''
    if is_running_restricted_application is False and len(RESTRICTED_APP_PIDS) > 0:
        for pid in RESTRICTED_APP_PIDS:
            try:
                if psutil.Process(pid).name() not in RESTRICTED_APPLICATIONS:
                    RESTRICTED_APP_PIDS.remove(pid)
            except psutil.NoSuchProcess:
                RESTRICTED_APP_PIDS.remove(pid)

        if len(RESTRICTED_APP_PIDS) > 0:
            is_running_restricted_application = True

    ''' DETERMINE IF ACTION IS REQUIRED '''
    if is_running_restricted_application and IS_PAUSED:
        do_action = False
    if is_running_restricted_application and not IS_PAUSED:
        do_action = True
    if not is_running_restricted_application and IS_PAUSED:
        do_action = True
    if not is_running_restricted_application and not IS_PAUSED:
        do_action = False

    ''' IF do_action, TOGGLE FOLDING@HOME '''
    if do_action:
        ''' ESTABLISH TELNET CONNECTION '''
        telnet_connection = telnetlib.Telnet("localhost", 36330)
        telnet_connection.read_until(b"server.\n")

        ''' UNPAUSE IF PAUSED, PAUSE IF RUNNING '''
        if IS_PAUSED:
            telnet_connection.write(b"unpause\n")
            IS_PAUSED = False
            print("Resuming Folding@Home...")
        else:
            telnet_connection.write(b"pause\n")
            IS_PAUSED = True
            print("Suspending Folding@Home...")

        telnet_connection.close()

    ''' SLEEP '''
    time.sleep(5)
