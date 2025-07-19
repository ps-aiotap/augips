"""
Debug utilities for Augips framework
"""

import sys
import traceback
from typing import Any, Optional


def debug_print(message: str, obj: Optional[Any] = None, error: Optional[Exception] = None) -> None:
    """
    Print debug information with consistent formatting
    
    Args:
        message: Debug message
        obj: Optional object to print
        error: Optional exception to print
    """
    print(f"[DEBUG] {message}")
    
    if obj is not None:
        print(f"[DEBUG] Object: {obj}")
    
    if error is not None:
        print(f"[DEBUG] Error: {str(error)}")
        print(f"[DEBUG] Error type: {type(error)}")
        print("[DEBUG] Traceback:")
        traceback.print_exc(file=sys.stdout)