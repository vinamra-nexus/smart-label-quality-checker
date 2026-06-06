def generate_suggestions(
    duplicate_count,
    label_count,
    semantic_count,
    mismatch_count
):

    suggestions = []

    if duplicate_count > 0:
        suggestions.append(
            "Remove duplicate records to reduce data redundancy."
        )

    if label_count > 0:
        suggestions.append(
            "Standardize label naming conventions."
        )

    if semantic_count > 0:
        suggestions.append(
            "Review semantically similar records and merge if necessary."
        )

    if mismatch_count > 0:
        suggestions.append(
            "Manually verify potentially mislabeled samples."
        )

    if len(suggestions) == 0:
        suggestions.append(
            "No major issues detected. Dataset quality is good."
        )

    return suggestions