import pytest

from voting import vote


params = (
    ([1, 1, 1, 2, 3], 1),
    ([1, 2, 3, 2, 2], 2)
)

@pytest.mark.parametrize(
    'x, expected',
    params
)
def test_vote_params(x, expected):
    assert vote(x) == expected