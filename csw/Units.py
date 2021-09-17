from enum import Enum
from dataclasses import dataclass


@dataclass
class Unit:
    """
    A class representing units for TMT (Corresponds to the CSW Units Scala class)
    """
    name: str
    description: str


class Units(Enum):
    # SI units
    angstrom = Unit("Angstrom", "10 -1 nm")
    arcmin = Unit("arcmin", "arc minute; angular measurement")
    arcsec = Unit("arcsec", "arc second: angular measurement")
    day = Unit("d", "day - 24 hours")
    degree = Unit("deg", "degree: agular measurement 1/360 of full rotation")
    elvolt = Unit("eV", "electron volt 1.6022x10-19 J")
    gram = Unit("g", "gram 10-3 kg")
    hour = Unit("h", "hour 3.6x10+3 s")
    hertz = Unit("Hz", "frequency")
    joule = Unit("J", "Joule: energy N m")
    kelvin = Unit("K", "Kelvin: temperature with a null point at absolute zero")
    kilogram = Unit("kg", "kilogram, base unit of mass in SI")
    kilometer = Unit("km", "kilometers - 10+3 m")
    liter = Unit("l", "liter, metric unit of volume 10+3 cm+3")
    meter = Unit("m", "meter: base unit of length in SI")
    marcsec = Unit("mas", "milli arc second: angular measurement 10-3 arcsec")
    millimeter = Unit("mm", "millimeters - 10-3 m")
    millisecond = Unit("ms", "milliseconds - 10-3 s")
    micron = Unit("µm", "micron: alias for micrometer")
    micrometer = Unit("µm", "micron: 10-6 m")
    minute = Unit("min", "minute 6x10+1 s")
    newton = Unit("N", "Newton: force")
    pascal = Unit("Pa", "Pascal: pressure")
    radian = Unit("rad", "radian: angular measurement of the ratio between the length of an arc and its radius")
    second = Unit("s", "second: base unit of time in SI")
    sday = Unit("sday", "sidereal day is the time of one rotation of the Earth: 8.6164x10+4 s")
    steradian = Unit("sr", "steradian: unit of solid angle in SI - rad+2")
    microarcsec = Unit("µas", "micro arcsec: angular measurement")
    volt = Unit("V", "Volt: electric potential or electromotive force")
    watt = Unit("W", "Watt: power")
    week = Unit("wk", "week - 7 d")
    year = Unit("yr", "year - 3.6525x10+2 d")
    # CGS units
    coulomb = Unit("C", "coulomb: electric charge")
    centimeter = Unit("cm", "centimeter")
    erg = Unit("erg", "erg: CGS unit of energy")
    # Astropyhsics units
    au = Unit("AU", "astronomical unit: approximately the mean Earth-Sun distance")
    jansky = Unit("Jy", "Jansky: spectral flux density - 10-26 W/Hz m+2")
    lightyear = Unit("lyr", "light year - 9.4607x10+15 m")
    mag = Unit("mag", "stellar magnitude")
    # Imperial units
    cal = Unit("cal", "thermochemical calorie: pre-SI metric unit of energy")
    foot = Unit("ft", "international foot - 1.2x10+1 inch")
    inch = Unit("inch", "international inch - 2.54 cm")
    pound = Unit("lb", "international avoirdupois pound - 1.6x10+1 oz")
    mile = Unit("mi", "international mile - 5.28x10+3 ft")
    ounce = Unit("oz", "international avoirdupois ounce")
    yard = Unit("yd", "international yard - 3 ft")
    # Others - engineering
    NoUnits = Unit("none", "scalar - no units specified")
    encoder = Unit("enc", "encoder counts")
    count = Unit("ct", "counts as for an encoder or detector")
    pix = Unit("pix", "pixel")
    # Datetime units
    tai = Unit("TAI", "TAI time unit")
    utc = Unit("UTC", "UTC time unit")
