from app.services.context_service import ContextService


def test_context_service():

    service = ContextService()

    result = service.get_full_context(
        "What is artificial intelligence?"
    )

    assert result is not None
    assert "memories" in result
    assert "documents" in result

    assert isinstance(result["memories"], list)
    assert isinstance(result["documents"], list)