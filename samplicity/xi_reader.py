from ctypes import *
import struct
import sys

def main():

    f = open(sys.argv[1])
    file = f.read()

    pos = 0

    xi, instrument, tracker, major_version, minor_version = struct.unpack('21s22sx20s2b', file[pos:(pos + 0x42)])
    pos += 0x42
    print '/' * 80
    print 'Sample info'
    print xi, instrument, tracker, major_version, minor_version

    note_samples = struct.unpack('96b', file[pos:(pos + 0x60)])
    pos += 0x60
    print '/' * 80
    print 'Samples-notes map'
    print note_samples

    volume_envelope = struct.unpack('24h', file[pos:(pos + 0x30)])
    pos += 0x30
    print '/' * 80
    print 'Volume envelope:'
    print volume_envelope
    panning_envelope = struct.unpack('24h', file[pos:(pos + 0x30)])
    pos += 0x30
    print '/' * 80
    print 'Panning envelope:'
    print panning_envelope

    (
        volume_points_number, panning_points_number,
        volume_sustain_point, volume_loop_start_point, volume_loop_end_point,
        panning_sustain_point, panning_loop_start_point, panning_loop_end_point,
        volume_type, panning_type, vibrato_type, vibrato_sweep, vibrato_depth, vibrato_rate
    ) = struct.unpack('14b', file[pos:(pos + 0xe)])
    pos += 0xe
    print '/' * 80
    print 'Volume and sustain points numbers:', volume_points_number, panning_points_number
    print 'Volume sustain point:', volume_sustain_point
    print 'Volume loop start and end points:', volume_loop_start_point, volume_loop_end_point
    print '/' * 80
    print 'Panning sustain point:', panning_sustain_point
    print 'Panning loop start and end points:', panning_loop_start_point, panning_loop_end_point
    print 'Volume type:', volume_type
    print 'Panning type:', panning_type
    print 'Vibrato type, weep, depth and rate:', vibrato_type, vibrato_sweep, vibrato_depth, vibrato_rate

    volume_fadeout = struct.unpack('h', file[pos:(pos + 0x2)])[0]
    pos += 0x2
    print 'Volume fadeout:', volume_fadeout

    extended_info = struct.unpack('22b', file[pos:(pos + 0x16)])
    pos += 0x16
    print '/' * 80
    print 'Extended info (mostly zeros):'
    print extended_info

    pos = 0x128
    samples_number = struct.unpack('h', file[pos:(pos + 0x2)])[0]
    print '/' * 80
    print 'Samples count: ', samples_number

    print '/' * 80
    print 'Sample data:'

    pos = 0x12a
    samples = range(samples_number)
    for i in range(samples_number):
        samples[i] = {}
        (
            samples[i]['length'], samples[i]['loop_start'], samples[i]['loop_length'],
            samples[i]['volume'], samples[i]['finetune'], samples[i]['type'],
            samples[i]['panning'], samples[i]['transpose'], samples[i]['sample_name_length'],
            samples[i]['sample_name']
        ) = struct.unpack('3i6b22s', file[pos:(pos + 40)])
        pos += 40
        print samples[i]

if __name__ == '__main__':
    main()
