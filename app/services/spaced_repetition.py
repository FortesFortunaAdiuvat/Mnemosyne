from datetime import datetime, timedelta
from typing import Tuple


class SM2Algorithm:
    """
    Implementation of the SM-2 (SuperMemo 2) spaced repetition algorithm
    
    The SM-2 algorithm calculates the next review interval based on:
    - Quality of recall (0-5 scale)
    - Current ease factor (difficulty multiplier)
    - Current interval (days between reviews)
    - Number of repetitions
    """
    
    MIN_EASE_FACTOR = 1.3
    
    def calculate_next_review(
        self, 
        quality: int, 
        ease_factor: float, 
        interval: int, 
        repetitions: int
    ) -> Tuple[int, float, int]:
        """
        Calculate the next review interval using SM-2 algorithm
        
        Args:
            quality: Quality of recall (0-5, where 0=complete blackout, 5=perfect)
            ease_factor: Current ease factor (minimum 1.3)
            interval: Current interval in days
            repetitions: Number of successful repetitions
            
        Returns:
            Tuple of (new_interval, new_ease_factor, new_repetitions)
        """
        
        if quality >= 3:  # Correct response
            if repetitions == 0:
                new_interval = 1
            elif repetitions == 1:
                new_interval = 6
            else:
                new_interval = round(interval * ease_factor)
            
            new_repetitions = repetitions + 1
        else:  # Incorrect response (quality < 3)
            new_repetitions = 0
            new_interval = 1
        
        # Update ease factor based on quality
        # Formula: EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
        new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # Ensure ease factor doesn't go below minimum
        new_ease_factor = max(self.MIN_EASE_FACTOR, new_ease_factor)
        
        return new_interval, new_ease_factor, new_repetitions
    
    def calculate_next_review_date(
        self, 
        quality: int, 
        ease_factor: float, 
        interval: int, 
        repetitions: int,
        base_date: datetime = None
    ) -> Tuple[datetime, float, int, int]:
        """
        Calculate the next review date using SM-2 algorithm
        
        Args:
            quality: Quality of recall (0-5)
            ease_factor: Current ease factor
            interval: Current interval in days
            repetitions: Number of successful repetitions
            base_date: Base date to calculate from (defaults to now)
            
        Returns:
            Tuple of (next_review_date, new_ease_factor, new_interval, new_repetitions)
        """
        if base_date is None:
            base_date = datetime.now()
        
        new_interval, new_ease_factor, new_repetitions = self.calculate_next_review(
            quality, ease_factor, interval, repetitions
        )
        
        next_review_date = base_date + timedelta(days=new_interval)
        
        return next_review_date, new_ease_factor, new_interval, new_repetitions
