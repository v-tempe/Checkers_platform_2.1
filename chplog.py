from datetime import datetime


def log_write(s_source, s_text):
    global g_Logfile, date, datetime
    #today = date.today()
    current_datetime = datetime.now()
    #g_Logfile.write(str(today))
    l_st = str(current_datetime) + ' ' + s_source + ' ' + s_text + '\n'
    g_Logfile.write(l_st)


def log_open(s_log_name):
    global g_Logfile
    g_Logfile = open(s_log_name, 'a')
    log_write("log", "new session created")


def log_close():
    global g_Logfile
    log_write("log", "log closed correctly")
    g_Logfile.close()
