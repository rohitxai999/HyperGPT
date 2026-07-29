from app.services.context_service import ContextService


def main():

    service = ContextService()

    query = "Tell me about HyperGPT project"

    print("=" * 60)
    print("FULL CONTEXT")
    print("=" * 60)

    context = service.get_full_context(query)

    print("\nMEMORIES:")
    for memory in context["memories"]:
        print(memory)


    print("\nDOCUMENTS:")
    for document in context["documents"]:
        print(document)


if __name__ == "__main__":
    main()