def calcAQI(cp, ih, il, bph, bpl):
    a = (ih - il)
    b = (bph - bpl)
    c = (cp - bpl)
    return int((a /b) * c + il)

def aqi_from_pm(pm):
    if (pm > 350.5):
        return calcAQI(pm, 500, 401, 500, 350.5)
    elif (pm > 250.5):
        return calcAQI(pm, 400, 301, 350.4, 250.5)
    elif (pm > 150.5):
        return calcAQI(pm, 300, 201, 250.4, 150.5)
    elif (pm > 55.5):
        return calcAQI(pm, 200, 151, 150.4, 55.5)
    elif (pm > 35.5):
        return calcAQI(pm, 150, 101, 55.4, 35.5)
    elif (pm > 12.1):
        return calcAQI(pm, 100, 51, 35.4, 12.1)
    elif (pm >= 0):
        return calcAQI(pm, 50, 0, 12, 0)

def get_aqi_description(aqi):
    if (aqi >= 401):
       return 'Hazardous'
    elif (aqi >= 301):
        return 'Hazardous'
    elif (aqi >= 201):
        return 'Very Unhealthy'
    elif (aqi >= 151):
        return 'Unhealthy'
    elif (aqi >= 101):
        return 'Unhealthy for Sensitive Groups'
    elif (aqi >= 51):
        return 'Moderate'
    elif (aqi >= 0):
        return 'Good'



