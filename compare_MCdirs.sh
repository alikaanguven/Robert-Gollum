#!/bin/bash

run_compareK(){

    kind=$1
    sample=$2
    shift
    shift
    SIGNAL=$HISTDIR/${sample}.root
    
    OUTDIR=$HISTDIR/plots/compare_dirs/${kind}/${sample}

    PDFDIR=$OUTDIR/pdf
    PNGDIR=$OUTDIR/png
    LOGPNGDIR=$OUTDIR/logpng

    mkdir -p $PDFDIR
    mkdir -p $PNGDIR
    mkdir -p $LOGPNGDIR


    python3 compare_modified.py                                                      \
    --input $SIGNAL                                                                  \
    --dirs $@                                                                        \
    --nice $@                                                                        \
    --output $OUTDIR                                                                 \
    --scale

    mv $OUTDIR/*.pdf            $PDFDIR
    mv $OUTDIR/*log.png         $LOGPNGDIR
    mv $OUTDIR/*.png            $PNGDIR
}

HISTDIR=/scratch-cbe/users/alikaan.gueven/Gollum/plots/test4/TT2lUnbinned_2016


run_compareK "" TT2lUnbinned_2016  gluon_0_evt gluon_1_evt gluon_2_evt gluon_3_evt gluon_4_evt


