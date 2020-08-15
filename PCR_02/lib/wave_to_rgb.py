def wavelength_to_rgb(self,data):
    Gamma = 0.80
    IntensityMax = 255
    wavelength=data
    if wavelength >= 380 and wavelength<440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif wavelength >= 440  and wavelength<490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif wavelength >= 490 and wavelength<510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif wavelength >= 510 and wavelength<580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif wavelength >= 580 and wavelength<645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    elif wavelength >= 645 and wavelength<781:
        red = 1.0
        green = 0.0
        blue = 0.0
    else:
        red = 0.0
        green = 0.0
        blue = 0.0
    if wavelength >= 380 and wavelength<420:
        factor = 0.3 + 0.7*(wavelength - 380) / (420 - 380)
    elif  wavelength >= 420 and wavelength<701:
        factor = 1.0
    elif  wavelength >= 701 and wavelength<781:
        factor = 0.3 + 0.7*(780 - wavelength) / (780 - 700)
    else:
        factor = 0.0
    if red != 0:
        red = round(IntensityMax * math.pow(red * factor, Gamma))
    if green != 0:
        green = round(IntensityMax * math.pow(green * factor, Gamma))
    if blue != 0:
        blue = round(IntensityMax * math.pow(blue * factor, Gamma))
    print(red,green,blue)