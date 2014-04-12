Samplicity v0.5
===============

Samplicity is a command line sample convertion tool created to transform
.SFZ sample packs to .XI (Fasttracker 2 eXtended Instrument) format,
supported by a number of music creation software. Designed to deal with
SunVox music tracker.

Thanks to `Alex Zolotov <http://www.warmplace.ru/>`__ for help and
materials.

**If you encounter any problems — contact me here, on
`SoundCloud <http://soundcloud.com/convergent>`__ or just email me
``andrew.magalich@gmail.com``**

Changelog
---------

v0.5 April 12th, 2014
~~~~~~~~~~~~~~~~~~~~~

-  Various WAV types support thanks to scikits.audiolab.SndFile
   (including 24bit!)
-  Runtime option "--play": play all samples converted
-  Runtime option "--verbose %": set output verbosity to % (0/1/2)
-  Excess samples are no longer added to resulting .XI file
-  New notice about omitted excess samples
-  Conversion speed increased dramatically

v0.4 September 27th, 2012
~~~~~~~~~~~~~~~~~~~~~~~~~

-  Added sample count constraint (no more than 128 per file) – -1
   observed error
-  Moved temp files to system temp dir – job done clear now
-  Fixed envelope length and seconds-to-ticks conversion parameter — no
   more SunVox crashes

Disclaimer
----------

Samplicity is in early beta status and does not support all features in
intersection of .SFZ and .XI. Now it is tested **only** in `SunVox
tracker <http://www.warmplace.ru/soft/sunvox/>`__ v1.6 and v1.7.2 with
59 sample packs (in 16bit format) I've got.

    Crashes of SunVox are known to me for wrongly encoded
    .XI-instruments, so **you should save your files every time before
    loading an instrument**

But what the hell! It helped me to write some `songs <http://soundcloud.com/convergent>`__!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Formats
-------

eXtended Instrument
~~~~~~~~~~~~~~~~~~~

This format was created in 1990's for DOS music tracker called
Fasttracker 2. It's binary, old and rusty, but still useful. ### SFZ
Open format by Cakewalk company. Designed for creation in notepad.
Sample pack contains .sfz textfile and a number of samples nearby. So,
you can create your sample pack without any specific software. See more
`here <http://www.cakewalk.com/DevXchange/article.aspx?aid=108>`__

Usage
-----

Samplicity is written in `python v2.7.3 <http://www.python.org/>`__. To
use this tool Python v2.7+ should be installed on your computer.

Installation
~~~~~~~~~~~~

If you use ``pip``, you can just

.. code:: bash

    pip install samplicity

To manually install this package, simply download and run in its
directory:

.. code:: bash

    python setup.py install

Now you're ready to use Samplicity! Try:

.. code:: bash

    samplicity

Sample convertion
~~~~~~~~~~~~~~~~~

To convert single sample pack, navigate in
**terminal/bash/command**\ line to sample pack folder and run the
following command:

.. code:: bash

    python samplicity "<SAMPLE PACK NAME>.sfz"

If python is installed, path to samplicity is right and sample pack is a
valid .SFZ file, you'll see something like this:

.. code:: bash

    --------------------------------------------------------------------------------
    Converting " Keys - Grand Piano.sfz "
    --------------------------------------------------------------------------------
    ////////// Notice: some regions are overlapping and would be overwritten
    c1, c#1, d1, d#1, e1, f1, f#1, g1, g#1, a1, a#1, b1, c2, c#2, d2, d#2, e2, f2,
    f#2, g2, g#2, a2, a#2, b2, c3, c#3, d3, d#3, e3, f3, f#3, g3, g#3, a3, a#3, b3,
    c4, c#4, d4, d#4, e4, f4, f#4, g4, g#4, a4, a#4, b4, c5, c#5, d5, d#5, e5, f5,
    f#5, g5, g#5, a5, a#5, b5, c6, c#6, d6, d#6, e6, f6, f#6, g6, g#6, a6, a#6, b6,
    c7, c#7, d7, d#7, e7, f7, f#7, g7, g#7, a7, a#7, b7
    ////////// Notice: some notes are out of range and ignored
    c8
    ////////// Notice: some regions are not used, skipping:
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    23, 24, 25, 26, 27, 28, 29

    29 samples, 54225 kB written during 0.347247 seconds

    1 files converted in 0.352371 seconds

You can control verbosity of output using ``--verbose`` command:

.. code:: bash

    $ samplicity Keys\ -\ Grand\ Piano.sfz --force --verbose 0
    --------------------------------------------------------------------------------
    Converting " Keys - Grand Piano.sfz "
    --------------------------------------------------------------------------------

    29 samples, 54225 kB written during 0.35783 seconds

    1 files converted in 0.362867 seconds

.. code:: bash

    $ samplicity Keys\ -\ Grand\ Piano.sfz --force --verbose 2
    --------------------------------------------------------------------------------
    Converting " Keys - Grand Piano.sfz "
    --------------------------------------------------------------------------------
    ////////// Notice: some regions are overlapping and would be overwritten
    c1, c#1, d1, d#1, e1, f1, f#1, g1, g#1, a1, a#1, b1, c2, c#2, d2, d#2, e2, f2,
    f#2, g2, g#2, a2, a#2, b2, c3, c#3, d3, d#3, e3, f3, f#3, g3, g#3, a3, a#3, b3,
    c4, c#4, d4, d#4, e4, f4, f#4, g4, g#4, a4, a#4, b4, c5, c#5, d5, d#5, e5, f5,
    f#5, g5, g#5, a5, a#5, b5, c6, c#6, d6, d#6, e6, f6, f#6, g6, g#6, a6, a#6, b6,
    c7, c#7, d7, d#7, e7, f7, f#7, g7, g#7, a7, a#7, b7
    ////////// Notice: some notes are out of range and ignored
    c8
    * pcm16 stereo sample " samples/grand piano/piano-p-c1.wav " 1493336 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-d#1.wav " 1516008 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-f#1.wav " 1509820 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-a1.wav " 1498120 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-c2.wav " 1481792 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-d#2.wav " 1449812 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-f#2.wav " 1439776 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-a2.wav " 1417312 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-c3.wav " 1261156 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-d#3.wav " 1303952 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-f#3.wav " 1243268 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-a3.wav " 1182584 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-c4.wav " 1153464 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-d#4.wav " 1079780 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-f#4.wav " 1025388 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-a4.wav " 953004 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-c5.wav " 918164 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-d#5.wav " 840008 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-f#5.wav " 753584 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-a5.wav " 698204 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-c6.wav " 676156 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-d#6.wav " 573092 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-f#6.wav " 512252 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-a6.wav " 425984 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-c7.wav " 404128 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-d#7.wav " 270348 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-f#7.wav " 246012 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-a7.wav " 224744 kB
    * pcm16 stereo sample " samples/grand piano/piano-p-c8.wav " 211276 kB
    ////////// Notice: some regions are not used, skipping:
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    23, 24, 25, 26, 27, 28, 29

    29 samples, 54225 kB written during 0.346783 seconds

    1 files converted in 0.351817 seconds

Batch conversion
~~~~~~~~~~~~~~~~

To convert more than one .SFZ file you can specify as many arguments to
Samplicity as you want. Or even use a wildcard

.. code:: bash

    samplicity "<SAMPLE 1>.sfz" "<SAMPLE 2>.sfz" "<SAMPLE 3>.sfz"
    samplicity *.sfz

Reconversion
~~~~~~~~~~~~

If there is corresponding to your sample pack .XI file, Samplicity won't
convert it again. To force reconversion, add ``--force`` attribute:

.. code:: bash

    samplicity "<SAMPLE NAME>.sfz" --force

Package
-------

Repository contains:

-  ``samplicity.py``
-  ``xi_reader.py`` — tool to verify your .XI if something went wrong.
   Usage:
   ``python "<PATH TO SAMPLICITY FOLDER>/xi_reader.py" "<SAMPLE NAME>.xi"``.
   It will show you full info, contained in .XI file (but not samples
   binary data). It is useful for bugtrack.
-  ``xi_specs.txt`` — specifications of eXtended Instrument edited and
   improved a bit. Thanks `Alex Zolotov <http://www.warmplace.ru/>`__
-  ``Cakewalk DevXchange - Specifications - sfz File Format.pdf`` —
   specifications of .SFZ saved from Cakewalk
   `website <http://www.cakewalk.com/DevXchange/article.aspx?aid=108>`__.

Notices and errors
------------------

-  **Notice: some notes are out of range and ignored** — .XI supports
   only 96 notes from C0 to B7, so some notes in your sample pack cannot
   fit in this range. Consider editing .SFZ file.
-  **Notice: some regions are overlapping and would be overwritten** —
   .SFZ format supports velocity maps. But .XI doesn't. Consider
   splitting your .SFZ file into separate files. For example, I've got
   ``Grand Piano (Piano).sfz`` and ``Grand Piano (Forte).sfz``
-  **24bit samples are not supported** — .XI and Sunvox don't support
   24bit sample format and there is no cooldown feature for them in
   Samplicity v0.3
-  **Too long envelope, shrinked to 512** — .XI does not support
   envelopes longer than 512 ticks (~10.24 seconds), so you instrument
   envelope was modified to fit this range
-  **Too many samples in file** — .XI does not support more than 128
   samples in instrument. Consider splitting your file or removing some.

