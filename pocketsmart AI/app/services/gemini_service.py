import os

from google import genai

from app.config import get_settings


settings = get_settings()


def get_client():
    """
    Create and return the Gemini client.

    Returns None if the API key has not been configured.
    """

    api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


def generate_recommendation(
    category: str,
    budget: float,
    details: str,
) -> str:
    """
    Generate a budget-aware recommendation using Gemini.
    """

    client = get_client()

    # Gemini API key is not configured yet
    if client is None:
        return (
            "Gemini API key is not configured yet.\n\n"
            "Your request was received successfully.\n"
            f"Category: {category}\n"
            f"Budget: ₹{budget:,.2f}\n"
            f"Details: {details}\n\n"
            "Please add GEMINI_API_KEY to the .env file "
            "to enable AI recommendations."
        )

    prompt = f"""
You are PocketSmart AI, a smart budget and recommendation assistant.

Category:
{category}

User budget:
₹{budget:,.2f}

User requirements:
{details}

Create a practical recommendation plan.

Important requirements:

1. Stay within the user's total budget.
2. Give realistic budget allocations.
3. Suggest suitable products or services.
4. Mention suitable platforms when appropriate.
5. Do not claim that you checked live prices.
6. Clearly state that prices are approximate.
7. Avoid unnecessary spending.
8. Give a total estimated cost.
9. Explain why the recommendations fit the user's needs.

Return the response using this structure:

TITLE

BUDGET SUMMARY

RECOMMENDATIONS

1. Item
   Estimated Price:
   Suggested Platform:
   Reason:

2. Item
   Estimated Price:
   Suggested Platform:
   Reason:

BUDGET BREAKDOWN

TOTAL ESTIMATED COST

MONEY LEFT

TIPS
"""

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )

        if response.text:
            return response.text

        return "Gemini returned an empty response."

    except Exception as exc:
        return (
            "Unable to contact Gemini right now.\n\n"
            f"Error: {str(exc)}"
        )