# Changelog

### v0.5 April 12th, 2014

* Various WAV types support thanks to scikits.audiolab.SndFile (including 24bit!)
* Runtime option "--play": play all samples converted
* Runtime option "--verbose %": set output verbosity to % (0/1/2)
* Excess samples are no longer added to resulting .XI file
* New notice about omitted excess samples
* Conversion speed increased dramatically

### v0.4 September 27th, 2012

* Added sample count constraint (no more than 128 per file) – -1 observed error
* Moved temp files to system temp dir – job done clear now
* Fixed envelope length and seconds-to-ticks conversion parameter — no more SunVox crashes