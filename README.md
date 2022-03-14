# Tutorial for making figures

This tutorial will cover my (Michael's) workflow for generating figures in `python`. It is completely based on Jan-Matthis' workflow. The figures that are created in this tutorial follow the style of the ones in the following two papers:  
- [Training deep neural density estimators to identify mechanistic models of neural dynamics](https://elifesciences.org/articles/56261)  
- [Energy efficient network activity from disparate circuit parameters](https://www.biorxiv.org/content/10.1101/2021.07.30.454484v4.abstract)

## Goals
- Consistent fontsizes, ticksizes, etc.  
- Generating figures completely from `python` and the command line, without using `inkscape` or `illustrator`.

## Ingredients
We will go through the workflow in five parts. Note that all code that is described in these parts can also be found in this repo.
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
├── tasks.py
├── results
├── name_of_your_project
├── setup.py
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
    plt.savefig("../svg/panel_a.svg")
    
with mpl.rc_context(fname=".matplotlib"):
    plt.plot([1.0, 2.0], [1.0, -2.0])
    plt.savefig("../svg/panel_b.svg")
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
          SVG("../svg/panel_a.svg").scale(svg_scale),
          Text("a", -5, 2.0, **kwargs_text),
    ).move(5, 0),
    
    Panel(
          SVG("../svg/panel_b.svg").scale(svg_scale),
          Text("b", -5, 2.0, **kwargs_text),
    ).move(5, 0),
)

!mkdir -p fig
f.save("../fig/fig.svg")
svg("../fig/fig.svg")
```

## Part 3: Using `invoke` to convert `svg` to `png` or `pdf`

We now have our final figure as `svg` file. For `overleaf`, we have to convert it to `png` or `pdf`. Of course, you could just open inkscape, import the `svg`, and export it as `png`. However, this is a bit tedious. Instead, we would like to do this from the commandline. I recommend to use [invoke](https://www.pyinvoke.org/) to convert `svg` to `png` and `pdf`. Paste the following into a file `tasks.py` in the root folder of your repo and adapt the `basepath` variable:
```python
from invoke import task
from pathlib import Path

basepath = "/path/to/your/repo"

open_cmd = "open"

fig_names = {
    "1": "paper/fig1",
    "2": "paper/fig2",
    "3": "paper/fig3",
}

@task
def convert_to_png_pdf(c, fig):
    _convertsvg2pdf(c, fig)
    _convertpdf2png(c, fig)


########################################################################################
# Helpers
########################################################################################
@task
def _convertsvg2pdf(c, fig):
    if fig is None:
        for f in range(len(fig_names)):
            _convert_svg2pdf(c, str(f + 1))
        return
    pathlist = Path("{bp}/{fn}/fig/".format(bp=basepath, fn=fig_names[fig])).glob(
        "*.svg"
    )
    for path in pathlist:
        c.run("inkscape {} --export-pdf={}.pdf".format(str(path), str(path)[:-4]))


@task
def _convertpdf2png(c, fig):
    if fig is None:
        for f in range(len(fig_names)):
            _convert_pdf2png(c, str(f + 1))
        return
    pathlist = Path("{bp}/{fn}/fig/".format(bp=basepath, fn=fig_names[fig])).glob(
        "*.pdf"
    )
    for path in pathlist:
        c.run(
            'inkscape {} --export-png={}.png -b "white" --export-dpi=250'.format(
                str(path), str(path)[:-4]
            )
        )
```

Now, from the commandline, run `invoke convert_to_png_pdf 1`. This will convert the `svg` of `fig1` to `pdf` and `png` and save them in the `fig` folder.

## Part 4: Syncing the `files` with overleaf from the commandline  
Finally, you will want to upload the `png` and `pdf` to overleaf. Again, we would like to do this from the commandline. To do so, we can first use `git` to create a local copy of the overleaf project, see [here](https://www.overleaf.com/learn/how-to/Using_Git_and_GitHub). Second, we will add a task to our `tasks.py` file which will directly copy the files from our repository folder to the overleaf folder. Add the following to `tasks.py` and adapt the `overleaf` variable:
```python
overleaf = "/path/to/your/overleaf"

@task
def sync_overleaf(c, fig):
    convert_to_png_pdf(c, fig)
    c.run(
        "cp {bp}/{fn}/fig/*.pdf {ol}/figs/ ".format(
            bp=basepath, fn=fig_names[fig], ol=overleaf
        )
    )
    c.run(
        "cp {bp}/{fn}/fig/*.png {ol}/figs/ ".format(
            bp=basepath, fn=fig_names[fig], ol=overleaf
        )
    )
```
Now, from the command-line, you can run `invoke sync_overleaf 1` and it will convert your `svg` to `pdf` and `png` and copy the files to the overleaf folder. Finally, you only have to commit your changes and upload to overleaf:
```
cd /path/to/your/overleaf
git commit -am "new figures"
git push
```

That's it! Your pretty multipanel figures are now on overleaf.
