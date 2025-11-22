from datetime import datetime
from typing import List, Optional

import requests.rq as rq
from models.schemas.schemas import (
     PredictionsResponse, PredictionSchema
)

from fastapi import APIRouter

from requests.prediction import PurchasePatternAnalyzer

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/", response_model=PredictionsResponse)
async def get_sales_predictions(
        min_orders: int = 3,
        confidence_threshold: float = 0.6,
        urgency_filter: Optional[str] = None
):
    """
    Predict which clients are likely to buy today based on purchase patterns.

    Parameters:
    - min_orders: Minimum number of past orders required (default: 3)
    - confidence_threshold: Minimum confidence score 0-1 (default: 0.6)
    - urgency_filter: Filter by urgency ("high", "medium", "low")

    Returns predictions sorted by urgency and days overdue.
    """
    # Get purchase patterns (using @connection decorator)
    patterns = await rq.get_purchase_patterns(min_orders=min_orders)

    # Analyze patterns
    analyzer = PurchasePatternAnalyzer(
        min_orders=min_orders,
        confidence_threshold=confidence_threshold
    )

    predictions = []

    for client_id, goods_dict in patterns.items():
        for goods_id, pattern_data in goods_dict.items():
            analysis = analyzer.analyze_client_product_pattern(
                pattern_data["dates"],
                pattern_data["quantities"]
            )

            if analysis is None:
                continue

            # Filter by confidence
            if analysis["confidence_score"] < confidence_threshold:
                continue

            # Filter by urgency if specified
            if urgency_filter and analysis["urgency"] != urgency_filter:
                continue

            client = pattern_data["client"]
            goods = pattern_data["goods"]

            prediction = PredictionSchema(
                client_id=client_id,
                client_name=client.name,
                contact_name=client.contact_name,
                phone=client.phone,
                email=client.email,
                goods_id=goods_id,
                goods_name=goods.name,
                unit=goods.unit,
                **analysis
            )

            predictions.append(prediction)

    # Sort by urgency (high first) and then by days overdue
    urgency_order = {"high": 0, "medium": 1, "low": 2}
    predictions.sort(
        key=lambda p: (urgency_order[p.urgency], -p.days_since_last_order)
    )

    return PredictionsResponse(
        predictions=predictions,
        generated_at=datetime.now(),
        total_predictions=len(predictions)
    )





#
#
# @router.get("/client/{client_id}", response_model=PredictionsResponse)
# async def get_client_predictions(
#         client_id: int,
#         min_orders: int = 3,
#         confidence_threshold: float = 0.6
# ):
#     """
#     Get predictions for a specific client across all products.
#
#     Useful for managers who want to see what a specific client might buy.
#     """
#     patterns = await rq.get_purchase_patterns(min_orders=min_orders)
#
#     if client_id not in patterns:
#         return PredictionsResponse(
#             predictions=[],
#             generated_at=datetime.now(),
#             total_predictions=0
#         )
#
#     analyzer = PurchasePatternAnalyzer(min_orders=min_orders)
#     predictions = []
#
#     for goods_id, pattern_data in patterns[client_id].items():
#         analysis = analyzer.analyze_client_product_pattern(
#             pattern_data["dates"],
#             pattern_data["quantities"]
#         )
#
#         if analysis is None:
#             continue
#
#         # Filter by confidence
#         if analysis["confidence_score"] < confidence_threshold:
#             continue
#
#         client = pattern_data["client"]
#         goods = pattern_data["goods"]
#
#         prediction = PredictionSchema(
#             client_id=client_id,
#             client_name=client.name,
#             contact_name=client.contact_name,
#             phone=client.phone,
#             email=client.email,
#             goods_id=goods_id,
#             goods_name=goods.name,
#             unit=goods.unit,
#             **analysis
#         )
#
#         predictions.append(prediction)
#
#     # Sort by urgency
#     urgency_order = {"high": 0, "medium": 1, "low": 2}
#     predictions.sort(
#         key=lambda p: (urgency_order[p.urgency], -p.days_since_last_order)
#     )
#
#     return PredictionsResponse(
#         predictions=predictions,
#         generated_at=datetime.now(),
#         total_predictions=len(predictions)
#     )
#
#
# @router.get("/stats")
# async def get_prediction_stats():
#     """
#     Get summary statistics about predictions.
#     Useful for dashboard overview.
#     """
#     patterns = await rq.get_purchase_patterns(min_orders=3)
#     analyzer = PurchasePatternAnalyzer(min_orders=3)
#
#     total_client_product_pairs = 0
#     high_urgency_count = 0
#     medium_urgency_count = 0
#     low_urgency_count = 0
#     high_confidence_count = 0
#
#     for client_id, goods_dict in patterns.items():
#         for goods_id, pattern_data in goods_dict.items():
#             analysis = analyzer.analyze_client_product_pattern(
#                 pattern_data["dates"],
#                 pattern_data["quantities"]
#             )
#
#             if analysis is None:
#                 continue
#
#             total_client_product_pairs += 1
#
#             if analysis["urgency"] == "high":
#                 high_urgency_count += 1
#             elif analysis["urgency"] == "medium":
#                 medium_urgency_count += 1
#             else:
#                 low_urgency_count += 1
#
#             if analysis["confidence_score"] >= 0.7:
#                 high_confidence_count += 1
#
#     return {
#         "total_trackable_patterns": total_client_product_pairs,
#         "high_urgency": high_urgency_count,
#         "medium_urgency": medium_urgency_count,
#         "low_urgency": low_urgency_count,
#         "high_confidence_predictions": high_confidence_count,
#         "generated_at": datetime.now()
#     }