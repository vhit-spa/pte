import re
from json import dumps
from pathlib import Path
from prettytable import PrettyTable
from abc import ABC, abstractmethod
from typing import List, TextIO, Any, Iterator

__all__ = ['MapParser']

# Constants
NEW_BLOCK = (
    "==============================================================================\n"
)


# Classes
class MapBlock(ABC):
    """Block handler"""

    def __init__(
        self,
        open_seq: str,
        columns: List[str],
    ):
        self._open_seq: list = open_seq.split("\n")
        self._columns: list = columns
        self._table: dict = {k: [] for k in self._columns}

    def matches_block(self, stream: TextIO) -> bool:
        for l in self._open_seq:
            if stream.readline() != l + "\n":
                return False

        return True

    @abstractmethod
    def collect_row(self, row: str) -> None:
        """This method updates the table attribute"""
        pass

    def get_mapvalues(
        self,
        filter_dict: dict,
        res_keys: str | list,
        unique: bool = False,
        with_key: bool = False,
    ) -> dict:
        _b_key: str = next(iter(filter_dict.keys()))
        out_dict: dict = {}.update(filter_dict) if with_key else {}

        for k in filter_dict.keys():
            filter_dict[k] = re.compile(filter_dict[k])

        row_i: int = 0

        res_keys = [res_keys] if isinstance(res_keys, str) else res_keys

        for k in res_keys:
            out_dict.update({k: []})

        while row_i < len(self._table[_b_key]):
            is_matching = True
            for k, rex in filter_dict.items():
                is_matching = is_matching and rex.match(self._table[k][row_i]) != None
                if not is_matching:
                    break

            if is_matching:
                for k in res_keys:
                    out_dict[k].append(self._table[k][row_i])

            row_i += 1

        if unique:
            for k in out_dict.keys():
                if isinstance(out_dict, list) and len(out_dict[k]) > 1:
                    raise Exception(
                        "Multiple matches for this filter input:\n\t%s" % filter_dict
                    )
                out_dict[k] = out_dict[k][0]

        return out_dict


class BlockB1(MapBlock):

    OPEN = """
Image Symbol Table

    Local Symbols

    Symbol Name                              Value     Ov Type        Size  Object(Section)
"""

    COLS = ["symbol_name", "value", "ov", "type", "size", "object"]

    MIN_COLS = 6
    MAX_COLS = 7

    rule = re.compile(
        r"^\s+(?P<symbol_name>[^\s]+)\s+(?P<value>0x[0-9a-f]+)\s(?P<ov>[\w\/\.]+|\s)\s(?P<type>\w+\s\w+|\w+)\s+(?P<size>\d+)\s+(?P<object>.*)$"
    )

    def __init__(self):
        super().__init__(open_seq=self.OPEN, columns=self.COLS)

    def collect_row(self, row: str) -> None:
        m = self.rule.match(row)

        if not m:
            return

        # Split row
        for k, v in m.groupdict().items():
            self._table[k].append(v)


class MapParser:
    """Main map parser class"""

    def __init__(self) -> None:
        self._container: dict = None
        self._blocks: list[MapBlock] = [BlockB1()]
        self._block_map: dict = {
            "ImageSymbolTable": self._blocks[0],
        }

    def parse(self, src_path: str, _debug: bool=False) -> None:
        src = Path(src_path)

        # Check the existince of the file
        assert src.exists(), "The input file [%s] does not exist" % src_path

        # Current block init
        b: int = -1

        # Parse the file and extract the memory map
        with src.open("r") as f:
            line = f.readline()
            while line:
                if line == NEW_BLOCK:

                    # Debug
                    if b >= 0:
                        if _debug:
                            with open("exit_%s" % b, "w") as u:
                                u.write(dumps(self._blocks[b].__dict__["_table"], indent=1))

                    if b + 1 >= len(self._blocks):
                        return

                    if self._blocks[b + 1].matches_block(f):
                        b += 1
                elif b >= 0:
                    self._blocks[b].collect_row(line)

                line = f.readline()

    def get_block(self, name: str) -> MapBlock:
        return self._block_map[name]

    @property
    def icd(self) -> dict:
        return self.get_block("ImageSymbolTable").get_mapvalues(
            {"type": "Data", "symbol_name": "\w+\_[a-z]\d+.*"}, ["symbol_name", "value"]
        )
    
    def print_icd(self)-> None:
        pt = PrettyTable()
        for k, v in self.icd.items():
            pt.add_column(k, v)

        print(pt)


