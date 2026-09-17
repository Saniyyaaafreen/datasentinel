import os

from openai import OpenAI

from dotenv import load_dotenv


# Load variables from the .env file
load_dotenv()


# Create a connection to DeepSeek
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def explain_flagged_row(
    row_dict,
    row_index,
    flag_reason,
    dataset_stats=None
):
    """
    Sends a flagged data row to DeepSeek
    and asks for a simple explanation based
    on the actual DataSentinel validation result.
    """

    context = ""

    if dataset_stats:
        context = f"\nDataset statistics: {dataset_stats}"

    prompt = f"""
You are a data quality analyst.

DataSentinel has flagged the following row as a data quality issue.

Row number: {row_index}

Row data: {row_dict}

EXACT VALIDATION REASON:
{flag_reason}

{context}

Explain in exactly ONE sentence why DataSentinel flagged this row.

Use the exact suspicious value and the validation reason provided above.

Do not invent a different problem.

Do not speculate about other columns.

Start with "Row {row_index}".

Keep the explanation simple and specific.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=100
    )

    return response.choices[0].message.content


def generate_dataset_summary(summary_data):
    """
    Sends the overall DataSentinel validation results to DeepSeek
    and asks for a concise natural-language dataset quality summary.
    """

    prompt = f"""
You are a data quality analyst.

DataSentinel analyzed this dataset.

VALIDATION SUMMARY:

{summary_data}

Write a concise natural-language summary of the dataset's data quality.

Rules:
- Use ONLY the facts provided in the validation summary.
- Do not invent causes or speculate.
- Mention only issue categories that are actually present.
- Include exact counts and percentages when provided.
- Mention categories with zero issues briefly when useful.
- Keep the summary to 2-4 sentences.
- Make it simple and professional.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=200
    )

    return response.choices[0].message.content
