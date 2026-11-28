from budget import calculate_cost


def test_zero_tokens():
    assert calculate_cost(0, 0) == 0


def test_input_cost():
    cost = calculate_cost(1_000_000, 0)
    assert cost == 0.30


def test_output_cost():
    cost = calculate_cost(0, 1_000_000)
    assert cost == 1.20


def test_combined_cost():
    cost = calculate_cost(1_000_000, 1_000_000)
    assert cost == 1.50


def test_small_token_usage():
    cost = calculate_cost(1000, 500)
    assert round(cost, 6) == 0.0009