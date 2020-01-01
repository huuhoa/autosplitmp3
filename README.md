# autosplitmp3
autosplit large mp3 file into smaller parts each start with a `Chapter`

## Usage

* **Step 1**: Prepare list of audio files (mp3 format) that contain multiple chapters to split
* **Step 2**: Run `python createsub.py` to create subtitle files for those audio files
* **Step 3**: Run `./subsplit.sh` to split audio files into smaller audio files that contain only single chapter

## Troubleshooting

When running on macosx, `createsub.py` may crash due to [known bug](https://bugs.python.org/issue35219). The symptom just looks like following:

```bash
+[__NSCFConstantString initialize] may have been in progress in another thread no such process ...
+[__NSCFConstantString initialize] may have been in progress in another thread no such process ...
+[__NSCFConstantString initialize] may have been in progress in another thread no such process ...
+[__NSCFConstantString initialize] may have been in progress in another thread no such process ...
```

The quick work-around is to run `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` before starting step 2
