# mimic
Simple toy experiments written in Python to generate sketches from pictures
using figures.
The sketches are generated with heuristic algorithms which minimize the 
difference between the target image and the candidate sketches.

## circles

Usage:
```
$python circles.py input.jpg output.jpg -e 100
```

This will generate an sketch of `input.jpg` using only circles. The `-e` 
parameter controls the number of guesses done by the heuristic algorithm.

## lemniscate

Usage:
```
$python lemniscate.py --width 800 --height 600
```

Interactive lemniscate design. Mouse click sets a new focus. Pressing 'r' removes
the last added focus. 'c' will erase all foci. 's' will save the image to disk.