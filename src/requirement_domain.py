def get_requirement_domain(sentence):
    sentence_lower = sentence.lower()
    software_keywords = [
        "software",
        "development",
        "testing",
        "deployment",
        "tools",
        "methodologies",
        "integration",
    ]
    hardware_keywords = [
        "hardware",
        "acquisition",
        "installation",
        "maintenance",
        "compatibility",
        "scalability",
    ]
    networks_keywords = [
        "networks",
        "design",
        "implementation",
        "management",
        "security",
        "performance",
    ]
    security_keywords = [
        "security",
        "unauthorized access",
        "firewalls",
        "intrusion detection systems",
        "encryption",
        "training",
    ]
    data_keywords = [
        "data",
        "collection",
        "storage",
        "processing",
        "analysis",
        "privacy regulations",
    ]
    cloud_keywords = [
        "cloud computing",
        "security of cloud computing services",
        "compliance with cloud computing regulations",
    ]
    iot_keywords = [
        "internet of things",
        "security of iot devices",
        "compliance with iot regulations",
    ]
    ai_keywords = [
        "artificial intelligence",
        "security of ai technologies",
        "compliance with ai regulations",
    ]

    if any(keyword in sentence_lower for keyword in software_keywords):
        return "Software"
    elif any(keyword in sentence_lower for keyword in hardware_keywords):
        return "Hardware"
    elif any(keyword in sentence_lower for keyword in networks_keywords):
        return "Networks"
    elif any(keyword in sentence_lower for keyword in security_keywords):
        return "Security"
    elif any(keyword in sentence_lower for keyword in data_keywords):
        return "Data"
    elif any(keyword in sentence_lower for keyword in cloud_keywords):
        return "Cloud computing"
    elif any(keyword in sentence_lower for keyword in iot_keywords):
        return "Internet of Things (IoT)"
    elif any(keyword in sentence_lower for keyword in ai_keywords):
        return "Artificial Intelligence (AI)"
    else:
        return "Other"
