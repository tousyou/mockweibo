#!/bin/sh
# the diff program
DIFF="vimdiff"

LEFT=${6}
RIGHT=${7}
$DIFF $LEFT $RIGHT
