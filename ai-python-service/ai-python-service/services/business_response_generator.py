import statistics
from typing import List, Dict, Any

def generate_business_response(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate business response from SQL query results
    
    Rules:
    - ALWAYS use actual data from "results"
    - NEVER return phrases like "analysis complete"
    - If numeric column exists: return max, min, average
    - If multiple rows: detect top performer
    - If dataset: summarize trend or variation
    """
    if not results or len(results) == 0:
        return {
            "answer": "No data found for the query.",
            "insights": []
        }

    # Get columns dynamically
    sample = results[0]
    numeric_cols = [k for k, v in sample.items() if isinstance(v, (int, float))]
    text_cols = [k for k, v in sample.items() if isinstance(v, str)]

    insights = []
    answer_parts = []

    # ---- Numeric Analysis ----
    for col in numeric_cols:
        values = [row[col] for row in results if isinstance(row[col], (int, float))]

        if not values:
            continue

        max_val = max(values)
        min_val = min(values)
        avg_val = round(statistics.mean(values), 2)

        insights.append(f"Highest {col} is {max_val}")
        insights.append(f"Lowest {col} is {min_val}")
        insights.append(f"Average {col} is {avg_val}")

        answer_parts.append(
            f"{col.capitalize()} ranges from {min_val} to {max_val}, averaging around {avg_val}"
        )

    # ---- Top Performer Detection ----
    for tcol in text_cols:
        if numeric_cols:
            main_num = numeric_cols[0]

            sorted_data = sorted(results, key=lambda x: x[main_num], reverse=True)
            top = sorted_data[0]

            insights.append(f"Top {tcol} is {top[tcol]} with {main_num} {top[main_num]}")
            answer_parts.append(
                f"{top[tcol]} stands out as the top performer"
            )
            break

    # ---- Final Answer ----
    answer = ". ".join(answer_parts[:2])  # keep 2–4 lines max

    if not answer:
        answer = "Data retrieved successfully, showing multiple records with varying values."

    return {
        "answer": answer,
        "insights": insights[:3]  # limit
    }
