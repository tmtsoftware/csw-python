from enum import Enum
from dataclasses import dataclass


@dataclass
class Subsystem:
    """
    Defines constants for the available subsystems
    """
    description: str


class Subsystems(Enum):
    AOESW = Subsystem("Adaptive Optics Executive Software")
    APS = Subsystem("Alignment and Phasing System ")
    CIS = Subsystem("Communications and Information Systems")
    CLN = Subsystem("Optical Cleaning Systems")
    CRYO = Subsystem("Instrumentation Cryogenic Cooling System")
    CSW = Subsystem("Common Software")
    DMS = Subsystem("Data Management System")
    DPS = Subsystem("Data Processing System")
    ENC = Subsystem("Enclosure")
    ESEN = Subsystem("Engineering Sensors")
    ESW = Subsystem("Executive Software")
    HNDL = Subsystem("Optics Handling Equipment")
    HQ = Subsystem("Observatory Headquarters")
    IRIS = Subsystem("InfraRed Imaging Spectrometer")
    LGSF = Subsystem("Laser Guide Star Facility")
    M1COAT = Subsystem("M1COAT M1 Optical Coating System")
    M1CS = Subsystem("M1CS M1 Control System ")
    M1S = Subsystem("M1S M1 Optics System")
    M2COAT = Subsystem("M2/M3 Optical Coating System")
    M2S = Subsystem("M2S M2 System")
    M3S = Subsystem("M3S M3 System")
    MODHIS = Subsystem("Multi-Object Diffraction-limited High-resolution IR Spectrograph")
    NFIRAOS = Subsystem("Narrow Field Infrared AO System")
    OSS = Subsystem("Observatory Safety System")
    REFR = Subsystem("Instrumentation Refrigerant Cooling System ")
    SCMS = Subsystem("Site Conditions Monitoring System")
    SER = Subsystem("Services")
    SOSS = Subsystem("Science Operations Support Systems")
    STR = Subsystem("Structure ")
    SUM = Subsystem("Summit Facilities")
    TCS = Subsystem("Telescope Control System")
    TINS = Subsystem("Test Instruments")
    WFOS = Subsystem("Wide Field Optical Spectrograph")
    Container = Subsystem("Container Subsystem")
