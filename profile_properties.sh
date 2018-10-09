#ROOT=/home/ppath
ROOT=/home/lgarreta/cloud/proteinpaths
ROOTPROP=$ROOT/03-Properties

BIN_PROPS=$ROOT/03-Properties/dev/bin
export PATH=$PATH:$BIN_PROPS

# Variable for rigidity analysis scripts using proflex program
export PROFLEX_HOME=$ROOT/03-Properties/dev/metrics/proflex/prog

# Variable for scripts manipulating PDBs using the MMTSB toolkit
export MMTSBDIR=$ROOT/03-Properties/dev/metrics/mmtsb

# Export bin for MMTSB 
export PATH=$PATH:$MMTSBDIR/bin:$MMTSBDIR/perl

# Global file for logging errors
export EVAL_LOGFILE=logs.log
export EVAL_ERRFILE=errors.log
export EVAL_TMPDIR=/dev/shm/tmp

# For structual similarity alphabet (encoder)
export EVAL_ALPHABET=$ROOTPROP/dev/metrics/xStructuralSimilarity/alphabet.sa
