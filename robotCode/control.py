def piControl(dev, lSpeed, rSpeed, integral):
    kp = 0.9
    kpp = 0.3
    ki = 0.02
    aDev = abs(dev)
    rIntegral = 0
    lIntegral = 0
    if dev < 0:
        lScale = kp * aDev
        rScale = kpp * kp * aDev
        rIntegral = abs(integral)
    elif dev > 0:
        rScale = kp * aDev
        lScale = kpp * kp * aDev
        lIntegral = abs(integral)
    else:
        rScale = 1
        lScale = 1
    leftSpeed = lSpeed - lScale + ki * lIntegral
    rightSpeed = rSpeed - rScale + ki * rIntegral
    return leftSpeed, rightSpeed
    
def pControl(dev, lSpeed, rSpeed):
    kp = 0.2
    kpp = 0.1
    aDev = abs(dev)
    if dev < 0:
        lScale = kp * aDev
        rScale = kpp * kp * aDev
    elif dev > 0:
        rScale = kp * aDev
        lScale = kpp * kp * aDev
    else:
        rScale = 0
        lScale = 0
    leftSpeed = lSpeed - lScale
    rightSpeed = rSpeed - rScale
    print("Scale: ", lScale, rScale)
    return leftSpeed, rightSpeed