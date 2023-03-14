import pyaudio
import time
from math import log
import audioop  
from decimal import Decimal

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_output_device_info()['defaultSampleRate'])
DEVICE = p.get_default_output_device_info()['index']
rms = Decimal(0.000001)
print(p.get_default_output_device_info())

def callback(in_data, frame_count, time_info, status):
    #print(in_data)
    print(audioop.rms(bytes(in_data), WIDTH)) #THIS NUMBER GOES UP IF I YELL!
    global rms 
    rms = Decimal(audioop.rms(bytes(in_data), WIDTH) / 32767)
    return in_data, pyaudio.paContinue


stream = p.open(format=p.get_format_from_width(WIDTH),
                output_device_index=DEVICE,
                channels=2,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

stream.start_stream()

while stream.is_active(): 
    db = 20 * rms.log10()
    print(f"RMS: {rms.ln()} DB: {db}") 
    # refresh every 0.3 seconds 
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()