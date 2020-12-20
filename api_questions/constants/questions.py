

class Questions():
    QUESTIONS = [
        {
            "content": "How much are you going to spend?",
            "options": [
                "Up to 5000000",
                "Up to 10000000",
                "Up to 15000000",
                "Up to 20000000",
                "Up to 25000000",
                "Up to 30000000",
                "Up to 40000000",
                "Unlimited",
            ],
            "train": False,
            "required": True,
            "multiple": False,
            "spec": True
        },
        {
            "content": "Which of the following will you use frequently?",
            "options": [
                "Web browsing",
                "Document",
                "Watching Movies",
                "Light Gaming",
                "Heavy Gaming",
                "Photo editing (pro)",
                "Photo editing (basic)",
                "Video production (pro)",
                "Video production basic)",
                "3D design",
                "Programming"
            ],
            "train": True,
            "required": True,
            "multiple": True,
            "spec": False
        },
        {
            "content": "Which brand do you prefer?",
            "options": [
                "HP",
                "Dell",
                "Acer",
                "Asus",
                "Lenovo",
                "Apple",
                "MSI",
                "Any"
            ],
            "train": False,
            "required": False,
            "multiple": True,
            "spec": True
        },
        {
            "content": "Are any of these important to you?",
            "options": [
                "Touchscreen laptop",
                "Having SSD",
                "Working in low light conditions",
                "Fingerprint",
            ],
            "train": False,
            "required": False,
            "multiple": True,
            "spec": False
        },
        {
            "content": "Is there a specific screen size you prefer?",
            "options": [
                "Very small (<= 13')",
                "Small (14')",
                "Medium (15')",
                "Large (> 17')",
                "Any size"
            ],
            "train": False,
            "required": False,
            "multiple": True,
            "spec": True
        },
        {
            "content": "Which operating system are you comfortable with?",
            "options": [
                "Microsoft windows",
                "Mac os",
                "Linux",
                "Any os"
            ],
            "train": False,
            "required": False,
            "multiple": False,
            "spec": False
        },
        {
            "content": "Which series cpu you prefer?",
            "options": [
                "Intel pentium",
                "Intel core i3",
                "Intel core i5",
                "Intel core i7",
                "Amd"
            ],
            "train": False,
            "required": False,
            "multiple": True,
            "spec": True
        },
        {
            "content": "Do you want a good graphic cards?",
            "options": [
                "Integrated intel",
                "Nvidia geforce GT series",
                "Nvidia geforce GTX series",
                "Amd series"
            ],
            "train": False,
            "required": False,
            "multiple": True,
            "spec": True
        },
        {
            "content": "How about weight?",
            "options": [
                "Very light",
                "Medium",
                "Don't bother"
            ],
            "train": True,
            "required": False,
            "multiple": True,
            "spec": True
        },

    ]