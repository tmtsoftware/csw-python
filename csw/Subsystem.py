from enum import Enum
from dataclasses import dataclass

from csw.EnumUtil import UpperCaseEnum


@dataclass
class SubsystemValue:
    """
    Defines constants for the available subsystems
    """
    name: str
    description: str


class Subsystem(UpperCaseEnum):
    AOESW = SubsystemValue("AOESW", "Adaptive Optics Executive Software")
    APS = SubsystemValue("APS", "Alignment and Phasing System ")
    CIS = SubsystemValue("CIS", "Communications and Information Systems")
    CLN = SubsystemValue("CLN", "Optical Cleaning Systems")
    CRYO = SubsystemValue("CRYO", "Instrumentation Cryogenic Cooling System")
    CSW = SubsystemValue("CSW", "Common Software")
    DMS = SubsystemValue("DMS", "Data Management System")
    DPS = SubsystemValue("DPS", "Data Processing System")
    ENC = SubsystemValue("ENC", "Enclosure")
    ESEN = SubsystemValue("ESEN", "Engineering Sensors")
    ESW = SubsystemValue("ESW", "Executive Software")
    HNDL = SubsystemValue("HNDL", "Optics Handling Equipment")
    HQ = SubsystemValue("HQ", "Observatory Headquarters")
    IRIS = SubsystemValue("IRIS", "InfraRed Imaging Spectrometer")
    LGSF = SubsystemValue("LGSF", "Laser Guide Star Facility")
    M1COAT = SubsystemValue("COAT", "M1COAT M1 Optical Coating System")
    M1CS = SubsystemValue("CS", "M1CS M1 Control System ")
    M1S = SubsystemValue("S", "M1S M1 Optics System")
    M2COAT = SubsystemValue("COAT", "M2/M3 Optical Coating System")
    M2S = SubsystemValue("S", "M2S M2 System")
    M3S = SubsystemValue("S", "M3S M3 System")
    MODHIS = SubsystemValue("MODHIS", "Multi-Object Diffraction-limited High-resolution IR Spectrograph")
    NFIRAOS = SubsystemValue("NFIRAOS", "Narrow Field Infrared AO System")
    OSS = SubsystemValue("OSS", "Observatory Safety System")
    REFR = SubsystemValue("REFR", "Instrumentation Refrigerant Cooling System ")
    SCMS = SubsystemValue("SCMS", "Site Conditions Monitoring System")
    SER = SubsystemValue("SER", "Services")
    SOSS = SubsystemValue("SOSS", "Science Operations Support Systems")
    STR = SubsystemValue("STR", "Structure ")
    SUM = SubsystemValue("SUM", "Summit Facilities")
    TCS = SubsystemValue("TCS", "Telescope Control System")
    TINS = SubsystemValue("TINS", "Test Instruments")
    WFOS = SubsystemValue("WFOS", "Wide Field Optical Spectrograph")
    Container = SubsystemValue("Container", "Container Subsystem")

