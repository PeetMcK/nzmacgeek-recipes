#!/usr/bin/python
# FilemakerUpdateDMGExtractor.py
# Extracts a FileMaker updater package from a given DMG.
#
# Copyright 2016 William McGrath
# w.mcgrath@auckland.ac.nz
#
# Licensed under the Apache License, version 2.0 (the "License"). You
# may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



"""See docstring for FilemakerUpdateDMGExtractor class"""

import json
import os
import shutil

from autopkglib.DmgMounter import DmgMounter
from autopkglib import Processor, ProcessorError

__all__ = ["FilemakerUpdateDMGExtractor"]

class FilemakerUpdateDMGExtractor(DmgMounter):
    """Extracts update pkg from given DMG"""

    description = __doc__
    input_variables = {
        "dmg_path": {
            "required": True,
            "description":
                "The path to the DMG downloaded from the FileMaker website"
        }
    }
    output_variables = {
        "pkg_path": {
            "description": "Outputs the extracted package path."
        }
    }
    def find_pkg(self, dir_path):
        '''Return path to the first package in dir_path'''
        #pylint: disable=no-self-use
        for item in os.listdir(dir_path):
            if item.endswith(".pkg"):
                return os.path.join(dir_path, item)
        raise ProcessorError("No package found in %s" % dir_path)

    def main(self):
        mount_point = self.mount(self.env["dmg_path"])
        # Wrap all other actions in a try/finally so the image is always
        # unmounted.
        try:
            pkg = self.find_pkg(mount_point)
            shutil.copy(pkg, self.env['RECIPE_CACHE_DIR'])
            self.env["pkg_path"] = os.path.join(self.env['RECIPE_CACHE_DIR'], os.path.basename(pkg))
        except BaseException, err:
            raise ProcessorError(err)
        finally:
            self.unmount(self.env["dmg_path"])

if __name__ == "__main__":
    PROCESSOR = FilemakerUpdateDMGExtractor()
    PROCESSOR.execute_shell()
