import os
import subprocess
import time
import sys

def get_inserted():
	return len([x for x in os.listdir("/dev") if x.startswith("hidraw")]) == 1

was_inserted = False

def on_change(inserted):
	if inserted:
		mode = "dorm_room.sh"
	else:
		mode = "laptop.sh"
	print("flip", mode)
	subprocess.check_call([os.path.join(os.getenv("HOME"), ".screenlayout", mode)])

def on_update():
	global was_inserted
	time.sleep(0.3)
	is_inserted = get_inserted()
	print("is", is_inserted)
	if was_inserted != is_inserted:
		was_inserted = is_inserted
		on_change(is_inserted)

time.sleep(2)

if os.getenv("DISPLAY") is None:
	os.putenv("DISPLAY", ":0.0")

print("GOT ENV", os.getenv("DISPLAY", "nope"))
on_update()

with subprocess.Popen(["/bin/dmesg", "--follow"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as sub:
	now = time.time()
	for line in sub.stdout:
		now2 = time.time()
		if now2 - now > 0.01 and b"USB" in line:
				on_update()
		now = now2
