from datetime import datetime, timedelta, date
from typing import List, Optional, Union


class PurchasePatternAnalyzer:

    def __init__(self, min_requirements: int = 3, confidence_threshold: float = 0.6):
        self.min_requirements = min_requirements
        self.confidence_threshold = confidence_threshold

    def analyze_client_product_pattern(
            self,
            order_dates: List[Union[datetime, date]],
            amounts: List[float]
    ) -> Optional[dict]:


        order_dates = [
            datetime.combine(d, datetime.min.time()) if isinstance(d, date) else d
            for d in order_dates
        ]

        cutoff = datetime.now() - timedelta(days=365)  # 12 months

        filtered_dates = []
        filtered_amounts = []

        for d, a in zip(order_dates, amounts):
            if d >= cutoff:
                filtered_dates.append(d)
                filtered_amounts.append(a)

        if len(filtered_dates) < self.min_requirements:
            return None

        order_dates = filtered_dates
        amounts = filtered_amounts

        if len(order_dates) < self.min_requirements:
            return None

        # Sort by date
        sorted_orders = sorted(zip(order_dates, amounts))
        dates = [d for d, _ in sorted_orders]
        qtys = [q for _, q in sorted_orders]


        cycles = []
        for i in range(1, len(dates)):
            days_diff = (dates[i] - dates[i - 1]).days
            if days_diff > 0:
                cycles.append(days_diff)

        if not cycles:
            return None

        avg_cycle = sum(cycles) / len(cycles)
        variance = sum((c - avg_cycle) ** 2 for c in cycles) / len(cycles)
        std_dev = variance ** 0.5

        # Coefficient of variation (lower = more consistent)
        cv = std_dev / avg_cycle if avg_cycle > 0 else 1
        confidence = max(0, min(1, 1 - cv))

        last_order_date = dates[-1]
        days_since = (datetime.now() - last_order_date).days

        # Predict next purchase date
        expected_next_order_date = last_order_date + timedelta(days=int(avg_cycle))
        days_until_expected = (expected_next_order_date - datetime.now()).days

        # Only return predictions that are actionable (within next 30 days or overdue)
        if days_until_expected < -30 or days_until_expected > 30:
            return None

        # Predict quantity
        recent_qtys = qtys[-3:]
        predicted_qty = sum(recent_qtys) / len(recent_qtys)

        # Determine pattern consistency
        if cv < 0.2:
            pattern_consistency = "highly_regular"
        elif cv < 0.4:
            pattern_consistency = "regular"
        elif cv < 0.6:
            pattern_consistency = "somewhat_regular"
        else:
            pattern_consistency = "irregular"

        return {
            "last_requirement_date": last_order_date.date(),
            "days_since_last_requirement": days_since,
            "predicted_next_purchase_date": expected_next_order_date.date(),
            "average_cycle_days": round(avg_cycle, 1),
            "avg_interval_days": round(avg_cycle, 1),
            "cycle_variance": round(variance, 1),
            "confidence_score": round(confidence, 2),
            "predicted_amount": round(predicted_qty, 2),
            "requirement_count": len(dates),
            "pattern_consistency": pattern_consistency,
        }
