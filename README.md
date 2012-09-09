#Samplicity v0.3
Samplicity is a command line sample convertion tool created to transform .SFZ sample packs to .XI (Fasttracker 2 eXtended Instrument) format, supported by a number of music creation software. Designed to deal with SunVox music tracker.

Thanks to [Alex Zolotov](http://www.warmplace.ru/) for help and materials.

**If you encounter any problems — contact me here, on [SoundCloud](http://soundcloud.com/convergent) or just email me ```andrew.magalich@gmail.com```**

##Disclaimer
Samplicity is in early beta status and does not support all features in intersection of .SFZ and .XI. Now it is tested **only** in [SunVox tracker](http://www.warmplace.ru/soft/sunvox/) v1.6 and v1.7.2 with 59 sample packs (in 16bit format) I've got.

> Crashes of SunVox are known to me for wrongly encoded .XI-instruments, so **you should save your files every time before loading an instrument** 

####But what the hell! It helped me to write a [song](http://soundcloud.com/convergent/the-fire)! 

##Formats
###eXtended Instrument
This format was created in 1990's for DOS music tracker called Fasttracker 2. It's binary, old and rusty, but still useful.
###SFZ
Open format by Cakewalk company. Designed for creation in notepad. Sample pack contains .sfz file and a number of samples nearby. See more [here](http://www.cakewalk.com/DevXchange/article.aspx?aid=108)

##Usage
Samplicity is writted in [python v2.7.3](http://www.python.org/). To use this tool Python v2.7+ should be installed on your computer.

###Sample convertion
To convert single sample pack, navigate in **terminal/bash/command** line to sample pack folder and run the following command:

```bash
python "<PATH TO SAMPLICITY FOLDER>/samplicity.py" "<SAMPLE PACK NAME>.sfz"
```

If python is installed, path to samplicity is right and sample pack is a valid .SFZ file, you'll see something like this:

```bash
--------------------------------------------------------------------------------
Converting " Keys - Grand Piano (Forte).sfz "
--------------------------------------------------------------------------------
* 16 bit stereo sample " samples/grand piano/piano-f-c1.wav " 726 kB
* 16 bit stereo sample " samples/grand piano/piano-f-d#1.wav " 735 kB
* 16 bit stereo sample " samples/grand piano/piano-f-f#1.wav " 734 kB
* 16 bit stereo sample " samples/grand piano/piano-f-a1.wav " 732 kB
* 16 bit stereo sample " samples/grand piano/piano-f-c2.wav " 725 kB
* 16 bit stereo sample " samples/grand piano/piano-f-d#2.wav " 709 kB
* 16 bit stereo sample " samples/grand piano/piano-f-f#2.wav " 700 kB
* 16 bit stereo sample " samples/grand piano/piano-f-a2.wav " 695 kB
* 16 bit stereo sample " samples/grand piano/piano-f-c3.wav " 623 kB
* 16 bit stereo sample " samples/grand piano/piano-f-d#3.wav " 639 kB
* 16 bit stereo sample " samples/grand piano/piano-f-f#3.wav " 607 kB
* 16 bit stereo sample " samples/grand piano/piano-f-a3.wav " 577 kB
* 16 bit stereo sample " samples/grand piano/piano-f-c4.wav " 563 kB
* 16 bit stereo sample " samples/grand piano/piano-f-d#4.wav " 526 kB
* 16 bit stereo sample " samples/grand piano/piano-f-f#4.wav " 499 kB
* 16 bit stereo sample " samples/grand piano/piano-f-a4.wav " 461 kB
* 16 bit stereo sample " samples/grand piano/piano-f-c5.wav " 441 kB
* 16 bit stereo sample " samples/grand piano/piano-f-d#5.wav " 410 kB
* 16 bit stereo sample " samples/grand piano/piano-f-f#5.wav " 361 kB
* 16 bit stereo sample " samples/grand piano/piano-f-a5.wav " 334 kB
* 16 bit stereo sample " samples/grand piano/piano-f-c6.wav " 322 kB
* 16 bit stereo sample " samples/grand piano/piano-f-d#6.wav " 273 kB
* 16 bit stereo sample " samples/grand piano/piano-f-f#6.wav " 218 kB
* 16 bit stereo sample " samples/grand piano/piano-f-a6.wav " 204 kB
* 16 bit stereo sample " samples/grand piano/piano-f-c7.wav " 138 kB
* 16 bit stereo sample " samples/grand piano/piano-f-d#7.wav " 104 kB
* 16 bit stereo sample " samples/grand piano/piano-f-f#7.wav " 97 kB
* 16 bit stereo sample " samples/grand piano/piano-f-a7.wav " 104 kB
* 16 bit stereo sample " samples/grand piano/piano-f-c8.wav " 103 kB
////////////////////////////////////////////////////////////////////////////////
Notice: some notes are out of range and ignored
['c8']
////////////////////////////////////////////////////////////////////////////////
29 samples
26751 kB written in file " Keys - Grand Piano (Forte).sfz " during 9.435801 seconds

1 files converted in 9.437803 seconds
```

###Batch conversion
To convert more than one .SFZ file you can specify as many arguments to Samplicity as you want. Or even use a wildcard

```bash
python "<PATH TO SAMPLICITY FOLDER>/samplicity.py" "<SAMPLE 1>.sfz" "<SAMPLE 2>.sfz" "<SAMPLE 3>.sfz"
python "<PATH TO SAMPLICITY FOLDER>/samplicity.py" *.sfz 
```

###Reconversion
If there is corresponding to your sample pack .XI file, Samplicity won't convert it again. To force reconversion, add ```--force``` attribute:

```bash
python "<PATH TO SAMPLICITY FOLDER>/samplicity.py" "<SAMPLE NAME>.sfz" --force 

```

##Package
Repository contains:

* ```samplicity.py```
* ```xi_reader.py``` — tool to verify your .XI if something went wrong. Usage: ```python "<PATH TO SAMPLICITY FOLDER>/xi_reader.py" "<SAMPLE NAME>.xi"```. It will show you full info, contained in .XI file (but not samples binary data). It is useful for bugtrack.
* ```xi_specs.txt``` — specifications of eXtended Instrument edited and improved a bit. Thanks [Alex Zolotov](http://www.warmplace.ru/)
* ```Cakewalk DevXchange - Specifications - sfz File Format.pdf``` — specifications of .SFZ saved from Cakewalk [website](http://www.cakewalk.com/DevXchange/article.aspx?aid=108).

##Notices and errors
* **Notice: some notes are out of range and ignored** — .XI supports only 96 notes from C0 to B7, so some notes in your sample pack cannot fit in this range. Consider editing .SFZ file.
* **Notice: some regions are overlapping and would be overwritten** — .SFZ format supports velocity maps. But .XI doesn't. Consider splitting your .SFZ file into separate files. For example, I've got ```Grand Piano (Piano).sfz``` and ```Grand Piano (Forte).sfz```
* **24bit samples are not supported** — .XI and Sunvox don't support 24bit sample format and there is no cooldown feature for them in Samplicity v0.3 
	