import argparse
import os
import subprocess


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ot", "--origin",
                        help="original track")
    parser.add_argument("-t", "--tracks",
                        help="track list")
    args = parser.parse_args()
    return args.origin, args.tracks


def get_title(original_track):
    cmd_string = 'ffmpeg -i "%s" -f ffmetadata meta.txt' % original_track
    subprocess.call(cmd_string, shell=True)
    value = ''
    with open('meta.txt', 'r') as f:
        for line in f:
            # skip line with comment and empty lines
            if line.startswith(';') or len(line) <= 1:
                continue
            key, value1 = line.strip().split('=')
            if key=='title':
                value = value1
                print('title is %s' % value)
                break

    os.remove('meta.txt')

    return value


def main():
    """code is mainly based on https://unix.stackexchange.com/a/400032"""
    """split a music track into specified sub-tracks by calling ffmpeg from the shell"""

    # record command line args
    original_track, track_list = parse_arg()

    track_title = get_title(original_track)

    # create a template of the ffmpeg call in advance
    cmd_string = 'ffmpeg -i "{tr}" -acodec copy -ss {st} -to {en} -metadata title="{title}" {nm}.mp3'

    # read each line of the track list and split into start, end, name
    with open(track_list, 'r') as f:
        for line in f:
            # skip comment and empty lines
            if line.startswith('#') or len(line) <= 1:
                continue

            # create command string for a given track
            start, end, name, suffix = line.strip().split()
            suffix = suffix.replace('_', ' ')
            name = name.lower().replace(' ', '_')
            command = cmd_string.format(tr=original_track, st=start, en=end, nm=name, title='%s %s' % (track_title, suffix))

            # use subprocess to execute the command in the shell
            subprocess.call(command, shell=True)

    return None


if __name__ == '__main__':
    main()
