import argparse
import os
import subprocess
import sys

# Define command-line arguments
parser = argparse.ArgumentParser(description='Securely erase a hard drive.')
parser.add_argument('device_path', metavar='DEVICE_PATH', type=str, help='Path to the device to erase')
parser.add_argument('--random', action='store_true', help='Use /dev/random to overwrite data')
parser.add_argument('--file', metavar='FILE', type=str, help='File to use as data for overwriting')

# Parse command-line arguments
args = parser.parse_args()

# Check if script is being run as root
if os.geteuid() != 0:
    print("Error: This script must be run as root.")
    exit(1)

# Secure erase using the DoD 5220.22-M standard
subprocess.run(["shred", "-n", "3", "-z", args.device_path])

# Secure erase using the GOST-R-50739-95 standard
if args.file:
    with open(args.file, 'rb') as f:
        data = f.read(512)
    while data:
        subprocess.run(["dd", "if=-", "of=" + args.device_path, "bs=512", "count=1"], input=data)
        data = f.read(512)
else:
    subprocess.run(["dd", "if=" + "/dev/random" if args.random else "/dev/urandom", "of=" + args.device_path, "bs=512", "count=1"])
    subprocess.run(["dd", "if=/dev/zero", "of=" + args.device_path, "bs=512", "count=1"])
    subprocess.run(["dd", "if=" + "/dev/random" if args.random else "/dev/urandom", "of=" + args.device_path, "bs=512", "count=1"])
