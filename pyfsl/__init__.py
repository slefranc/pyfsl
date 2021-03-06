##########################################################################
# NSAp - Copyright (C) CEA, 2013 - 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Package to wrap the FSL software and simplify scripting calls.
In the root location of the module are implemented:

    * the FSL's dedicated exceptions.
    * the FSL's wrapper.
    * the FSL's configuration parser.
"""

from .info import __version__
from .info import DEFAULT_FSL_PATH
