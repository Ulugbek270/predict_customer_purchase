from datetime import datetime
from typing import List, Optional


class PurchasePatternAnalyzer:
    """Analyzes purchase patterns and predicts when clients will buy next"""

    def __init__(self, min_orders: int = 3, confidence_threshold: float = 0.6):
        self.min_orders = min_orders
        self.confidence_threshold = confidence_threshold

    def analyze_client_product_pattern(
            self,
            order_dates: List[datetime],
            quantities: List[float]
    ) -> Optional[dict]:
        """
        Analyze purchase pattern for a specific client-product combination
        Returns: dict with cycle info, confidence, and prediction, or None if insufficient data
        """
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

        # Calculate statistics
        avg_cycle = sum(cycles) / len(cycles)
        variance = sum((c - avg_cycle) ** 2 for c in cycles) / len(cycles)
        std_dev = variance ** 0.5

        # Calculate confidence (inverse of coefficient of variation)
        # Lower variance = higher confidence
        cv = std_dev / avg_cycle if avg_cycle > 0 else 1
        confidence = max(0, min(1, 1 - cv))

        # Calculate days since last order
        last_order_date = dates[-1]
        days_since = (datetime.now() - last_order_date).days

        # Predict quantity (average of last 3 orders)
        recent_qtys = qtys[-3:]
        predicted_qty = sum(recent_qtys) / len(recent_qtys)

        # Determine urgency
        urgency = self._calculate_urgency(days_since, avg_cycle, std_dev, cycles)

        return {
            "last_order_date": last_order_date,
            "days_since_last_order": days_since,
            "average_cycle_days": round(avg_cycle, 1),
            "cycle_variance": round(variance, 1),
            "confidence_score": round(confidence, 2),
            "urgency": urgency,
            "predicted_quantity": round(predicted_qty, 2),
            "order_count": len(dates),
        }

    def _calculate_urgency(self, days_since: int, avg_cycle: float, std_dev: float, cycles: List[int]) -> str:
        """
        Calculate urgency by checking if days_since matches historical purchase intervals
        - High: Within ±5 days of any historical interval OR past average cycle
        - Medium: Within ±10 days of any historical interval
        - Low: Too early
        """
        # Check if current days_since is close to any historical cycle
        min_cycle = min(cycles) if cycles else avg_cycle
        max_cycle = max(cycles) if cycles else avg_cycle

        # HIGH: If we're within ±5 days of any historical interval
        for cycle in cycles:
            if abs(days_since - cycle) <= 5:
                return "high"

        # HIGH: If we've passed the average cycle time
        if days_since >= avg_cycle:
            return "high"

        # MEDIUM: If we're within ±10 days of any historical interval
        for cycle in cycles:
            if abs(days_since - cycle) <= 10:
                return "medium"

        # MEDIUM: If we're approaching the shortest cycle
        if days_since >= (min_cycle * 0.85):
            return "medium"

        # LOW: Too early
        return "low"