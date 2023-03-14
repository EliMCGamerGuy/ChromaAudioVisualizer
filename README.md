# ChromaAudioVisualizer
I didn't like how the default Razer Chroma visualizer looked, so I made my own.

It's about time I uploaded this to my github. After I fixed a bug causing the visualizer to lock up after about a minute of silence, I pretty much forced myself to actually get around to this. Sorry if it's a little rough.

```
The Environment:
  Windows 10
  Razer synapse 3.0 & 2.0 (how is that even possible?)
  Voicemeeter Banana (Not immediately required if you have some sort of loopback device, but makes things much more convenient!)
  Anaconda Navigator 2.3.2 (Please help, it won't automatically update no matter how many times I say yes!)
    "ChromaVis"
      Version:
        Python 3.7.13
      Modules:
        Pychroma
        Pyaudio
        Windows-curses
```   
The way it looks for loopback devices is it loops through all recording devices, searching for devices that contain "stereo mix", "loopback", or "voicemeeter aux output" in it's title. The way it's set up is it takes the first one of these three that it finds first, so what I do is disable all loopback devices that I don't want it to use. In my current case, this happens to be all but Voicemeeter Banana's second virtual microphone(which I'm piping my sound output through, of course).

For the batch files to work, Anaconda has to be in you PATH and the environment has to be called ChromaVis, unless you want to edit a couple batch files. All "Anti-crash start.bat" does is infinitely loop start.bat, as sometimes, for unknown reasons, it will occasionally crash on me. I actually have it running as I type this! I actually made these batch files so that this program can be added to Windows' startup folder, starting the script when Windows starts.

I've only tested this with an old Razer Deathadder Chroma and a newer Razer Chroma keyboard that I borrowed. If it's wanted, I can try (but probably can't test) colorizing of different devices.

Hope you can get it working! Where there's a will, there's a way!
