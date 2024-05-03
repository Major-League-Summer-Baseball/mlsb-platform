import pytest
from api.queries.team_records import \
    rank_teams_by_espys, rank_teams_by_record, rank_teams_by_runs_for, \
    rank_teams_by_stats


def is_sorted(values, attribute):
    return all(
        values[i][attribute] >= values[i + 1][attribute]
        for i in range(len(values) - 1)
    )


@pytest.mark.usefixtures('mlsb_app')
def test_rank_teams_by_espys(mlsb_app):
    """Test ranking is decreasing."""
    with mlsb_app.app_context():
        ranking = rank_teams_by_espys()
        assert is_sorted(ranking, 'total')
        assert ranking[0]['total'] > 0


@pytest.mark.usefixtures('mlsb_app')
def test_rank_teams_by_record(mlsb_app):
    """Test ranking is decreasing."""
    with mlsb_app.app_context():
        ranking = rank_teams_by_record()
        assert is_sorted(ranking, 'wins')
        assert ranking[0]['wins'] > 0


@pytest.mark.usefixtures('mlsb_app')
def test_rank_teams_by_runs_for(mlsb_app):
    """Test ranking is decreasing."""
    with mlsb_app.app_context():
        ranking = rank_teams_by_runs_for()
        assert is_sorted(ranking, 'total')
        assert ranking[0]['total'] > 0


@pytest.mark.usefixtures('mlsb_app')
def test_rank_teams_by_stats(mlsb_app):
    """Test ranking is decreasing."""
    with mlsb_app.app_context():
        ranking = rank_teams_by_stats("hr")
        assert is_sorted(ranking, 'total')
        assert ranking[0]['total'] > 0
