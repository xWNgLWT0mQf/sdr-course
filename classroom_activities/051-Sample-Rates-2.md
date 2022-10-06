### Need for speed

Now, imagine a thermometer on a processor. Actually, you don't need to use your imagination — on Linux, simply run this:

```
watch -n 0.2 -- cat /sys/class/thermal/thermal_zone*/temp
```

This means to check the temperature reading every 0.2 seconds, which is a sample rate of 5 Hz (5 times per second).

The units are thousandths of a degree Celsius, so `27800` means 27.8 °C.

Now, let's make the temperature go up by running a useless (but processor-intensive) Python program:

```python3
for x in range(1000000000000):
    y = x
```

Incredibly, the temperature jumps up by about 13 °C within a fifth of a second. (At least, it did on my computer.)

We can take measurements using Python:

`temp_measure.py`

```python3
import time

outputFileName = "myTempReadings.txt"

# If this doesn't work, try changing it to thermal_zone0, thermal_zone1, thermal_zone3, etc
inputFileName = "/sys/class/thermal/thermal_zone2/temp"

f_out = open(outputFileName, "w")

while True:
    f_temp = open(inputFileName, "r")
    contents = f_temp.read().strip()
    print(contents)
    f_out.write(contents + "\n")
    time.sleep(0.2)
```

<details><summary><i>Note: This will take a measurement <b>approximately</b> five times per second. Click for more info.</i></summary>
   
> For our purposes in this class, "approx 5 times per second" is completely fine.
> 
> However, if you ever need a more precise sample rate for something outside of this class, you would want to use a different approach. See [here](https://stackoverflow.com/a/67930185) and [here](https://mail.python.org/pipermail/python-list/2000-November/060154.html). Fair warning that both links go fairly deeply into the topic.

</details>

When you run that Python file, it will start writing to a file called `myTempReadings.txt`. After a few seconds of data have been recorded, press <kbd>Ctrl C</kbd> to exit the program.
