import os
import subprocess
import glob
import autosub 
import time

def main():
    for file in glob.glob('*.mp3'):
        print('generating subtitle for %s' % file)
        if os.path.exists(file.replace('.mp3', '.srt')):
            print('skip existing file: %s' % file)
            continue
        autosub.generate_subtitles(file)
        time.sleep(10)
        # command = 'autosub -S en -D en "%s"' % file
        # subprocess.call(command, shell=True)


if __name__ == '__main__':
    main()
