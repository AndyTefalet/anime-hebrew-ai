"""RTL/BiDi text processing for Hebrew subtitle rendering in LTR contexts."""
import arabic_reshaper
from bidi.algorithm import get_display


def fix_hebrew_text(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)
