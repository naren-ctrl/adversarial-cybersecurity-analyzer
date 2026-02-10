# File: src/05_ensemble_learning/risk_scorer.py

class RiskScorer:
    """
    Calculate risk score for detected threats
    """
    
    def __init__(self):
        self.threat_severity = {
            'normal': 0,
            'brute_force': 7,
            'port_scan': 5,
            'dos': 9
        }
        
        self.context_factors = {
            'business_hours': 0.7,    # Less risk during work hours
            'after_hours': 1.3,       # More risk at night
            'weekend': 1.5,           # Even more on weekends
            'target_critical': 2.0,   # If targeting critical server
            'repeated_attempts': 1.8  # If multiple attempts
        }
    
    def calculate_risk_score(self, detection_result, context):
        """
        Calculate 0-100 risk score
        """
        # Base score from prediction confidence
        base_score = detection_result.get('confidence', 50)
        
        # Adjust for threat type
        threat_type = detection_result.get('prediction', 'normal')
        severity = self.threat_severity.get(threat_type, 0)
        base_score *= (severity / 5)  # Scale by severity
        
        # Apply context factors
        context_multiplier = 1.0
        for factor, value in context.items():
            if value:  # If factor is present
                context_multiplier *= self.context_factors.get(factor, 1.0)
        
        risk_score = min(100, base_score * context_multiplier)
        
        # Adversarial attack increases risk
        if detection_result.get('adversarial_attack_detected'):
            risk_score = min(100, risk_score * 1.5)
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = "CRITICAL"
            action = "IMMEDIATE RESPONSE REQUIRED"
        elif risk_score >= 60:
            risk_level = "HIGH"
            action = "Investigate immediately"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
            action = "Review when possible"
        else:
            risk_level = "LOW"
            action = "Monitor"
        
        return {
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'recommended_action': action,
            'breakdown': {
                'base_score': base_score,
                'threat_severity': severity,
                'context_multiplier': context_multiplier,
                'factors_considered': list(context.keys())
            }
        }