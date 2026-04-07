def evaluate_policy(receipt_text, purpose):
    receipt_text = receipt_text.lower()
    purpose = purpose.lower()

    # Meals detection
    if any(word in receipt_text for word in ["restaurant", "burger", "pasta", "food", "dining"]):
        return {
            "category": "meals",
            "result": "Approved (Meal expense)"
        }

    # Travel detection
    if any(word in receipt_text for word in ["uber", "taxi", "ola"]):
        return {
            "category": "travel",
            "result": "Approved (Transport expense)"
        }

    # Fallback
    if receipt_text.strip() == "":
        return {
            "category": "unknown",
            "result": "Receipt empty"
        }

    return {
        "category": "general",
        "result": "Approved (General expense)"
    }