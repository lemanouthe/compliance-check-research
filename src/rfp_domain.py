def get_rfp_domain(sentence):
    sentence_lower = sentence.lower()
    it_keywords = [
        "information technology",
        "it",
        "software",
        "hardware",
        "cloud computing",
    ]
    construction_keywords = ["construction", "building", "road", "bridge"]
    engineering_keywords = ["engineering", "design", "infrastructure"]
    scientific_keywords = [
        "scientific",
        "research",
        "development",
        "products",
        "technologies",
    ]
    healthcare_keywords = [
        "healthcare",
        "medical care",
        "drugs",
        "healthcare information systems",
    ]
    logistics_keywords = [
        "logistics",
        "transportation",
        "warehousing",
        "inventory management",
    ]
    manufacturing_keywords = ["manufacturing", "production", "assembly", "testing"]
    energy_keywords = ["energy", "electricity", "transmission", "distribution"]
    environmental_keywords = [
        "environmental",
        "remediation",
        "waste management",
        "natural resources",
    ]

    if any(keyword in sentence_lower for keyword in it_keywords):
        return "Information Technology (IT)"
    elif any(keyword in sentence_lower for keyword in construction_keywords):
        return "Construction"
    elif any(keyword in sentence_lower for keyword in engineering_keywords):
        return "Engineering"
    elif any(keyword in sentence_lower for keyword in scientific_keywords):
        return "Scientific"
    elif any(keyword in sentence_lower for keyword in healthcare_keywords):
        return "Healthcare"
    elif any(keyword in sentence_lower for keyword in logistics_keywords):
        return "Logistics"
    elif any(keyword in sentence_lower for keyword in manufacturing_keywords):
        return "Manufacturing"
    elif any(keyword in sentence_lower for keyword in energy_keywords):
        return "Energy"
    elif any(keyword in sentence_lower for keyword in environmental_keywords):
        return "Environmental"
    else:
        return "Other"
