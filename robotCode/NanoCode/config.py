## VIDEO CONFIGURATION VARIABLES ## 
VIDEO_ON = True
video_multiplier = 1
display_videofeed = True
if display_videofeed:
    display_barcode_bounding_box = True
    display_contour_bounds = True
    display_crosshair = True
else:     
    display_barcode_bounding_box = False
    display_contour_bounds = False
    display_crosshair = False

SHOW_STATS = False

###### COMMUNICATION CONFIGURATION VARIABLES ###### 
SERVER_IP = "192.169.20.68" # HL Desktop address
#SERVER_IP = "192.168.20.89" # Bens apple computer address
# 192.168.55.100 # Nano1 IP address

# Headless mode doesnt connect to MQTT 
# Use this for line following testing only 
HEADLESS_MODE = True 

# Brainless mode doesnt assign robot number but still connects to MQTT. 
# Assumes node assignments will be sent through mosquitto_pub on laptop 
# IF TRUE: 
    # Server must be running to send bot number for enable
# IF FALSE: 
    # Send commands in the form -t "Brainless" -m "n__"
    # Message sent to -t "Halt" in the form -m "Toggle", -m "Halt", -m "Continue" will enable halt commands as well 
BRAINLESS_MODE = False 

###### CONTROL CONFIGURATION VARIABLES ###### 
# CONTROL_MODE = 1 # Proportional Control
CONTROL_MODE = 2 # PI Control
PWM_CENTER_LEFT = 307
PWM_CENTER_RIGHT = 307
LEFT_DIRECTION = -1
RIGHT_DIRECTION = 1
MAX_SPEED = 11
FRAME_RATE = 60

