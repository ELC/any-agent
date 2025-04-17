from any_agent.logging import logger


def show_plan(plan: str) -> str:
    """Show the current plan to the user.

    Args:
        plan: The current plan.

    """
    logger.info("Current plan: %s", plan)
    return plan


def show_final_answer(answer: str) -> str:
    """Show the final answer to the user.

    Args:
        answer: The final answer.

    """
    logger.info("Final answer: %s", answer)
    return answer


def ask_user_verification(query: str) -> str:
    """Asks user to verify the given `query`.

    Args:
        query: The question that requires verification.

    """
    return input(f"{query} => Type your answer here:")


def send_console_message(user: str, query: str) -> str:
    """Sends the specified user a message via console and returns their response.

    Args:
        query: The question to ask the user.
        user: The user to ask the question to.

    Returns:
        str: The user's response.

    """
    return input(f"{query}\n{user}>>")
