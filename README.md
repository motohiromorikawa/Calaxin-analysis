# Calaxin-analysis
Description of python scripts to analyze sperm waveform.

1. Introduction
This is a introduction of 3 python scripts, "LineTrace_4x.py", "PlotLine.py", and "Asymindex.py".
To start this analysis, you need a tif file of a trace of a sperm flagellum.
"LineTrace_4x.py" converts the tif file to 3 text files that contain xy coordinates, tangent angles, and cumulative length of the trace.
"PlotLine.py" overlays multiple length vs. tangent angle plots and calculate the average slope of the plot (what we call "basal curvature").
"Asymindex.py" calculate the asymmetry index as in (Mizuno et al, 2012).

2. How to use
These scripts need following libraries: Pillow, numpy, matplotlib, and circle-fit.

"LineTrace_4x.py"has 3 arguments: .tif file and x and y coordinates of the anterior end of the trace.
For example, if you are analyzin "sperm_1.tif" and its anterior end is (x, y)=(1, 1), please execute as follows:
$python LineTrace_4x.py sperm_1.tif 1 1
It will return 3 text files, "sperm_1_point.txt", "sperm_2_slope.txt", and "sperm_3_length.txt".

After analyzing 3 tif files, "sperm_1.tif", "sperm_2.tif", and "sperm_3.tif", we can calculate the basal curvature with "PlotLine.py" as follows:
$python PlotLine.py sperm 1 2 3
It will return the basal curvature and the plot containing tangent angles of 3 traces and the linear fitting.

If you want to calculate asymmetry index, you can use "Asymindex.py":
$python Asymindex.py sperm 1 2 3
It will return the asymmetry index.
