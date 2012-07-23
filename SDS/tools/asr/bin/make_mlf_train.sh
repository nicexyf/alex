#!/bin/bash
# Make the train MLF
#
# After we do prep_train.sh, we want to create a word level MLF for all
# the files that were succefully converted to MFC files.

# Create a file listing all the MFC files in the train directory
find $TRAIN_DATA -iname '*.mfc' > $WORK_DIR/train_mfc_files.txt

# Now create the MLF file using a script, we prune out anything that
# has words that aren't in our dictionary, producing a MLF with only
# these files and a corresponding script file.
if [[ $7 != "prune" ]]
then
  python $TRAIN_SCRIPTS/CreateMLF.py "-" $WORK_DIR/train_words.mlf $WORK_DIR/train.scp $TRAIN_DATA $TRAIN_DATA_SOURCE'/*.trn' > $LOG_DIR/train_missing_words.log
else
  python $TRAIN_SCRIPTS/CreateMLF.py $WORK_DIR/dict_full $WORK_DIR/train_words.mlf $WORK_DIR/train.scp $TRAIN_DATA $TRAIN_DATA_SOURCE'/*.trn' > $LOG_DIR/train_missing_words.log
fi