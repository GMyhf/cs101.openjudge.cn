"""Hard policy for T-004 independent oracle reviews.

An oracle is independent only when its algorithm family differs from the
reference family and a conceptual reference bug would not be copied by it.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class OracleContract:
    reference_family: str
    oracle_family: str
    conceptual_bug_independence: bool
    rationale: str

    def validate(self):
        if self.reference_family == self.oracle_family:
            raise AssertionError("reference and oracle use the same algorithm family")
        if not self.conceptual_bug_independence:
            raise AssertionError("oracle can repeat a conceptual reference bug")
        if not self.rationale.strip():
            raise AssertionError("independence rationale is required")
        return True


FAMILY_PAIRS = {
    "dp_vs_enumeration": ("dynamic programming", "brute-force enumeration"),
    "greedy_vs_search": ("greedy/two-pointer", "search or memoized exhaustive choices"),
    "closed_form_vs_simulation": ("closed form/bit operation", "digit or state simulation"),
    "dijkstra_vs_relaxation": ("Dijkstra", "Bellman-Ford relaxation"),
    "heap_vs_sorted_queue": ("two heaps", "sorted list/deque simulation"),
    "recursive_parser_vs_stack_parser": ("recursive parser", "explicit stack parser"),
    "bfs_vs_exhaustive_search": ("BFS shortest path", "exhaustive simple-path search"),
}


def contract(pair, rationale):
    reference_family, oracle_family = FAMILY_PAIRS[pair]
    value = OracleContract(reference_family, oracle_family, True, rationale)
    value.validate()
    return value

