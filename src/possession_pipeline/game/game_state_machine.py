from enum import Enum


class GameState(str, Enum):
    UNKNOWN = "UNKNOWN"     # desconocemos si el juego está activo.
    IN_PLAY = "IN_PLAY"     # tenemos un estado que indica que el juego está activo.
    POSSIBLE_STOPPAGE = "POSSIBLE_STOPPAGE"     # existe una señal que sugiere una interrupción.
    STOPPED = "STOPPED"     # existe una confirmación de interrupción según nuestra máquina.


class GameEvent(str, Enum):
    STOPPAGE_CANDIDATE = "STOPPAGE_CANDIDATE"
    STOPPAGE_CONFIRMED = "STOPPAGE_CONFIRMED"
    RESTART_CONFIRMED = "RESTART_CONFIRMED"


def game_state_machine(
    events: list[GameEvent | None],
) -> list[GameState]:

    current_state = GameState.UNKNOWN
    predictions = []

    for event in events:

        if event is None:
            predictions.append(current_state)
            continue

        if event == GameEvent.STOPPAGE_CANDIDATE:
            if current_state == GameState.IN_PLAY:
                current_state = GameState.POSSIBLE_STOPPAGE

        elif event == GameEvent.STOPPAGE_CONFIRMED:
            current_state = GameState.STOPPED

        elif event == GameEvent.RESTART_CONFIRMED:
            current_state = GameState.IN_PLAY

        else:
            raise ValueError(f"Invalid event: {event}")

        predictions.append(current_state)

    return predictions