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


    python3 compare.py                                                               \
    --input $SIGNAL                                                                  \
    --dirs $@                                                                        \
    --nice $@                                                                        \
    --output $OUTDIR                                                                 \
    --scale

    mv $OUTDIR/*.pdf            $PDFDIR
    mv $OUTDIR/*log.png         $LOGPNGDIR
    mv $OUTDIR/*.png            $PNGDIR
}

HISTDIR=/scratch-cbe/users/alikaan.gueven/Gollum/plots/test1/TT2lUnbinned_2016


run_compareK "" TT2lUnbinned_2016  gluon20_evt gluon40_evt gluon60_evt gluon80_evt gluon100_evt


