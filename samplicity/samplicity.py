#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Samplicity
__version__ = '0.5.1'
# April 12th, 2014
# Andrii Magalich
# https://github.com/ckald/Samplicity

import struct
import string
import os
import tempfile
import sys
import time
import math
import shutil
import numpy as np
from scikits.audiolab import Sndfile, play

from common import wrap, pad_name, path_insensitive

VERSION = 'Samplicity v' + __version__

OPTIONS = {}

cwd = os.getcwd() + '/'
tempdir = tempfile.mkdtemp()

scale = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
notes = []
for i in range(11):
    for note in scale:
        notes.append(note + str(i))


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
        self['sample_path'] = os.path.normpath(self['sample'])
        if not os.path.exists(self['sample_path']):
            self['sample_path'] = self['sample_path'].replace('\\', '/')
        self['sample_path'] = path_insensitive(self['sample_path'])
        self.read_wav(self['sample_path'])

    def read_wav(self, sample_path):

        sample = Sndfile(cwd + sample_path, 'r')
        sampling_rate = sample.samplerate
        channels = sample.channels
        encoding = sample.encoding
        frames_count = sample.nframes

        frames = sample.read_frames(frames_count, dtype=np.float32)
        sample.close()
        del sample

        if channels == 1:
            text_type = 'mono'
            sample_type = 0
        elif channels == 2:
            text_type = 'stereo'
            sample_type = 0b01100100
        else:
            text_type = '{0}-channels'.format(channels)

        if OPTIONS['verbose'] > 1:
            print "*", encoding, text_type, 'sample "', sample_path, '"', 4 * frames_count, 'kB'

        if OPTIONS['play_sound']:
            play(frames.astype(np.float64).T, sampling_rate)

        self.update({
            'sample_data': frames,
            'sample_type': sample_type,
            'channels': 2,
            'sample_bittype': 4
        })


class SFZ_instrument:
    group_settings = {}
    groups = [[]]
    regions = []
    curr = -1
    input_file = None
    output_file = None
    last_chunk = False
    notes_samples = [-1 for i in xrange(96)]

    class ParseError(Exception):
        pass

    def open(self, file):
        self.filename = file
        self.input_file = open(file, 'r')

        self.output_file = open(self.filename[:-4] + '.temp.xi', 'w')

    def close(self):
        self.input_file.close()

    def read(self):
        return self.input_file.readline()

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
            self.groups.append([])
            self.in_region = False
            self.group_settings = {}
        elif chunk == '<region>':  # it's a region - save the following and add group data
            if len(self.regions) >= 128:
                raise SFZ_instrument.ParseError(
                    "Too many samples in file: " + self.filename +
                    " (no more than 128 samples supported)"
                )
            self.regions.append(SFZ_region())
            self.curr += 1
            if self.in_group:
                self.regions[self.curr].update(self.group_settings)
                self.groups[-1].append(self.curr)

            self.in_region = True
        else:  # this should be the assignment
            segments = chunk.split('=')
            if len(segments) != 2:
                # maybe, we can just append this data to the previous chunk
                if self.last_chunk:
                    self.regions[self.curr][self.last_chunk[0]] += " " + segments[0]
                    segments = (self.last_chunk[0], self.regions[self.curr][self.last_chunk[0]])
                else:
                    raise SFZ_instrument.ParseError(
                        "Ambiguous spaces in SFZ file: " + self.filename
                    )
            if self.in_region:
                self.regions[self.curr][segments[0]] = segments[1]
            elif self.in_group:
                self.group_settings[segments[0]] = segments[1]
            self.last_chunk = segments

    def is_region_used(self, i):
        return any([j == i for j in self.notes_samples])

    def collect_samples(self, do_print=True):
        self.overlapping = []
        self.ignored = []

        for i, region in enumerate(self.regions):
            for note in region['notes']:
                if note < len(self.notes_samples) and note > -1:
                    if self.notes_samples[note] != -1:
                        self.overlapping.append(notes[note])
                    self.notes_samples[note] = i
                else:
                    self.ignored.append(notes[note])

        if do_print and OPTIONS['verbose']:
            if len(self.overlapping) > 0:
                wrap("/"*10 + " Notice: some regions are overlapping and would be overwritten")
                wrap(", ".join(self.overlapping))
            if len(self.ignored) > 0:
                wrap("/"*10 + " Notice: some notes are out of range and ignored")
                wrap(", ".join(set(self.ignored)))

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
        for i, region in enumerate(self.regions):
            region.validate()
            lo = notes.index(region['lokey'])
            hi = notes.index(region['hikey'])
            region['notes'] = range(lo, hi + 1)

        self.collect_samples()

        used_regions = []
        unused_regions = []
        for i, region in enumerate(self.regions):
            if self.is_region_used(i):
                region.load_audio()
                region['delta_sample'] = tempdir + str(time.clock()) + '.dat'
                region['sample_length'] = len(region['sample_data']) * region['channels']
                region['sample_data'].T.flatten().tofile(region['delta_sample'], format='f')
                region['sample_data'] = ''
                del region['sample_data']
                used_regions.append(region)
            else:
                unused_regions.append(i)

        self.regions = used_regions

        if unused_regions and OPTIONS['verbose']:
            wrap("/"*10 + ' Notice: some samples are not used, skipping:')
            wrap(", ".join([str(i+1) for i in unused_regions]))

        self.options = {}
        for region in self.regions:
            self.options.update(region)

        self.collect_samples(do_print=False)

    def write_header(self):
        # create xi file
        self.output_file.write(struct.pack(
            '21s22sb20sh',
            'Extended Instrument: ',
            (self.filename[:-4] + ' ' * 22)[:22], 0x1a, pad_name(VERSION, 20), 0x0
        ))

        self.output_file.write(struct.pack('96b', *(self.notes_samples)))

    def write_envelopes(self):
        stt = 50  # seconds-to-ticks converter
        # volume envelope
        volume_points = 0
        volume_ticks = 0
        volume_envelope = []
        if 'ampeg_attack' not in self.options:
            volume_level = 0x40
        else:
            volume_level = 0
        vol_sustain_point = 0

        volume_envelope.append(volume_ticks)
        if 'ampeg_delay' in self.options:
            volume_ticks += float(self.options['ampeg_delay']) * stt
            volume_points += 1
            volume_level = 0

            volume_envelope.append(volume_level)
            volume_envelope.append(volume_ticks)

        if 'ampeg_start' in self.options:
            volume_level = int(float(self.options['ampeg_start']) / 100 * stt)

        if 'ampeg_attack' in self.options:
            volume_ticks += int(float(self.options['ampeg_attack']) * stt)

        volume_envelope.append(volume_level)
        volume_points += 1

        if 'ampeg_hold' in self.options:
            volume_ticks += int(float(self.options['ampeg_hold']) * stt)
        else:
            volume_level = 0x40
        volume_envelope.append(volume_ticks)
        volume_envelope.append(volume_level)
        volume_points += 1

        if 'ampeg_decay' in self.options:
            volume_ticks += int(float(self.options['ampeg_decay']) * stt)
            volume_envelope.append(volume_ticks)

            if 'ampeg_sustain' in self.options:
                volume_envelope.append(int(float(self.options['ampeg_sustain']) / 100 * stt))
            else:
                volume_envelope.append(0)

            volume_points += 1

        if 'ampeg_sustain' in self.options:
            volume_level = int(float(self.options['ampeg_sustain']) / 100 * stt)
            volume_envelope.append(volume_ticks)
            volume_envelope.append(volume_level)
            volume_points += 1
            vol_sustain_point = volume_points - 1

        if 'ampeg_release' in self.options:
            volume_ticks += int(float(self.options['ampeg_release']) * stt)
            volume_level = 0x0
            volume_envelope.append(volume_ticks)
            volume_envelope.append(volume_level)
            volume_points += 1

        if volume_ticks > 512:
            for i in range(len(volume_envelope) / 2):
                volume_envelope[2 * i] = int(volume_envelope[2 * i] * 512 / volume_ticks)
            if OPTIONS['verbose']:
                wrap("/"*10 + " Too long envelope: "+str(volume_ticks)+" ticks, shrinked to 512")

        self.output_file.write(struct.pack('{0}h'.format(2 * volume_points), *(volume_envelope)))
        self.output_file.write(struct.pack('{0}h'.format(2 * (12 - volume_points)),
                               *(0 for i in range(2 * (12 - volume_points)))))

        self.output_file.write(struct.pack('24h', *(0 for i in range(24))))  # panning envelope

        self.output_file.write(struct.pack('b', volume_points))
        self.output_file.write(struct.pack('b', 0))

        self.output_file.write(struct.pack('b', vol_sustain_point))

        self.output_file.write(struct.pack('5b', *(0 for i in range(5))))

        volume_type = 0
        if volume_points > 0:
            volume_type += 0b1
        if vol_sustain_point > 0:
            volume_type += 0b10

        self.output_file.write(struct.pack('b', volume_type))
        self.output_file.write(struct.pack('b', 0))

        # vibrato type/sweep/depth/rate
        self.output_file.write(struct.pack('4b', *(0 for i in range(4))))

        # envelope data

        self.output_file.write(struct.pack('h', 0))  # volume fadeout
        self.output_file.write(struct.pack('22b', *(0 for i in range(22))))  # extended data

    def write_regions_meta(self):
        self.output_file.write(struct.pack('h', len(self.regions)))  # number of samples

        for region in self.regions:
            self.output_file.write(struct.pack(
                'i', region['sample_bittype'] * region['sample_length']))  # sample length
            self.output_file.write(struct.pack('2i', 0, 0))  # sample loop start and end
            # volume
            volume = 255
            if 'volume' in region:
                volume = math.floor(
                    255 * math.exp(float(region['volume']) / 10) / math.exp(0.6)
                )  # volume is in dB

            self.output_file.write(struct.pack('B', volume))

            self.output_file.write(struct.pack('b', int(region['tune'])))  # finetune (signed!)
            self.output_file.write(struct.pack('b', region['sample_type']))  # sample type

            #panning (unsigned!)
            pan = 128
            if 'pan' in region:
                pan = (float(region['pan']) + 100) * 255 / 200
            self.output_file.write(struct.pack('B', pan))

            key = region['pitch_keycenter'] if 'pitch_keycenter' in region else region['lokey']

            self.output_file.write(struct.pack(
                'b',
                1 - notes.index(key)
                + notes.index('e6')
            ))  # relative note - transpose c4 ~ 00

            sample_name = pad_name(os.path.split(region['sample_path'])[1], 22)

            self.output_file.write(struct.pack('b', len(sample_name.strip(' '))))
            self.output_file.write(struct.pack('22s', sample_name))

    def write_regions(self):
        for region in self.regions:
            df = open(region['delta_sample'], 'r')
            self.output_file.write(df.read())
            df.close()

            os.remove(region['delta_sample'])
            region = {}
            del region


def main():

    if len(sys.argv) < 2:
        print VERSION + ": .SFZ to .XI musical samples format converter"
        print "Usage:"
        print "    samplicity [--play] [--verbose N] [--force] file ..."
        print "See docs at https://github.com/ckald/Samplicity"
        sys.exit()

    OPTIONS['force'] = False
    if '--force' in sys.argv:
        OPTIONS['force'] = True
        del sys.argv[sys.argv.index('--force')]

    OPTIONS['play_sound'] = False
    if '--play' in sys.argv:
        OPTIONS['play_sound'] = True
        del sys.argv[sys.argv.index('--play')]

    OPTIONS['verbose'] = 1
    if '--verbose' in sys.argv:
        index = sys.argv.index('--verbose')
        OPTIONS['verbose'] = int(sys.argv[index + 1])
        del sys.argv[index]
        del sys.argv[index]

    start_time = time.clock()
    converted = 0
    try:
        for arg in sys.argv[1:]:
            if not os.path.exists(cwd + arg):
                print 'Warning: No file', arg, 'found, skipping'
            elif not os.path.exists(cwd + arg[:-4] + '.xi') or OPTIONS['force']:
                print '-' * 80
                print "Converting \"", arg, "\""
                print '-' * 80

                start = time.clock()
                instrument = SFZ_instrument(cwd + arg)

                instrument.write_header()
                instrument.write_envelopes()
                instrument.write_regions_meta()
                instrument.write_regions()

                print
                print len(instrument.regions), 'samples,',
                print instrument.output_file.tell() / 1024,
                print 'kB written during', time.clock() - start, 'seconds'
                print
                instrument.output_file.close()
                instrument = {}
                del instrument
                os.rename(cwd + arg[:-4] + '.temp.xi', cwd + arg[:-4] + '.xi')

                converted += 1
            else:
                print "File", arg, "is already converted!"

        print converted, "files converted in", time.clock() - start_time, "seconds"

    finally:
        try:
            shutil.rmtree(tempdir)  # delete directory
        except OSError, e:
            if e.errno != 2:  # code 2 - no such file or directory
                raise e

if __name__ == '__main__':
    main()
