from possession_pipeline.game.game_state_machine import (
    GameState,
    GameEvent,
    game_state_machine,
)


def test_initial_state_unknown():

    result = game_state_machine([None, None])

    assert result == [
        GameState.UNKNOWN,
        GameState.UNKNOWN,
    ]


def test_confirmed_stoppage():

    events = [
        GameEvent.RESTART_CONFIRMED,
        GameEvent.STOPPAGE_CANDIDATE,
        GameEvent.STOPPAGE_CONFIRMED,
    ]

    result = game_state_machine(events)

    assert result == [
        GameState.IN_PLAY,
        GameState.POSSIBLE_STOPPAGE,
        GameState.STOPPED,
    ]


def test_candidate_does_not_confirm_stoppage():

    events = [
        GameEvent.RESTART_CONFIRMED,
        GameEvent.STOPPAGE_CANDIDATE,
        None,
    ]

    result = game_state_machine(events)

    assert result == [
        GameState.IN_PLAY,
        GameState.POSSIBLE_STOPPAGE,
        GameState.POSSIBLE_STOPPAGE,
    ]


def test_restart_after_stoppage():

    events = [
        GameEvent.STOPPAGE_CONFIRMED,
        None,
        GameEvent.RESTART_CONFIRMED,
    ]

    result = game_state_machine(events)

    assert result == [
        GameState.STOPPED,
        GameState.STOPPED,
        GameState.IN_PLAY,
    ]


def test_no_look_ahead():

    prefix = [
        GameEvent.RESTART_CONFIRMED,
        GameEvent.STOPPAGE_CANDIDATE,
    ]

    future = [
        GameEvent.STOPPAGE_CONFIRMED,
        GameEvent.RESTART_CONFIRMED,
    ]

    prefix_result = game_state_machine(prefix)

    full_result = game_state_machine(prefix + future)

    assert prefix_result == full_result[:len(prefix)]