from typing import List
import requests.rq as rq
from models.schemas.schemas import PredictionsResponse, PredictionSchema
from requests.prediction import PurchasePatternAnalyzer
from fastapi import APIRouter, Query

from datetime import datetime

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/predictions", response_model=PredictionsResponse)
def get_sales_predictions(
        min_requirements: int = Query(3, ge=2, le=10, description="Minimum purchase count"),
        confidence_threshold: float = Query(0.6, ge=0.0, le=1.0, description="Minimum confidence")
):
    patterns_data = rq.get_purchase_patterns(min_requirements=min_requirements)

    if not patterns_data["patterns"]:
        return PredictionsResponse(
            predictions=[],
            generated_at=datetime.now(),
            total_predictions=0,
            filters_applied={
                "min_requirements": min_requirements,
                "confidence_threshold": confidence_threshold
            }
        )

    analyzer = PurchasePatternAnalyzer(
        min_requirements=min_requirements,
        confidence_threshold=confidence_threshold
    )

    predictions: List[PredictionSchema] = []

    for pattern in patterns_data["patterns"]:
        analysis = analyzer.analyze_client_product_pattern(
            pattern["dates"],
            pattern["amounts"]
        )

        if analysis is None:
            continue

        # Filter by confidence
        if analysis["confidence_score"] < confidence_threshold:
            continue

        # Create prediction
        try:
            prediction = PredictionSchema(
                client_id=pattern["client_id"],
                client_name=pattern["client_name"],
                agent_id=pattern["agent_id"],
                agent_name=pattern["agent_name"],
                goods_id=pattern["goods_id"],
                goods_name=pattern["goods_name"],
                purchase_count=pattern["purchase_count"],

                **analysis
            )
            predictions.append(prediction)
        except Exception as e:
            print(f"Error creating prediction: {e}")
            continue

    # Sort by urgency (days since last requirement, descending)
    predictions.sort(key=lambda p: p.days_since_last_requirement, reverse=True)

    return PredictionsResponse(
        predictions=predictions,
        generated_at=datetime.now(),
        total_predictions=len(predictions),
        filters_applied={
            "min_requirements": min_requirements,
            "confidence_threshold": confidence_threshold
        }
    )
