class TemporalStateMachine:

    def __init__(
            self, 
            confirmation_frames: int,
            max_missing_frames: int | None = None,
    ):

        if confirmation_frames < 1:
            raise ValueError("confirmation_frames must be >= 1")

        if max_missing_frames is not None and max_missing_frames < 0:
            raise ValueError("max_missing_frames must be >= 0")

        self.confirmation_frames = confirmation_frames
        self.max_missing_frames = max_missing_frames

        self.current_state = None           # Última posesión confirmada
        self.candidate_state = None         # Equipo candidato a nueva posesión
        self.candidate_count = 0            # Número de observaciones consecutivas del candidato
        self.missing_count = 0              # Número de frames consecutivos sin evidencia   
   

    def update(self, evidence: str | None) -> str | None:
        
        if evidence not in ("H", "A", None):
            raise ValueError(f"Invalid evidence: {evidence}")

        if evidence is None:
            self.missing_count += 1
            self.candidate_state = None
            self.candidate_count = 0

            if (
                self.max_missing_frames is not None
                and self.missing_count > self.max_missing_frames
            ):
                self.current_state = None
            return self.current_state

        # Evidence is available again.
        self.missing_count = 0

        if self.current_state is None:
            self.current_state = evidence

        elif evidence == self.current_state:
            self.candidate_state = None
            self.candidate_count = 0

        else:
            if self.candidate_state != evidence:
                self.candidate_state = evidence
                self.candidate_count = 1
            else:
                self.candidate_count += 1

            if self.candidate_count >= self.confirmation_frames:
                self.current_state = self.candidate_state
                self.candidate_state = None
                self.candidate_count = 0

        return self.current_state


def run_temporal_state_machine(
    evidence_sequence,
    confirmation_frames: int,
    max_missing_frames: int | None = None,
) -> list[str | None]:
    """Batch helper: runs a fresh TemporalStateMachine over a sequence."""

    machine = TemporalStateMachine(
        confirmation_frames=confirmation_frames,
        max_missing_frames=max_missing_frames,
    )

    return [machine.update(item) for item in evidence_sequence]
