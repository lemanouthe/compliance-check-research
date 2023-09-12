def get_confidence_factor(sentence):
    sentence_lower = sentence.lower()
    specificity_keywords = [
        "specific",
        "detailed",
        "clear instructions",
        "precise functionality",
        "features",
        "deliverables",
    ]
    unambiguous_keywords = [
        "eliminate ambiguity",
        "clear understanding",
        "little room for misinterpretation",
    ]
    measurable_keywords = [
        "measurable criteria",
        "performance metrics",
        "quality standards",
        "key performance indicators",
        "kpis",
    ]
    verifiable_keywords = [
        "verifiable",
        "tested",
        "validated",
        "compliance with requirements",
    ]

    confidence_score = 0

    if any(keyword in sentence_lower for keyword in specificity_keywords):
        confidence_score += 0.25

    if any(keyword in sentence_lower for keyword in unambiguous_keywords):
        confidence_score += 0.25

    if any(keyword in sentence_lower for keyword in measurable_keywords):
        confidence_score += 0.25

    if any(keyword in sentence_lower for keyword in verifiable_keywords):
        confidence_score += 0.25

    return confidence_score
