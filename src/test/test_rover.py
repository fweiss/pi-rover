from nose.tools import *
from mock import patch

import pigpio

@patch("pigpio.pi.output", autoSpec=True)
class TestMotor:
    def test_init(self):
        assert_equal(1, 1)
        mock_output.assert_has_calls([call(self.fwdPin, True)])