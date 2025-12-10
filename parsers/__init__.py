"""
Parsers para diferentes tipos de informes NIR
"""
from .baseline_parser import BaselineParser
from .validation_parser import ValidationParser
from .predictions_parser import PredictionsParser

__all__ = ['BaselineParser', 'ValidationParser', 'PredictionsParser']