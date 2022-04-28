#####################################################################################################################
#                                               HOW TO USE NETSH                                                    #
#                                                                                                                   #
#     set dynamic portrange: netsh int ipv4 set dynamicport tcp start=50000 num=255                                 #
#   list excluded portrange: netsh int ipv4 show excludedportrange protocol=tcp                                     #
#    add excluded portrange: netsh int ipv4 add excludedportrange protocol=tcp numberofports=100 startport=50000    #
# delete excluded portrange: netsh int ipv4 delete excludedportrange protocol=tcp numberofports=100 startport=50000 #
#####################################################################################################################

from __init__ import *

system(
    f"netsh interface ipv4 show dynamicport tcp",
    f"netsh interface ipv4 show excludedportrange protocol=tcp",
    f"type {sys.argv[0]}"
)
