## VIDEO CONFIGURATION VARIABLES ## 
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

## MQTT CONFIGURATION VARIABLES ##
# SERVER_IP = "192.168.20.68" # Desktop HL
 
SERVER_IP = "192.168.20.89" # Ben's mac HL
# 192.168.55.100 # Nano1 IP address

## CONTROL CONFIGURATION VARIABLES ## 
CONTROL_MODE = 1 # Proportional Control
# CONTROL_MODE = 2 # PI Control
PWM_CENTER_LEFT = 307
PWM_CENTER_RIGHT = 307
LEFT_DIRECTION = -1
RIGHT_DIRECTION = 1
MAX_SPEED = 13
