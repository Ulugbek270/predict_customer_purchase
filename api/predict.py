from datetime import datetime
from typing import List
import requests.rq as rq
from models.schemas.schemas import PredictionsResponse, PredictionSchema
from fastapi import APIRouter
from requests.prediction import PurchasePatternAnalyzer


router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/", response_model=PredictionsResponse)
async def get_sales_predictions(
        min_orders: int = 3,
        confidence_threshold: float = 0.6,
):

    # Get purchase patterns
    patterns = await rq.get_purchase_patterns(min_orders=min_orders)

    analyzer = PurchasePatternAnalyzer(
        min_orders=min_orders,
        confidence_threshold=confidence_threshold
    )

    predictions: List[PredictionSchema] = []

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
                **analysis,
            )

            predictions.append(prediction)

    # Sorting by days
    predictions.sort(key=lambda p: -p.days_since_last_order)

    return PredictionsResponse(
        predictions=predictions,
        generated_at=datetime.now(),
        total_predictions=len(predictions)
    )
