from dataclasses import dataclass

@dataclass(frozen=True)
class RestartCandidate:
    start_frame: int        # Inicio del intervalo etiquetado
    end_frame: int          # Fin del intervalo etiquetado
    restart_type: str       # Tipo de reinicio ("Corner", "Free Kick", etc.)
    team: str | None        # Equipo asociado


TEAM_MAPPING = {
    "Barcelona": "H",
    "Atletic Club": "A",
    "N/A": None,
}


def extract_restart_candidates(events):

    candidates = []

    for event in events:

        if (event["code"] or "").strip().upper() != "SET PIECES":
            continue

        candidate = RestartCandidate(
            start_frame=event["start_frame"],
            end_frame=event["end_frame"],
            restart_type=event["tags"].get("Type", "UNKNOWN"),
            team=TEAM_MAPPING.get(
                event["tags"].get("Team")
            ),
        )

        candidates.append(candidate)

    return candidates
