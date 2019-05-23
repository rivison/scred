# Testing class project.RedcapProject

import os
import sys
import pytest

sys.path.insert(
    0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

import pandas as pd

from scred import RedcapProject
from scred.config import TEST_CFG
from . import testdata

# ---------------------------------------------------

def test_RedcapProject_init_with_empty_args_uses_stored_user_cfg():
    rp = RedcapProject()

def test_RedcapProject_init_with_config_object():
    rp = RedcapProject(TEST_CFG)

def test_RedcapProject_init_with_token_str():
    # faketoken = "ABCD9999DDDDXXZZ067JTP01Y44MSPD1"
    faketoken = "48F35658A6AD741128CB8CE03A3774FC"
    rp = RedcapProject(faketoken)
    response = rp.post(content="record").json()
    print(response)
