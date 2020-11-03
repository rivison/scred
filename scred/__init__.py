"""
scred/__init__.py

Contains everything intended for exposure to users.
"""

from .project import RedcapProject
from .dtypes import Record, RecordSet, DataDictionary
from .webapi import RedcapRequester

import typing

# using typing.NewType to force type-checking to treat types as distinct
_FieldNameValueType = typing.NewType("_FieldNameValueType", object)
_MetadataValueType = typing.NewType("_MetadataValueType", object)
_ParsedValueType = typing.NewType("_ParsedValueType", object)
_PayloadValueType = typing.NewType("_PayloadValueType", object)
_PostJsonType = typing.NewType("_PostJsonType", object)
_RecordValueType = typing.NewType("_RecordValueType", object)
