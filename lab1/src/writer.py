from reader import Descriptor

from typing import FrozenSet, Set


class Writer:
    @staticmethod
    def _format_state(state_frozenset: FrozenSet[str]) -> str:
        return "".join(sorted(state_frozenset))

    @staticmethod
    def _format_set_of_states(states_set: Set[FrozenSet[str]]) -> str:
        formatted = [Writer._format_state(s) for s in states_set]
        return " ".join(sorted(formatted))

    @staticmethod
    def write_to_file(file_path: str, descriptor: Descriptor) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"alphabet: {' '.join(sorted(descriptor.alphabet))}\n")

            f.write(f"start: {Writer._format_set_of_states(descriptor.start_state)}\n")

            f.write(f"accept: {Writer._format_set_of_states(descriptor.accept_states)}\n")

            for from_state, transitions in sorted(descriptor.transitions.items(),
                                                  key=lambda x: Writer._format_state(x[0])):
                from_str = Writer._format_state(from_state)

                for symbol, to_states_set in sorted(transitions.items()):
                    if not to_states_set:
                        continue
                    to_state_frozenset = next(iter(to_states_set))
                    to_str = Writer._format_state(to_state_frozenset)

                    f.write(f"{from_str} {symbol} {to_str}\n")
