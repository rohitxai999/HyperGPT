import pytest

from backend.app.services.agent_router import AgentRouter


@pytest.fixture
def router():
    return AgentRouter()


@pytest.mark.parametrize(
    ("task", "expected_agent"),
    [
        ("Calculate 21 plus 21", "Math Agent"),
        ("Add 2 and 3", "Math Agent"),
        ("What is the derivative of x squared?", "Math Agent"),
        ("Write Python code to calculate 21 plus 21", "Coding Agent"),
        ("Review this report", "Reviewer Agent"),
        ("Write project documentation", "Writer Agent"),
        ("Plan an AI startup", "Planner Agent"),
        ("Explain machine learning", "Research Agent"),
    ],
)
def test_route_selects_expected_agent(router, task, expected_agent):
    assert router.route(task).name == expected_agent


def test_route_does_not_misclassify_non_math_add_request(router):
    assert router.route("Add documentation to the project").name == "Writer Agent"


def test_route_requires_text_task(router):
    with pytest.raises(TypeError, match="task must be a string"):
        router.route(None)
