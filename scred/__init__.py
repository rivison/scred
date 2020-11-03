"""
scred/__init__.py

Contains everything intended for exposure to users.
"""

from .project import RedcapProject
from .dtypes import Record, RecordSet, DataDictionary
from .webapi import RedcapRequester

import typing

_FieldNameValueType = typing.Any
_MetadataValueType = typing.Any
_ParsedValueType = typing.Any
_PayloadValueType = typing.Any
_PostJsonType = typing.Any
_RecordValueType = typing.Any
