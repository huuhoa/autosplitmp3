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


def read_srt(src):
    tracks = []
    # read each line of the track list and split into start, end, name
    with open(src, 'r') as f:
        line_index = 0
        seg_index = 0
        seg_time = ''
        seg_content = ''
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
                seg_index = line.strip()
                continue
            if line_index == 2: # subtitle time start-end
                seg_time = line.strip()
                continue

            # line_index == 3: - subtitle content
            seg_content = line.strip()
            tracks.append((seg_index, seg_time, seg_content))
            line_index = 0
        # end for

    return tracks


def transform_tracks(srt_segments, prefix):
    start = '00:00:00'
    current_chapter = ''
    filename = ''
    tracks = []
    for _, seg_time, content in srt_segments:
        if not content.startswith('Chapter '):
            continue
        line_timing, _, _ = seg_time.split(',')

        # encounter first chapter, should not append track since it is just the begining
        if len(current_chapter) <= 1:
            filename, current_chapter = get_filename_title(prefix, "begin")

        # begining of new chapter, should record current chapter
        append_track(tracks, start, line_timing, filename, current_chapter)

        # starting new chapter
        filename, current_chapter = get_filename_title(prefix, content)
        start = line_timing

    # end for

    # last chapter
    if len(current_chapter) > 1:
        _, seg_time, _ = srt_segments[-1]
        line_timing, _, _ = seg_time.split(',')
        append_track(tracks, start, line_timing, filename, current_chapter)
    return tracks


def main():
    """create track list file from subtitle"""

    # record command line args
    subtitle, track_list, prefix = parse_arg()
    srt_segments = read_srt(subtitle)
    tracks = transform_tracks(srt_segments, prefix)
    # # read each line of the track list and split into start, end, name
    # with open(subtitle, 'r') as f:
    #     start = '00:00:00'
    #     current_chapter = ''
    #     current_file = ''
    #     line_index = 0
    #     filename = ''
    #     for line in f:
    #         # skip comment
    #         if line.startswith('#'):
    #             continue

    #         # empty line
    #         if len(line) <= 1:
    #             line_index = 0
    #             continue

    #         # not empty lines
    #         line_index += 1
    #         # skip line numbering
    #         if line_index == 1:
    #             continue
    #         if line_index == 2: # subtitle time start-end
    #             line_timing, _, _ = line.strip().split(',')
    #             continue

    #         # line_index == 3: - subtitle content
    #         if not line.startswith('Chapter '):
    #             continue

    #         # encounter first chapter, should not append track since it is just the begining
    #         if len(current_chapter) <= 1:
    #             filename, current_chapter = get_filename_title(prefix, line)
    #             continue

    #         # begining of new chapter, should record current chapter
    #         append_track(tracks, start, line_timing, filename, current_chapter)

    #         # starting new chapter
    #         filename, current_chapter = get_filename_title(prefix, line)
    #         start = line_timing

    #     # end for

    #     # last chapter
    #     if len(current_chapter) > 1:
    #         append_track(tracks, start, line_timing, filename, current_chapter)

    write_track_list(tracks, track_list)


if __name__ == '__main__':
    main()
