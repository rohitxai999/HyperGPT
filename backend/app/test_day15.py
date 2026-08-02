from app.planner.autonomous_planner import AutonomousPlanner
from app.planner.execution_engine import ExecutionEngine


def main():
    planner = AutonomousPlanner()

    user_request = (
        "Calculate something, tell me the time and save the report"
    )

    print("=" * 60)
    print("USER REQUEST")
    print("=" * 60)
    print(user_request)

    # Create execution plan
    tasks = planner.create_plan(user_request)

    print("\n" + "=" * 60)
    print("TASK PLAN")
    print("=" * 60)

    for task in tasks:
        print(task)

    # Execute tasks
    engine = ExecutionEngine()
    results = engine.execute(tasks)

    print("\n" + "=" * 60)
    print("EXECUTION RESULTS")
    print("=" * 60)

    for result in results:
        print(result)

    print("\n" + "=" * 60)
    print("FINAL TASK STATUS")
    print("=" * 60)

    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()