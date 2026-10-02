from dataclasses import dataclass, field
from typing import Dict, Set, FrozenSet


@dataclass
class Descriptor:
    start_state: Set[FrozenSet[str]] = field(default_factory=set)
    alphabet: Set[str] = field(default_factory=set)
    accept_states: Set[FrozenSet[str]] = field(default_factory=set)
    transitions: Dict[FrozenSet[str], Dict[str, Set[FrozenSet[str]]]] = field(default_factory=dict)


class Reader:
    @staticmethod
    def read_from_file(file_path: str) -> Descriptor:
        desc = Descriptor()

        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        alphabet_line = lines[0].replace("alphabet:", "").strip()
        desc.alphabet = set(alphabet_line.split())

        start_line = lines[1].replace("start:", "").strip()
        desc.start_state = {frozenset([state]) for state in start_line.split()}

        accept_line = lines[2].replace("accept:", "").strip()
        desc.accept_states = {frozenset([state]) for state in accept_line.split()}

        for line in lines[3:]:
            parts = line.split()
            if len(parts) != 3:
                continue

            from_state_str, symbol, to_state_str = parts

            if symbol not in desc.alphabet:
                continue

            from_state = frozenset([from_state_str])
            to_state = frozenset([to_state_str])

            if from_state not in desc.transitions:
                desc.transitions[from_state] = {}
            if symbol not in desc.transitions[from_state]:
                desc.transitions[from_state][symbol] = set()

            desc.transitions[from_state][symbol].add(to_state)

        return desc
