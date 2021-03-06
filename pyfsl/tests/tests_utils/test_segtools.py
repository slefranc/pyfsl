##########################################################################
# NSAp - Copyright (C) CEA, 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import unittest
import sys

# COMPATIBILITY: since python 3.3 mock is included in unittest module
python_version = sys.version_info
if python_version[:2] <= (3, 3):
    import mock
    from mock import patch
else:
    import unittest.mock as mock
    from unittest.mock import patch

# Pyfsl import
from pyfsl.utils.segtools import bet2


class FslBet2(unittest.TestCase):
    """ Test the FSL diffusion tensor model:
    'pyfsl.utils.segtools.bet2'
    """
    def setUp(self):
        """ Run before each test - the mock_popen will be available and in the
        right state in every test<something> function.
        """
        # Mocking popen
        self.popen_patcher = patch("pyfsl.wrapper.subprocess.Popen")
        self.mock_popen = self.popen_patcher.start()
        mock_process = mock.Mock()
        attrs = {
            "communicate.return_value": ("mock_OK", "mock_NONE"),
            "returncode": 0
        }
        mock_process.configure_mock(**attrs)
        self.mock_popen.return_value = mock_process

        # Mocking set environ
        self.env_patcher = patch(
            "pyfsl.wrapper.FSLWrapper._fsl_version_check")
        self.mock_env = self.env_patcher.start()
        self.mock_env.return_value = {}

        # Define function parameters
        self.kwargs = {
            "input_file": "/my/path/mock_input_fileroot",
            "output_fileroot": "/my/path/mock_output_fileroot",
            "outline": False,
            "mask": False,
            "skull": False,
            "nooutput": False,
            "f": 0.5,
            "g": 0,
            "radius": None,
            "smooth": None,
            "c": None,
            "threshold": False,
            "mesh": False,
            "shfile": "/my/path/mock_shfile",
        }

    def tearDown(self):
        """ Run after each test.
        """
        self.popen_patcher.stop()
        self.env_patcher.stop()

    @mock.patch("pyfsl.utils.segtools.os.path.isfile")
    def test_badfileerror_raise(self, mock_isfile):
        """ Bad input file -> raise valueError.
        """
        # Set the mocked functions returned values
        mock_isfile.side_effect = [False]

        # Test execution
        self.assertRaises(ValueError, bet2, **self.kwargs)

    @mock.patch("pyfsl.models.tensor.os.mkdir")
    @mock.patch("pyfsl.models.tensor.os.path.isdir")
    @mock.patch("pyfsl.models.tensor.os.path.isfile")
    def test_baddirerror_raise(self, mock_isfile, mock_isdir, mock_mkdir):
        """ Bad directory -> raise valueError.
        """
        # Set the mocked functions returned values
        mock_isfile.side_effect = [True]
        mock_isdir.side_effect = [False]

        # Test execution
        self.assertRaises(ValueError, bet2, **self.kwargs)

    @mock.patch("pyfsl.models.tensor.os.mkdir")
    @mock.patch("pyfsl.models.tensor.os.path.isdir")
    @mock.patch("pyfsl.models.tensor.os.path.isfile")
    def test_nofsltype_raise(self, mock_isfile, mock_isdir, mock_mkdir):
        """ Bad FSL extension error  -> raise valueError.
        """
        # Set the mocked functions returned values
        mock_isfile.side_effect = [True]
        mock_isdir.side_effect = [True]
        self.mock_env.return_value = {"EXT": "NIFTI"}

        # Test execution
        self.assertRaises(ValueError, bet2, **self.kwargs)

    @mock.patch("pyfsl.models.tensor.os.mkdir")
    @mock.patch("pyfsl.models.tensor.os.path.isdir")
    @mock.patch("pyfsl.utils.segtools.os.path.isfile")
    def test_normal_execution(self, mock_isfile, mock_isdir, mock_mkdir):
        """ Test the normal behaviour of the function.
        """
        # Set the mocked function returned values.
        mock_isfile.side_effect = [True]
        mock_isdir.side_effect = [True]
        self.mock_env.return_value = {"FSLOUTPUTTYPE": "NIFTI"}

        # Test execution
        returned_files = bet2(**self.kwargs)
        self.assertEqual([
            mock.call(["which", "bet2"],
                      env={"FSLOUTPUTTYPE": "NIFTI"},
                      stderr=-1, stdout=-1),
            mock.call(["bet2",
                       self.kwargs["input_file"],
                       self.kwargs["output_fileroot"],
                       "-f", str(self.kwargs["f"]),
                       "-g", str(self.kwargs["g"])],
                      env={"FSLOUTPUTTYPE": "NIFTI"}, stderr=-1, stdout=-1)],
            self.mock_popen.call_args_list)
        self.assertEqual(len(self.mock_env.call_args_list), 1)
        self.assertEqual(len(returned_files), 11)


if __name__ == "__main__":
    unittest.main()
