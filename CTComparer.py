# CTComparer.py
# Compare two "CustomText"-format ".ini" textbibles from TS:H&R.
# Feb-2025 @CelestialAddy

# Initialisation

import sys            as System
import Module.CTDump  as Dumper

PROG_VER              = "1"
SKIP_ASKS_ON          = False
PRINT_PADDING_ON      = True
PRINT_CUTTING_ON      = True
COMMAND_LINE_ARGS     = System.argv
TEMP_ASK              = ""

CLA_T1_PATH           = 1
CLA_T1_TYPE           = 2
CLA_T2_PATH           = 3
CLA_T2_TYPE           = 4
CLA_XO_PATH           = 5
CLA_XO_TYPE           = 6
CLA_MAX               = 7

T1_PATH = ""
T1_TYPE = ""
T1_DUMP = {}
T1_BACK = {}

T2_PATH = ""
T2_TYPE = ""
T2_DUMP = {}
T2_BACK = {}

T1_ONLY = []
T2_ONLY = []
DIFFERS = []

XO_FLAG = None
XO_PATH = ""
XO_TYPE = ""
XO_FILE = None
XO_DATA = ""

# Error function

def Error(Message="ERROR"):
    if SKIP_ASKS_ON: print(Message)
    else: input(Message + "\n")
    exit(0)

# Process CLIs

if len(COMMAND_LINE_ARGS) == CLA_MAX:
    try:
        T1_PATH = COMMAND_LINE_ARGS[CLA_T1_PATH]
        T1_TYPE = COMMAND_LINE_ARGS[CLA_T1_TYPE]
        T1_DUMP = Dumper.Dump(Path=T1_PATH, Codec=T1_TYPE)
        T1_BACK = T1_DUMP.copy()
        T2_PATH = COMMAND_LINE_ARGS[CLA_T2_PATH]
        T2_TYPE = COMMAND_LINE_ARGS[CLA_T2_TYPE]
        T2_DUMP = Dumper.Dump(Path=T2_PATH, Codec=T2_TYPE)
        T2_BACK = T2_DUMP.copy()
        XO_PATH = COMMAND_LINE_ARGS[CLA_XO_PATH]
        XO_TYPE = COMMAND_LINE_ARGS[CLA_XO_TYPE]
        SKIP_ASKS_ON = True
    except:
        Error("Error on responding to command line arguments.")

# Asks if on

print(f"CustomText Comparer (revision {PROG_VER}) by CelestialAddy)\n" + "=" * 100)

if not SKIP_ASKS_ON:
    try:
        TEMP_ASK = input("1st INI (path; encoding)? ")
        T1_PATH = TEMP_ASK.split(";")[0].strip()
        T1_TYPE = TEMP_ASK.split(";")[1].strip()
        T1_DUMP = Dumper.Dump(Path=T1_PATH, Codec=T1_TYPE)
        T1_BACK = T1_DUMP.copy()
        TEMP_ASK = input("1st INI (path; encoding)? ")
        T2_PATH = TEMP_ASK.split(";")[0].strip()
        T2_TYPE = TEMP_ASK.split(";")[1].strip()
        T2_DUMP = Dumper.Dump(Path=T2_PATH, Codec=T2_TYPE)
        T2_BACK = T2_DUMP.copy()
    except:
        Error("Error on acquiring textbibles.")

# Compare pt1/Exclusives

for String in T1_DUMP:
    if String not in T2_DUMP:
        T1_ONLY.append(String)
        T1_DUMP[String] = None
for String in T2_DUMP:
    if String not in T1_DUMP:
        T2_ONLY.append(String)
        T2_DUMP[String] = None

# Compare pt2/Differences

for String, Text in T1_DUMP.items():
    if Text == None: continue
    if Text != T2_DUMP[String]: DIFFERS.append(String)

# Compare pt3/Print

print("-" * 50)
print("Exclusive to 1st (" + str(len(T1_ONLY)) + ") :")
for String in T1_ONLY: print(String)
print("Exclusive to 2nd (" + str(len(T2_ONLY)) + ") :")
for String in T2_ONLY: print(String)
print("Differences in text (" + str(len(DIFFERS))  + ") :")
for String in DIFFERS: print(String)
print("-" * 50)

# Compare pt4/Dump

if not SKIP_ASKS_ON:
    while XO_FLAG == None:
        XO_FLAG = input("Output full results to text file (Y/N)? ").upper()
        if XO_FLAG == "Y": XO_FLAG = True
        elif XO_FLAG == "N": XO_FLAG = False
        else: XO_FLAG = None
else:
    XO_FLAG = True

if XO_FLAG == True:
    try:
        if not SKIP_ASKS_ON:
            TEMP_ASK = input("To where (path; encoding)? ")
            XO_PATH = TEMP_ASK.split(";")[0].strip()
            XO_TYPE = TEMP_ASK.split(";")[1].strip()
        XO_FILE = open(XO_PATH, "wt", encoding=XO_TYPE)
        XO_DATA = XO_DATA + f"Exclusive to 1st ({str(len(T1_ONLY))}):\n"
        for String in T1_ONLY:
            XO_DATA = XO_DATA + "\t"
            XO_DATA = XO_DATA + String + " :\n\t\t"
            XO_DATA = XO_DATA + T1_BACK[String]
            XO_DATA = XO_DATA + "\n"
        XO_DATA = XO_DATA + f"Exclusive to 2nd ({str(len(T2_ONLY))}):\n"
        for String in T2_ONLY:
            XO_DATA = XO_DATA + "\t"
            XO_DATA = XO_DATA + String + " :\n\t\t"
            XO_DATA = XO_DATA + T2_BACK[String]
            XO_DATA = XO_DATA + "\n"
        XO_DATA = XO_DATA + f"Differences in text ({str(len(DIFFERS))}):\n"
        for String in DIFFERS:
            XO_DATA = XO_DATA + "\t"
            XO_DATA = XO_DATA + String + " :\n\t\t"
            XO_DATA = XO_DATA + T1_BACK[String] + "\n\t\t" + T2_BACK[String]
            XO_DATA = XO_DATA + "\n"
        XO_FILE.write(XO_DATA)
        XO_FILE.close()
    except:
        Error("Error on making full results output.")

# Done

exit(0)

# End.
