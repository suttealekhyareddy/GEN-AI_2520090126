from llm_client import generate_response


def test_generate_response():
    result = generate_response("What is Artificial Intelligence?")

    assert "success" in result
    assert "response" in result
    assert "input_tokens" in result
    assert "output_tokens" in result
    assert "total_tokens" in result
    assert "response_time" in result