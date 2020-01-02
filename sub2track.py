import argparse


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subtitle",
                        help="subtitle path")
    parser.add_argument("-t", "--tracks",
                        help="track list")
    parser.add_argument("-p", "--prefix",
                        help="prefix")
    args = parser.parse_args()
    return args.subtitle, args.tracks, args.prefix.replace(' ', '_')


def write_track_list(tracks, track_list):
    with open(track_list, 'w') as file:
        file.write('\n'.join(tracks))


def get_filename_title(prefix, line):
    title = line.strip().replace(' ', '_')
    filename = '%s_%s' % (prefix, title.lower().replace(' ', '_'))
    return filename, title


def append_track(tracks, start, line_timing, filename, current_chapter):
    track = '%s %s %s %s' % (start, line_timing, filename, current_chapter)
    tracks.append(track)
    print('track: %s' % track)


def main():
    """create track list file from subtitle"""

    # record command line args
    subtitle, track_list, prefix = parse_arg()

    tracks = []
    # read each line of the track list and split into start, end, name
    with open(subtitle, 'r') as f:
        start = '00:00:00'
        current_chapter = ''
        current_file = ''
        line_index = 0
        filename = ''
        for line in f:
            # skip comment
            if line.startswith('#'):
                continue

            # empty line
            if len(line) <= 1:
                line_index = 0
                continue

            # not empty lines
            line_index += 1
            # skip line numbering
            if line_index == 1:
                continue
            if line_index == 2: # subtitle time start-end
                line_timing, _, _ = line.strip().split(',')
                continue

            # line_index == 3: - subtitle content
            if not line.startswith('Chapter'):
                continue

            # encounter first chapter, should not append track since it is just the begining
            if len(current_chapter) <= 1:
                filename, current_chapter = get_filename_title(prefix, line)
                continue

            # begining of new chapter, should record current chapter 
            append_track(tracks, start, line_timing, filename, current_chapter)

            # starting new chapter
            filename, current_chapter = get_filename_title(prefix, line)
            start = line_timing

        # end for

        # last chapter
        if len(current_chapter) > 1:
            append_track(tracks, start, line_timing, filename, current_chapter)

    write_track_list(tracks, track_list)
    return None


if __name__ == '__main__':
    main()
