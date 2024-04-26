##############################################################################
#                                                                            #
#       ___              _              _          _                         #
#      / _ \ ___  _ __  | |_  ___  ___ | |_  _ __ (_)__  __                  #
#     / /_)// _ \| '_ \ | __|/ _ \/ __|| __|| '__|| |\ \/ /                  #
#    / ___/|  __/| | | || |_|  __/\__ \| |_ | |   | | >  <                   #
#    \/     \___||_| |_| \__|\___||___/ \__||_|   |_|/_/\_\                  #
#                                                                            #
#                                                                            #
#   author: @artemko-ua                                                      #
#   github: https://github.com/artemko-ua                                    #
#   version: 1.0                                                             #
#    the docs is in the docs.md file                                         #
##############################################################################



from sql import sql 
from xss import xss
from multi import multi

art = """
   ___              _              _          _       
  / _ \ ___  _ __  | |_  ___  ___ | |_  _ __ (_)__  __
 / /_)// _ \| '_ \ | __|/ _ \/ __|| __|| '__|| |\ \/ /
/ ___/|  __/| | | || |_|  __/\__ \| |_ | |   | | >  < 
\/     \___||_| |_| \__|\___||___/ \__||_|   |_|/_/\_\ 
"""

print(art)

print("""
Options:
  -h, --help     Display help information.
  -s, --sql      Enable SQL injection mode.
  -x, --xss      Enable XSS attack mode.
  -m, --multi    Enable multi-mode (SQL injection and XSS attacks).
  -e, --exit     Gracefully exit the script.
""")



def mode_chose(_mode):
    if _mode in ("-h", "--help"):
        print("  -h, --help     Display help information.")
        print("  -s, --sql      Enable SQL injection mode.")
        print("  -x, --xss      Enable XSS attack mode.")
        print("  -m, --multi    Enable multi-mode (SQL injection and XSS attacks).")
        print("  -e, --exit     Gracefully exit the script.")

    elif _mode in ("-s", "--sql"):
        print("SQL injection mode activated.")
        sql()
        print("Report ist saved in folder with script.")

    elif _mode in ("-x", "--xss"):
        print("XSS attack mode activated.")
        xss()
        print("Report ist saved in folder with script.")

    elif _mode in ("-m", "--multi"):
        print("Multi-mode (SQL injection and XSS attacks) activated.")
        multi()
        print("Report ist saved in folder with script.")
        
    elif _mode in ("-e", "--exit"):
        print("Exiting the script gracefully.")
        exit() 

while True:
    mode = input("Choose mode: ")
    mode_chose(mode)
