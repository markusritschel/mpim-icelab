# !/usr/bin/env python
# -*- coding utf-8 -*-
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  kontakt@markusritschel.de
# Date:   23/10/2020
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import os
import subprocess


def clean_log_file(file, output=None):
    """Cleanse lines, which do not start with a TSTICK identifier. If no output is given, the result is written to
    <filename>_clean.<ext>."""
    file = os.path.abspath(file)
    filename, ext = os.path.splitext(file)
    if not output:
        output = f"{filename}_clean{ext}"
    sed_cmd = f"sed -rn '/^[[:digit:]]+?: /p' {file} > {output}"

    ret = subprocess.run(sed_cmd, shell=True)
    if ret.returncode == 0:
        print(f'Created {output}')
        return
    else:
        return ret.returncode
