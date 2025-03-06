import snowboydecoder
import snowboydetect
import sys
import signal
import lirc
from pyaudio import PyAudio, paInt16
import os
import time
from aip import AipSpeech
import urllib
import requests



model="Xiaogao.pmdl"

BAIDU_APP_ID = "117747355"
BAIDU_API_KEY = "CTeU8kxApZQ1RQSesKE8zKq6"
BAIDU_SECRET_KEY = "BHXqCW5u8dkv9Obvs64m0yUQqKmXbpdh"
BAIDU_ENDPOINT = "https://aip.baidubce.com/rest/26/ai/v1/online-speech-recognition"




def detect(model):
    global interrupted
    interrupted = False

    def signal_handler(signal, frame):
        global interrupted
        interrupted = True

    def interrupt_callback():
        global interrupted
        return interrupted

    # if len(sys.argv) == 1:
    #    print("Error: need to specify model name")
    #    print("Usage: python demo.py your.model")
    #    sys.exit(-1)

    # model = sys.argv[1]

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    detector.start(detected_callback=snowboydecoder.play_audio_file,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    return detector.terminate()

def init_baidu_sdk():
    """INITIAL BAIDU AI SDK"""
    return AipSpeech(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)

def find_microphone_device(p, devices):
    device_list = []
    for i in range(devices):
       # Get the device info
       device_info = p.get_device_info_by_index(i)
       # Check if this device is a microphone (an input device)
       if device_info.get('maxInputChannels') > 0 and device_info.get('hostApi') == 0:
          # device_list.append(f"Microphone: {device_info.get('name')} , Device Index: {device_info.get('index')}")
          device_list.append(device_info.get('index'))
          #print(f"Microphone: {device_info.get('name')} , Device Index: {device_info.get('index')}")
          print("microphone is selected by id = " + str(i))
          return i
def record_audio(device_index, duration=5):
    """Record speech"""
    stream = p.open(
        format=paInt16,
        channels=1,
        rate=16000,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=1024
    )

    frames = []
    start_time = time.time()
    print("Starting recording...")

    while time.time() - start_time < duration:
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with open("record.wav", "wb") as f:
        f.write(b''.join(frames))
    print("Record finish. The file is saved as record.wav")
    return "PASS"

def speech_to_text(audio_file):
    
    print("Starting converting...")
    

    aip_speech = init_baidu_sdk()

    aip_speech.setConnectionTimeoutInMillis(10000) 

    with open(audio_file, "rb") as f:
        audio_data = f.read()

    result = aip_speech.asr(audio_data)

    print("The result has been converted! Now writting it in result_all.txt")

    with open("result_all.txt", "w") as fr:
        fr.write(f"{result}")

    #return result['result'][-1]
    #return "PASS"
    print("Convert finish!")
    return ["PASS", result['result'][-1]]


def qingyunke(msg):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    html = requests.get(url)
    return html.json()["content"]


if __name__ == "__main__":
    p=PyAudio()
    devices=p.get_device_count()
    device_index = find_microphone_device(p,devices)
    
    status=2 #0:wake 1:listen 2:recognition 3:reply
    
    while True:
        if status == 0:
            r0 = detect(model)
            if r0 == "PASS":
                print("Detected waked word!")
                status+=1
            else:
                print("Failed at r0!")
                break
        elif status == 1:
            r1 = record_audio(device_index, duration=10)
            if r1 == "PASS":
                status+=1
            else:
                print("Fail at r1!")
                break
        elif status == 2:
            r2 = speech_to_text("record.wav")
            if r2[0] == "PASS":
                with open("r2.txt", "w", encoding="utf-8") as f2:
                    f2.write(f"Recognition result:\n{r2[1]}")
                status+=1
            else:
                print("Failed at r2")
                break
        elif status == 3:
            r3=qingyunke(r2[1])
            if r3 != None:
                with open("r3.txt", "w", encoding="utf-8") as f3:
                    f3.write(f"Reply result:\n{r3}")
                status=0
            else:
                print("Failed at r3")
                break



