from typing import List, Tuple

from board.controller import Controller


def global_control(command: str) -> Controller:
    def control(agent_list: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        shift_vector = {
            "w": (-1, 0),
            "s": (+1, 0),
            "a": (0, -1),
            "d": (0, +1),
        }
        dh, dw = shift_vector.get(command, (0, 0))
        next_agent_list = [(h + dh, w + dw) for h, w in agent_list]
        return next_agent_list

    return control
