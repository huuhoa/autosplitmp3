# autosplitmp3
autosplit large mp3 file into smaller parts each start with a `Chapter`

## Usage

* **Step 1**: Prepare list of audio files (mp3 format) that contain multiple chapters to split
* **Step 2**: Run `python createsub.py` to create subtitle files for those audio files
* **Step 3**: Run `./subsplit.sh` to split audio files into smaller audio files that contain only single chapter
