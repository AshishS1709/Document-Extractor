from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ScoreComponent:
    """Represents a component of the confidence score."""
    name: str
    weight: float
    value: float
    description: str = ""

class ConfidenceScorer:
    """
    Calculates confidence scores for extracted document data.
    
    Confidence scores are calculated based on multiple factors:
    - OCR confidence
    - Field presence
    - Field validation
    - Data type consistency
    - Pattern matching
    """
    
    def __init__(self):
        self.components: List[ScoreComponent] = []
        self.weights = {
            'ocr_confidence': 0.3,
            'field_presence': 0.2,
            'validation': 0.3,
            'data_type': 0.1,
            'pattern_match': 0.1
        }
    
    def calculate_score(self, extraction_result: Dict[str, Any]) -> float:
        """
        Calculate overall confidence score for an extraction result.
        
        Args:
            extraction_result: Dictionary containing extraction results and metadata
            
        Returns:
            Float between 0 and 1 representing the confidence score
        """
        self.components = []
        
        # Calculate OCR confidence component
        ocr_confidence = extraction_result.get('metadata', {}).get('ocr_confidence', 0.8)
        self._add_component('ocr_confidence', self.weights['ocr_confidence'], ocr_confidence,
                          "Confidence of the OCR text extraction")
        
        # Calculate field presence component
        extracted_fields = extraction_result.get('extracted_data', {})
        required_fields = extraction_result.get('metadata', {}).get('required_fields', [])
        
        if required_fields:
            present_fields = sum(1 for field in required_fields if field in extracted_fields)
            field_presence = present_fields / len(required_fields)
            self._add_component('field_presence', self.weights['field_presence'], field_presence,
                              "Proportion of required fields that were extracted")
        
        # Calculate validation component
        validation_errors = extraction_result.get('validation', {}).get('errors', {})
        total_fields = len(extracted_fields)
        
        if total_fields > 0:
            validated_fields = total_fields - len(validation_errors)
            validation_score = validated_fields / total_fields
            self._add_component('validation', self.weights['validation'], validation_score,
                              "Proportion of fields that passed validation")
        
        # Calculate data type consistency
        type_errors = sum(
            1 for field_errors in validation_errors.values() 
            if any('Expected type' in str(err) for err in field_errors)
        )
        
        if total_fields > 0:
            type_consistency = 1 - (type_errors / total_fields)
            self._add_component('data_type', self.weights['data_type'], type_consistency,
                              "Proportion of fields with correct data types")
        
        # Calculate pattern matching score
        pattern_errors = sum(
            1 for field_errors in validation_errors.values() 
            if any('pattern' in str(err).lower() for err in field_errors)
        )
        
        if total_fields > 0:
            pattern_score = 1 - (pattern_errors / total_fields)
            self._add_component('pattern_match', self.weights['pattern_match'], pattern_score,
                              "Proportion of fields that matched expected patterns")
        
        # Calculate weighted sum
        total_weight = sum(comp.weight for comp in self.components)
        if total_weight > 0:
            weighted_sum = sum(comp.weight * comp.value for comp in self.components)
            final_score = weighted_sum / total_weight
        else:
            final_score = 0.0
        
        return max(0.0, min(1.0, final_score))  # Clamp between 0 and 1
    
    def get_score_breakdown(self) -> List[Dict[str, Any]]:
        """Get detailed breakdown of score components."""
        return [
            {
                'name': comp.name,
                'weight': comp.weight,
                'value': comp.value,
                'weighted_value': comp.weight * comp.value,
                'description': comp.description
            }
            for comp in self.components
        ]
    
    def _add_component(self, name: str, weight: float, value: float, description: str = ""):
        """Add a score component."""
        self.components.append(
            ScoreComponent(
                name=name,
                weight=weight,
                value=value,
                description=description
            )
        )
    
    def adjust_weights(self, new_weights: Dict[str, float]):
        """
        Adjust the weights of score components.
        
        Args:
            new_weights: Dictionary of component names to new weights
        """
        for component, weight in new_weights.items():
            if component in self.weights:
                self.weights[component] = max(0.0, min(1.0, weight))
