from combat_raven.models.participant_template import ParticipantTemplate


class ParticipantRepository:
    """
    In-memory repository for participant templates.
    """

    def __init__(self) -> None:
        self._participants: dict[str, ParticipantTemplate] = {}

    def add(self, participant: ParticipantTemplate) -> None:
        """
        Adds a participant template to the repository.
        """
        self._participants[participant.id] = participant

    def get_by_id(self, participant_id: str) -> ParticipantTemplate | None:
        """
        Returns a participant template by its ID.
        """
        return self._participants.get(participant_id)

    def get_by_name(self, name: str) -> ParticipantTemplate | None:
        """
        Returns the first participant template with the given name.
        """
        for participant in self._participants.values():
            if participant.name == name:
                return participant

        return None

    def get(self, name: str) -> ParticipantTemplate | None:
        """
        Returns a participant template by name.

        Kept for backwards compatibility.
        """
        return self.get_by_name(name)

    def list(self) -> list[ParticipantTemplate]:
        """
        Returns all participant templates.
        """
        return list(self._participants.values())

    def remove(self, participant_id: str) -> None:
        """
        Removes a participant template by its ID.
        """
        self._participants.pop(participant_id, None)