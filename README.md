# Tutorial for making figures

This tutorial will cover my (Michael's) workflow for generating figures in `python`. It is completely based on Jan-Matthis' workflow. The figures that are created in this tutorial follow the style of the ones in the following two papers:
- [Training deep neural density estimators to identify mechanistic models of neural dynamics](https://elifesciences.org/articles/56261)
- [Energy efficient network activity from disparate circuit parameters](https://www.biorxiv.org/content/10.1101/2021.07.30.454484v4.abstract)

## Goals
- Consistent fontsizes, ticksizes, etc.
- Generating figures completely from `python` and the command line, without using `inkscape` or `illustrator`.

## Ingredients
Part 0: Recommended filestructure (optional)
Part 1: Using a `matplotlib` stylefile
Part 2: Using `svgutils` to compose multipanel figures
Part 3: Using `invoke` to convert `svg` to `png` or `pdf`
Part 4: Syncing the `files` with overleaf from the commandline

## Part 0: Recommended filestructure (optional)
I recommend using the following filestructure within your repo:
```
├── paper
│   ├── fig1
│   │   ├── svg
│   │   ├── fig
│   │   ├── notebooks
│   │   │   ├── 01_assemble_figure.ipynb
│   │   │   ├── 01_assemble_appendix.ipynb
│   └── fig2
│   └── fig3
├── results
├── setup.py
├── name_of_your_project
```
All the code you import is in the `name_of_your_project` folder. The `paper` folder takes care of generating the figures. I recommend one subfolder for each figure (e.g. `fig1`). Each of these subfolders contains the `notebooks` that are used to generate the figure, an `svg` folder in which the individual panels will lie (see later), and a `fig` folder which contains the final figures that are used in your paper.

## Part 1: Using a `matplotlib` stylefile
In order to make your figures look pretty, you can use a stylefile. This repo constains the stylefile which we used for the papers mentioned above (filename: `.matplotlibrc`). This file defines the linewidths, ticklengths, removes the top and right axes, etc. You can use the file as such:
```python
import matplotlib as mpl
import matplotlib.pyplot as plt

with mpl.rc_context(fname=".matplotlib"):
    plt.plot([0.0, 1.0], [1.0, 2.0])
```

## Part 2: Using `svgutils` to compose multipanel figures
In science, you often want to be able to flexibly compose multi-panel figures and add small letters (`a`, `b`, ...) to the figure. You can do this with [svgutils](https://svgutils.readthedocs.io/en/latest/). First, save each panel individually as `svg`:
```python
import matplotlib as mpl
import matplotlib.pyplot as plt

with mpl.rc_context(fname=".matplotlib"):
    plt.plot([0.0, 1.0], [1.0, 2.0])
    plt.savefig("panel_a.svg")
    
with mpl.rc_context(fname=".matplotlib"):
    plt.plot([1.0, 2.0], [1.0, -2.0])
    plt.savefig("panel_b.svg")
```

Second, we use `svgutils` to compose the multipanel figure:
```python
from svgutils.compose import *

# > Inkscape pixel is 1/90 of an inch, other software usually uses 1/72.
# > http://www.inkscapeforum.com/viewtopic.php?f=6&t=5964
svg_scale = 1.25  # set this to 1.25 for Inkscape, 1.0 otherwise

# Panel letters in Helvetica Neue, 12pt, Medium
kwargs_text = {'size': '12pt', 'font': 'Arial', 'weight': '800'}

f = Figure("20.3cm", "14.1cm",
           
    Panel(
          SVG("panel_a.svg").scale(svg_scale),
          Text("a", -5, 2.0, **kwargs_text),
    ).move(5, 0),
    
    Panel(
          SVG("panel_b.svg").scale(svg_scale),
          Text("b", -5, 2.0, **kwargs_text),
    ).move(5, 0),
)

!mkdir -p fig
f.save("fig.svg")
svg('fig.svg')

## Part 3: Using `invoke` to convert `svg` to `png` or `pdf`
We now have our final figure as `svg` file. For `overleaf`, we have to convert it to `png` or `pdf`. 
