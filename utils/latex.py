import os
import random
import subprocess

async def generate_image(preamble, latex):
    """Compiles LaTeX and gives image."""
    filenum = str(random.randint(1, 2 ** 31))
    texfilename = "utils/latex_files/{0}.tex".format(filenum)
    imgfilename = "utils/latex_files/{0}.png".format(filenum)
    pdffilename = "utils/latex_files/{0}.pdf".format(filenum)

    with open(texfilename, "w") as f:
        f.write("\\documentclass[preview]{standalone}\n")
        f.write("\\usepackage[usenames, dvipsnames]{color}\n")
        f.write("\\usepackage{amsmath}\n")
        f.write("\\usepackage{asymptote}\n")
        f.write(preamble)
        f.write("\\nonstopmode\n")
        f.write("\n")
        f.write("\\begin{document}\n")
        f.write("\\color{white}\n")
        f.write(latex)
        f.write("\n")
        f.write("\\end{document}")
        f.close()

    result = subprocess.call("latexmk -pdf -jobname=utils/latex_files/{0} {1} >> output.txt".format(filenum, texfilename), shell=True)
    if (result != 0):
        os.system("latexmk -C {0}".format(texfilename))
        os.system("rm " + texfilename)
        return "-1"
    os.system("convert -density 300 " + pdffilename + " -quality 90 " + imgfilename)
    os.system("latexmk -C")
    os.system("rm utils/latex_files/{0}.tex".format(filenum))
    os.system("rm utils/latex_files/{0}.pre".format(filenum))
    os.system("rm utils/latex_files/{0}.asy".format(filenum))
    os.system("rm utils/latex_files/{0}.pdf".format(filenum))
    return imgfilename
