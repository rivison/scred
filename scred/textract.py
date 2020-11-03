"""
textract.py

Tools for extracting text entries directly from REDCap.
"""

from typing import TYPE_CHECKING, Iterable, List, Set, Tuple

import pandas as pd

# from requests.exceptions import HTTPError

if TYPE_CHECKING:
    from . import RedcapProject, _PostJsonType, _RecordValueType

# ---------------------------------------------------


class Textractor:
    """
    Takes a scred.RedcapProject instance and
    pulls values of all text fields.
        project: the instance to use for sending requests
        idfield: the field in current project used for labeling records
    """

    def __init__(self, project: "RedcapProject", idfield: str) -> None:
        self.project = project
        self.idfield = idfield
        self._bounded: Set[str] = set()
        # TODO: set Project attrs to None,
        # call API when they're first accessed

    @property
    def bounded(self) -> Set[str]:
        """
        Text fields that aren't "free" text, but bounded in some way.
        Unique IDs, numerics, and so on.
        """
        return self._bounded

    @bounded.setter
    def bounded(self, value: Iterable[str]) -> None:
        if isinstance(value, set):
            self._bounded = value
        elif isinstance(value, str):
            self._bounded = {value}
        else:
            self._bounded = set(value)  # let any exceptions rise

    @property
    def textfields(self) -> Set[str]:
        text_mask = self.project.metadata["field_type"] == "text"
        return set(self.project.metadata[text_mask].index)

    @property
    def desired(self) -> List[str]:
        return sorted(self.textfields - self.bounded)

    def pull_desired(
        self, **kwargs: str
    ) -> "List[Tuple[str, str, _RecordValueType]]":
        """
        Extracts all provided values from REDCap for each desired field.
        Returns a JSON object.
        """
        data = self._request_desired(**kwargs)
        df = pd.DataFrame(data)
        df = df.set_index(self.idfield).T
        entries = []
        for field, row in df.iterrows():
            has_text = row.loc[lambda x: x != ""]  # .loc might break it, test
            for idfield, value in sorted(has_text.iteritems()):
                new = (field, idfield, value)
                # Factor out 2nd loop into generator? yield has_text
                entries.append(new)
        return entries

    def _request_desired(self, **kwargs: str) -> "_PostJsonType":
        """
        Factored out of `pull_desired` for testability.
        Returns JSON of REDCap records.
        """
        fields = {"fields": [self.idfield] + self.desired}
        return self.project.get_records(fields=fields, **kwargs)

    def pull_to_csv(self, filename: str, *args: str, **kwargs: str) -> None:
        tups = self.pull_desired(*args, **kwargs)
        df = pd.DataFrame(
            tups, columns=["Field", "Participant ID", "Value Reported"]
        )
        df["Action Needed"] = ""
        df.to_csv(filename, index=False)
