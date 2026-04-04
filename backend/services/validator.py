def is_blurry(text):
    return len(text.strip())<20

def validate_receipt(text):
    if is_blurry(text):
        return False, "Receipt is unclear or unreadable"
    return True, "Valid receipt"