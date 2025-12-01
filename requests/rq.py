from typing import Dict, Any, List
from collections import defaultdict


from core.remote_db import RemoteMySQL

db = RemoteMySQL()



def get_purchase_patterns(
        min_requirements: int = 3,
) -> Dict[str, Any]:
    """
    Analyze purchase patterns by grouping sales by client and goods.
    Returns patterns with dates, quantities, and related entities.
    """

    query = """
    SELECT 
        s.sales_id,
        s.client_id,
        s.created_date,
        s.agent_id,
        c.client_name,
        a.agent_name,
        sg.goods_id,
        g.goods_name,
        sg.amount
    FROM sales s
    INNER JOIN sales_goods sg ON s.sales_id = sg.sales_id
    INNER JOIN goods g ON sg.goods_id = g.goods_id
    INNER JOIN client c ON s.client_id = c.client_id
    INNER JOIN agent a ON s.agent_id = a.agent_id
    WHERE sg.amount > 0
    ORDER BY s.created_date DESC
    """

    results = db.query(query)

    if not results:
        return {
            "patterns": [],
            "total_patterns": 0,
            "min_requirements_used": min_requirements
        }

    patterns = defaultdict(lambda: defaultdict(lambda: {
        "dates": [],
        "amounts": [],
        "client_id": None,
        "client_name": None,
        "agent_id": None,
        "agent_name": None,
        "goods_id": None,
        "goods_name": None
    }))

    for row in results:
        client_id = row["client_id"]
        goods_id = row["goods_id"]

        pattern = patterns[client_id][goods_id]
        pattern["dates"].append(row["created_date"])
        pattern["amounts"].append(float(row["amount"]))
        pattern["client_id"] = client_id
        pattern["client_name"] = row["client_name"]
        pattern["agent_id"] = row["agent_id"]
        pattern["agent_name"] = row["agent_name"]
        pattern["goods_id"] = goods_id
        pattern["goods_name"] = row["goods_name"]

    # Filter and format patterns
    formatted_patterns = []

    for client_id, goods_dict in patterns.items():
        for goods_id, pattern in goods_dict.items():
            purchase_count = len(pattern["dates"])

            if purchase_count >= min_requirements:
                amounts = pattern["amounts"]

                formatted_patterns.append({
                    "client_id": pattern["client_id"],
                    "client_name": pattern["client_name"],
                    "agent_id": pattern["agent_id"],
                    "agent_name": pattern["agent_name"],
                    "goods_id": pattern["goods_id"],
                    "goods_name": pattern["goods_name"],
                    "purchase_count": purchase_count,
                    "dates": pattern["dates"],
                    "amounts": amounts

                })

    formatted_patterns.sort(key=lambda x: x["purchase_count"], reverse=True)

    return {
        "patterns": formatted_patterns,
        "total_patterns": len(formatted_patterns),
        "min_requirements_used": min_requirements
    }