from dataclasses import dataclass
from queue import Queue
from typing import FrozenSet, Dict, Tuple

from reader import Descriptor


@dataclass(frozen=True)
class RunResult:
    is_success: bool

    def get_status(self) -> bool:
        return self.is_success


class Runner:
    @staticmethod
    def run_word(descriptor: Descriptor, word: str) -> RunResult:
        cache: Dict[Tuple[FrozenSet[str], int], bool] = {}
        success = False
        for initial_state in descriptor.start_state:
            success = Runner._dfs(descriptor, word, initial_state, 0, cache)
            if success:
                break
        return RunResult(success)

    @staticmethod
    def _dfs(descriptor: Descriptor, word: str, state: FrozenSet[str], i: int,
             cache: Dict[Tuple[FrozenSet[str], int], bool]) -> bool:
        if (state, i) in cache:
            return cache[(state, i)]

        if i >= len(word):
            cache[(state, i)] = state in descriptor.accept_states
            return state in descriptor.accept_states

        all_transitions = descriptor.transitions.get(state, {}).get(word[i], set())
        success = False
        for new_state in all_transitions:
            success = Runner._dfs(descriptor, word, new_state, i + 1, cache)
            if success:
                break
        cache[(state, i)] = success
        return success


class Transformer:
    @staticmethod
    def form_nfa_to_dfa(descriptor: Descriptor, empty_symbol: str = "d"):
        new_descriptor = Descriptor()
        new_descriptor.start_state = descriptor.start_state
        new_descriptor.alphabet = descriptor.alphabet

        q: Queue[FrozenSet[str]] = Queue()

        for initial_state in descriptor.start_state:
            q.put(initial_state)
            new_descriptor.transitions[initial_state] = {}

        while not q.empty():
            current_node: FrozenSet[str] = q.get()

            for part in current_node:
                if frozenset([part]) in descriptor.accept_states:
                    new_descriptor.accept_states.add(current_node)

            for symbol in descriptor.alphabet:
                new_node = set()

                for part in current_node:
                    for el in descriptor.transitions.get(frozenset([part]), {}).get(symbol, set()):
                        for s in el:
                            new_node.add(s)

                if len(new_node) == 0:
                    new_node.add(empty_symbol)

                frozen_new_node = frozenset(new_node)

                new_descriptor.transitions[current_node][symbol] = {frozen_new_node}

                if frozen_new_node not in new_descriptor.transitions:
                    new_descriptor.transitions[frozen_new_node] = {}
                    q.put(frozen_new_node)

        return new_descriptor
