#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Samplicity v0.4
# September 27th, 2012
# © Magalich Andrew
# https://github.com/ckald/Samplicity

import struct
import string
import os
import tempfile
import wave
import sys
import sndhdr
from array import array
import time
import math
import shutil


if len(sys.argv) < 2:
    print "No input file specified"
    sys.exit()

if '--force' in sys.argv:
    force = True
    del sys.argv[sys.argv.index('--force')]
else:
    force = False

cwd = os.getcwd() + '/'

tempdir = tempfile.mkdtemp()

scale = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
notes = []
for i in range(11):
    for note in scale:
        notes.append(note + str(i))


def pad_name(name, length, pad=' ', dir='right'):
    if dir == 'right':
        return (name + pad * length)[:length]
    else:
        return (name + pad * length)[-length:]


def read_wav(sample_path):
    (format, sampling_rate, channels, frames_count, bits_per_sample) = sndhdr.what(cwd + sample_path)
    sample = wave.open(cwd + sample_path)

    if frames_count == -1:
        frames_count = sample.getnframes()

    if format != 'wav':
        print 'This is not wav file:', sample_path

    if channels == 1:
        text_type = 'mono'
        sample_type = 0
    elif channels == 2:
        text_type = 'stereo'
        sample_type = 0b01010000
    else:
        text_type = '{0}-channels'.format(channels)

    byte = bits_per_sample / 8  # sample.getsampwidth()

    if byte == 3:  # for some reason
        print "*", (byte * 8), 'bit', text_type, 'sample "', sample_path, '"', byte * frames_count / 2 ** 9, 'kB'
    else:
        print "*", (byte * 8), 'bit', text_type, 'sample "', sample_path, '"', byte * frames_count / 2 ** 10, 'kB'

    if byte == 1:
        bittype = 'B'
        scissors = 0xFF
    elif byte == 2:
        bittype = 'H'
        scissors = 0xFFFF
    elif byte == 3:
        scissors = 0xFFFFFF
        bittype = 'I'
        print "/" * 80
        print '24bit samples are not supported'
        print "/" * 80
        # return ([], sample_type)
    elif byte == 4:
        scissors = 0xFFFFFFFF
        bittype = 'I'

    delta = 0
    frames = []
    total_len = byte * frames_count

    if byte == 3:  # need to treat this independently for some reason. maybe, python.wave bug?
        frames = struct.unpack("<{0}B".format(total_len * 2), sample.readframes(total_len))
        # frames = []
        # for i in range(total_len / 2):
        #     bytes = struct.unpack('<6B', sample.readframes(1))
        #     for j in range(len(bytes) / 3):
        #         frames.append(bytes[j] + bytes[j + 1] << 0xFF + bytes[j + 2] << 0xFFFF)
                # 'cause little-endian
        # bytes = struct.unpack("<{0}".format(total_len / 2) + bittype, sample.readframes(total_len))
        # for i in range(total_len / 3):
        #     frames.append(bytes[i] + bytes[i + 1] << 0xFF + bytes[i + 2] << 0xFFFF)
            # 'cause little-endian
    else:
        for i in range(total_len / 2 ** 9 + 1):
            r = sample.readframes(2 ** 9)
            frames[len(frames):] = struct.unpack("<{0}".format(len(r) / byte) + bittype, r)

    sample.close()
    del sample

    ret = array(bittype)
    for frame in frames:
        original = frame
        frame = (frame - delta) & scissors
        delta = original
        ret.append(frame)

    frames = []
    del frames
    return (ret, sample_type, byte)


class SFZ_region(dict):
    def validate(self):
        if 'tune' not in self:
            self['tune'] = 0
        if 'key' in self:
            self['pitch_keycenter'] = self['key']
            self['lokey'] = self['key']
            self['hikey'] = self['key']
        if 'pitch_keycenter' in self:
            if 'lokey' not in self:
                self['lokey'] = self['pitch_keycenter']
            if 'hikey' not in self:
                self['hikey'] = self['pitch_keycenter']

        for key in ('pitch_keycenter', 'lokey', 'hikey'):
            if key in self and self[key].isdigit():
                self[key] = notes[int(self[key])]

    def load_audio(self):
        self['sample_path'] = self['sample'].replace('\\', '/')
        if self['sample_path'][-4:] == '.wav':
            (self['sample_data'], self['sample_type'], self['sample_bittype']) = read_wav(self['sample_path'])


class SFZ_instrument:
    group = {}
    regions = []
    curr = -1
    file = ''
    last_chunk = False

    def open(self, file):
        self.filename = file
        self.file = open(file, 'r')
        return self.file

    def close(self):
        self.file.close()

    def read(self):
        return self.file.readline()

    def parse_line(self, line):
        line = string.strip(line, ' \r\n')
        comment_pos = line.find('//')  # remove comments
        if comment_pos >= 0:
            line = line[:comment_pos]
        if len(line) == 0:
            return  # blank line - nothing to do here
        # now split line in chunks by spaces
        chunks = line.split(' ')
        for chunk in chunks:
            if len(chunk) > 0:
                self.parse_chunk(chunk)

    def parse_chunk(self, chunk):
        if chunk == '<group>':  # it's a group - lets remember the following
            self.in_group = True
            self.in_region = False
            self.group = {}
        elif chunk == '<region>':  # it's a region - save the following and add group data
            if len(self.regions) >= 128:
                print "Too many samples in file:", self.filename, " (no more than 128 samples supported)"
                sys.exit()
            self.regions.append(SFZ_region())
            self.curr += 1
            if self.in_group:
                self.regions[self.curr].update(self.group)

            self.in_region = True
        else:  # this should be the assignment
            segments = chunk.split('=')
            if len(segments) != 2:
                # maybe, we can just append this data to the previous chunk
                if self.last_chunk != False:
                    self.regions[self.curr][self.last_chunk[0]] += " " + segments[0]
                    segments = (self.last_chunk[0], self.regions[self.curr][self.last_chunk[0]])
                else:
                    print "Ambiguous spaces in SFZ file:", self.filename
                    sys.exit()
            if self.in_region:
                self.regions[self.curr][segments[0]] = segments[1]
            elif self.in_group:
                self.group[segments[0]] = segments[1]
            self.last_chunk = segments

    def __init__(self, file):
        self.open(file)

        self.regions = []
        self.group = {}
        self.last_chunk = False
        self.curr = -1
        self.in_region = -1
        self.in_group = False

        line = self.read()
        while len(line) > 0:
            self.parse_line(line)
            line = self.read()

        # complete samples info
        for region in self.regions:
            region.validate()
            lo = notes.index(region['lokey'])
            hi = notes.index(region['hikey'])
            region['notes'] = range(lo, hi + 1)
            region.load_audio()
            region['delta_sample'] = tempdir + str(time.clock()) + '.dat'
            region['sample_length'] = len(region['sample_data'])
            df = open(region['delta_sample'], 'w')

            if region['sample_bittype'] == 1:
                df.write(struct.pack('{0}B'.format(len(region['sample_data'])), *(region['sample_data'])))
            elif region['sample_bittype'] == 2:
                df.write(struct.pack('{0}H'.format(len(region['sample_data'])), *(region['sample_data'])))
            elif region['sample_bittype'] == 3:
                for byte in region['sample_data']:
                    df.write(struct.pack('3B', byte & 0xFF0000 >> 0xFFFF, byte & 0xFF00 >> 0xFF, byte & 0xFF))
            elif region['sample_bittype'] == 4:
                df.write(struct.pack('{0}I'.format(len(region['sample_data'])), *(region['sample_data'])))

            df.close()
            region['sample_data'] = ''
            del region['sample_data']


def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line) - line.rfind('\n') - 1
                         + len(word.split('\n', 1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )


def magic(filename):
    start = time.clock()
    instrument = SFZ_instrument(cwd + filename)

    file = open(cwd + filename[:-4] + '.temp.xi', 'w')
    # create xi file
    file.write(struct.pack('21s22sb20sh',\
        'Extended Instrument: ', (filename[:-4] + ' ' * 22)[:22], 0x1a,\
        pad_name('Samplicity v0.3', 20), 0x0))

    notes_samples = [0 for i in range(96)]

    overlapping = []
    ignored = []

    i = 0

    for region in instrument.regions:
        for note in region['notes']:
            if note < len(notes_samples) and note > -1:
                if notes_samples[note] != 0:
                    overlapping.append(notes[note])
                notes_samples[note] = i
            else:
                ignored.append(notes[note])
        i += 1

    if len(overlapping) > 0:
        print "/" * 80
        print wrap("Notice: some regions are overlapping and would be overwritten", 80)
        print wrap(str(overlapping), 80)
        print "/" * 80
    if len(ignored) > 0:
        print "/" * 80
        print wrap("Notice: some notes are out of range and ignored", 80)
        print wrap(str(ignored), 80)
        print "/" * 80

    file.write(struct.pack('96b', *(notes_samples)))

    stt = 50  # seconds-to-ticks converter
# volume envelope
    volume_points = 0
    volume_ticks = 0
    volume_envelope = []
    if 'ampeg_attack' not in region:
        volume_level = 0x40
    else:
        volume_level = 0
    vol_sustain_point = 0

    #file.write(struct.pack('h', volume_ticks))
    volume_envelope.append(volume_ticks)
    if 'ampeg_delay' in region:
        volume_ticks += float(region['ampeg_delay']) * stt
        volume_points += 1
        volume_level = 0

        #file.write(struct.pack('h', volume_level))
        volume_envelope.append(volume_level)
        #file.write(struct.pack('h', volume_ticks))
        volume_envelope.append(volume_ticks)

    if 'ampeg_start' in region:
        volume_level = int(float(region['ampeg_start']) / 100 * stt)

    if 'ampeg_attack' in region:
        volume_ticks += int(float(region['ampeg_attack']) * stt)

    #file.write(struct.pack('h', volume_level))
    volume_envelope.append(volume_level)
    volume_points += 1

    if 'ampeg_hold' in region:
        volume_ticks += int(float(region['ampeg_hold']) * stt)
    else:
        volume_level = 0x40
    #file.write(struct.pack('h', volume_ticks))
    volume_envelope.append(volume_ticks)
    #file.write(struct.pack('h', volume_level))
    volume_envelope.append(volume_level)
    volume_points += 1

    if 'ampeg_decay' in region:
        volume_ticks += int(float(region['ampeg_decay']) * stt)
        #file.write(struct.pack('h', volume_ticks))
        volume_envelope.append(volume_ticks)

        if 'ampeg_sustain' in region:
            #file.write(struct.pack('h', int(float(region['ampeg_sustain']) / 100 * stt)))
            volume_envelope.append(int(float(region['ampeg_sustain']) / 100 * stt))
        else:
            #file.write(struct.pack('h', 0))
            volume_envelope.append(0)

        volume_points += 1

    if 'ampeg_sustain' in region:
        volume_level = int(float(region['ampeg_sustain']) / 100 * stt)
        #file.write(struct.pack('h', volume_ticks))
        volume_envelope.append(volume_ticks)
        #file.write(struct.pack('h', volume_level))
        volume_envelope.append(volume_level)
        volume_points += 1
        vol_sustain_point = volume_points - 1

    if 'ampeg_release' in region:
        volume_ticks += int(float(region['ampeg_release']) * stt)
        volume_level = 0x0
        #file.write(struct.pack('h', volume_ticks))
        volume_envelope.append(volume_ticks)
        #file.write(struct.pack('h', volume_level))
        volume_envelope.append(volume_level)
        volume_points += 1

    if volume_ticks > 512:
        for i in range(len(volume_envelope) / 2):
            volume_envelope[2 * i] = int(volume_envelope[2 * i] * 512 / volume_ticks)
        print "/" * 80
        print "Too long envelope:", volume_ticks, "ticks, shrinked to 512"
        print "/" * 80

    file.write(struct.pack('{0}h'.format(2 * volume_points), *(volume_envelope)))
    file.write(struct.pack('{0}h'.format(2 * (12 - volume_points)), *(0 for i in range(2 * (12 - volume_points)))))
    #envelope = [0, 64, 4, 50, 8, 36, 13, 28, 20, 22, 33, 18, 47, 14, 62, 8, 85, 4, 161, 0, 100, 0, 110, 0]
    #file.write(struct.pack('24h', *(envelope)))
    file.write(struct.pack('24h', *(0 for i in range(24))))  # panning envelope

    file.write(struct.pack('b', volume_points))
    file.write(struct.pack('b', 0))

    file.write(struct.pack('b', vol_sustain_point))

    file.write(struct.pack('5b', *(0 for i in range(5))))

    volume_type = 0
    if volume_points > 0:
        volume_type += 0b1
    if vol_sustain_point > 0:
        volume_type += 0b10

    file.write(struct.pack('b', volume_type))
    file.write(struct.pack('b', 0))

    # vibrato type/sweep/depth/rate
    file.write(struct.pack('4b', *(0 for i in range(4))))

# envelope data
    #file.write(struct.pack('b'))

    file.write(struct.pack('h', 0))  # volume fadeout
    file.write(struct.pack('22b', *(0 for i in range(22))))  # extended data
    file.write(struct.pack('h', len(instrument.regions)))  # number of samples

    for region in instrument.regions:
        file.write(struct.pack('i', region['sample_bittype'] * region['sample_length']))  # sample length
        file.write(struct.pack('2i', 0, 0))  # sample loop start and end
        # volume
        if 'volume' in region:
            file.write(struct.pack('B', math.floor(255 * math.exp(float(region['volume']) / 10) / math.exp(0.6))))  # 'cause volume is in dB
        else:
            file.write(struct.pack('B', 255))

        file.write(struct.pack('b', int(region['tune'])))  # finetune (signed!)
        file.write(struct.pack('b', region['sample_type']))  # sample type

        #panning (unsigned!)
        if 'pan' in region:
            file.write(struct.pack('B', (float(region['pan']) + 100) * 255 / 200))
        else:
            file.write(struct.pack('B', 128))

        if 'pitch_keycenter' in region:
            file.write(struct.pack('b',\
             1 - notes.index(region['pitch_keycenter'])\
             + notes.index('e6')))  # relative note - transpose c4 ~ 00
        else:
            file.write(struct.pack('b',\
             1 - notes.index(region['lokey'])\
             + notes.index('e6')))  # relative note - transpose c4 ~ 00

        sample_name = pad_name(os.path.split(region['sample_path'])[1], 22)

        file.write(struct.pack('b', len(sample_name.strip(' '))))
        file.write(struct.pack('22s', sample_name))

    for region in instrument.regions:
        df = open(region['delta_sample'], 'r')
        file.write(df.read())
        df.close()

        os.remove(region['delta_sample'])
        region = {}
        del region

    print len(instrument.regions), 'samples'
    print file.tell() / 1024, 'kB written in file "', filename, '" during', time.clock() - start, 'seconds'
    file.close()
    instrument = {}
    del instrument
    os.rename(cwd + filename[:-4] + '.temp.xi', cwd + filename[:-4] + '.xi')

start_time = time.clock()
converted = 0

try:
    for arg in sys.argv[1:]:
        if not os.path.exists(cwd + arg[:-4] + '.xi') or force:
            print '-' * 80
            print "Converting \"", arg, "\""
            print '-' * 80
            magic(arg)
            converted += 1
        else:
            print "File", arg, "is already converted!"

    print ''
    print converted, "files converted in", time.clock() - start_time, "seconds"

finally:
    try:
        shutil.rmtree(tempdir)  # delete directory
    except OSError, e:
        if e.errno != 2:  # code 2 - no such file or directory
            raise
