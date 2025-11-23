from datetime import datetime, timedelta
from typing import List, Optional


class PurchasePatternAnalyzer:

    def __init__(self, min_orders: int = 3, confidence_threshold: float = 0.6):
        self.min_orders = min_orders
        self.confidence_threshold = confidence_threshold

    def analyze_client_product_pattern(
            self,
            order_dates: List[datetime],
            quantities: List[float]
    ) -> Optional[dict]:

        if len(order_dates) < self.min_orders:
            return None

        # Sort by date
        sorted_orders = sorted(zip(order_dates, quantities))
        dates = [d for d, _ in sorted_orders]
        qtys = [q for _, q in sorted_orders]

        # Calculate days between consecutive orders
        cycles = []
        for i in range(1, len(dates)):
            days_diff = (dates[i] - dates[i - 1]).days
            if days_diff > 0:  # Ignore same-day orders
                cycles.append(days_diff)

        if not cycles:
            return None

        # Calculate average cycle
        avg_cycle = sum(cycles) / len(cycles)
        variance = sum((c - avg_cycle) ** 2 for c in cycles) / len(cycles)
        std_dev = variance ** 0.5

        # Calculate confidence
        cv = std_dev / avg_cycle if avg_cycle > 0 else 1
        confidence = max(0, min(1, 1 - cv))

        # Last order date
        last_order_date = dates[-1]
        days_since = (datetime.now() - last_order_date).days

        # Expected next order date
        expected_next_order_date = last_order_date + timedelta(days=int(avg_cycle))
        days_until_expected = (expected_next_order_date - datetime.now()).days

        # Only return if within 0-5 days of expected date
        if not (0 <= days_until_expected <= 5):
            return None

        # Predict quantity
        recent_qtys = qtys[-3:]
        predicted_qty = sum(recent_qtys) / len(recent_qtys)

        return {
            "last_order_date": last_order_date,
            "days_since_last_order": days_since,
            "average_cycle_days": round(avg_cycle, 1),
            "expected_next_order_date": expected_next_order_date,
            "days_until_expected": days_until_expected,
            "cycle_variance": round(variance, 1),
            "confidence_score": round(confidence, 2),
            "predicted_quantity": round(predicted_qty, 2),
            "order_count": len(dates),
            "urgency": "high"  # Always high
        }
