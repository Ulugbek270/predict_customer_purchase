from datetime import datetime, timedelta
from typing import List, Optional


class PurchasePatternAnalyzer:

    def __init__(self, min_requirements: int = 3, confidence_threshold: float = 0.6):
        self.min_requirements = min_requirements
        self.confidence_threshold = confidence_threshold

    def analyze_client_product_pattern(
            self,
            order_dates: List[datetime],
            amount: List[float]
    ) -> Optional[dict]:

        # cutoff = datetime.now() - timedelta(days=30 * 24)
        #
        # filtered_dates = []
        # filtered_amount = []
        #
        # for d, a in zip(order_dates, amount):
        #     if d >= cutoff:
        #         filtered_dates.append(d)
        #         filtered_amount.append(a)
        #
        # # If filtered has enough, use filtered, else keep all
        # if len(filtered_dates) >= self.min_requirements:
        #     order_dates = filtered_dates
        #     amount = filtered_amount

        if len(order_dates) < self.min_requirements:
            return None

        # Sort by date
        sorted_orders = sorted(zip(order_dates, amount))
        dates = [d for d, _ in sorted_orders]
        qtys = [q for _, q in sorted_orders]

        # Calculate days between consecutive orders
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

        cv = std_dev / avg_cycle if avg_cycle > 0 else 1
        confidence = max(0, min(1, 1 - cv))

        last_order_date = dates[-1]
        days_since = (datetime.now() - last_order_date).days

        expected_next_order_date = last_order_date + timedelta(days=int(avg_cycle))
        days_until_expected = (expected_next_order_date - datetime.now()).days

        if not (0 <= days_until_expected <= 5):
            return None

        recent_qtys = qtys[-3:]
        predicted_qty = sum(recent_qtys) / len(recent_qtys)

        return {
            "last_requirement_date": last_order_date,
            "days_since_last_requirement": days_since,
            "average_cycle_days": round(avg_cycle, 1),
            "cycle_variance": round(variance, 1),
            "confidence_score": round(confidence, 2),
            "predicted_amount": round(predicted_qty, 2),
            "requirement_count": len(dates),
        }
