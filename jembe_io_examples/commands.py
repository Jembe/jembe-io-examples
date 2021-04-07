from typing import TYPE_CHECKING
from random import randint

if TYPE_CHECKING:
    from flask import Flask


def init_commands(app: "Flask"):
    @app.cli.command("load-data")
    def load_data():
        from .db import db
        from .models import Project, Note

        # Create database
        db.create_all()
        db.session.bulk_insert_mappings(
            Project,
            [
                dict(id=index, name=name, description=None,)
                for index, name in enumerate(
                    [
                        "Speech Stress Analysis based Cheap Lie Detector for Loyalty Test",
                        "Credit Card Reader with Face Recognition based on Webcam",
                        "Recognition of Hand Movement for Paralytic Persons Based on a Neural Network",
                        "Network Security Implementation Layer through Voice Biometric",
                        "Agent-Based Blocking and Response, Intrusion Detection using Signature",
                        "Load Balancing of Artificial Intelligence Network using Ant Colony Optimization",
                        "Authentication and Adaptive Security for DNS System",
                        "Multicasting of Bandwidth Efficient Video in Multiradio Multicellular Wireless networks",
                        "ADHOC Networks Based Bandwidth Estimation of IEEE 802.11",
                        "Data Mining Technique Based Building Intelligent Shopping for Web Services",
                        "Automatic Teller Machine Network Implementation based Controlling of CAC Connection Admission",
                        "Adaptive Coaching and Co-Operative System for MANETS",
                        "Multidimensional and Color Imaging Projections",
                        "Inter-Domain Packet Filters based Controlling of IP Spoofing",
                        "Hidden Markov Models Based Credit Card Fraud Detection",
                        "XML Enable SQL Server Based Data Storage and Minimization",
                        "Artificial Neural Network Based Verification of Digital Signature",
                        "Design and Implementation of E Secure Transaction",
                        "Pattern Recognition and Dynamic Character Using Neural Network",
                        "Verification of Dynamic Signature Using Pattern Signature",
                        "Data Integrity Maintenance and Dynamic University Linking",
                        "Filtering and Analyzing of Effective Packet System for ATM Network",
                        "Efficient and Distribution and Secure Content Processing by Cooperative Intermediaries",
                        "Rule Mining Algorithm for Efficient Association in Distributed Databases",
                        "Digest Algorithm for Efficient Message for Data Security",
                        "Using Concurrent Engineering Train Simulation Based on Genetic Algorithm",
                        "Travelling Salesman and Genetic Algorithm Problem Using ATL COM and C#",
                        "Channel Rate Allocation for Scalable Video Streaming Using Genetic Algorithm over Error-Prone Networks Based on GOP",
                        "High-Speed Face Recognition Based on RBF Neural Networks and Discrete Cosine Transform.",
                    ]
                )
            ],
        )
        db.session.bulk_insert_mappings(
            Note,
            [
                dict(id=index, name=name, description=None, project_id=project_id)
                for index, (name, project_id) in enumerate(
                    [
                        ("Voice-based E-mail for the Blind", randint(1, 29)),
                        ("Automated Robot for Military System (ARMS)", randint(1, 29)),
                        ("Unique ID (UID) Management System Project", randint(1, 29)),
                        (
                            "Online Voting Using Bluetooth Enabled Mobile Phone",
                            randint(1, 29),
                        ),
                        ("Wi-Fi Based Mobile Quiz", randint(1, 29)),
                        ("Inter-Operability of 802.11e and 802.11", randint(1, 29)),
                        (
                            "Semi-Supervised Learning using Graph Kernels",
                            randint(1, 29),
                        ),
                        (
                            "Gram-Based Fuzzy Keyword Search over Encrypted Data in Cloud Computing",
                            randint(1, 29),
                        ),
                        (
                            "Battery Optimizer for Android Mobile Devices",
                            randint(1, 29),
                        ),
                        (
                            "Visual Tracking Using Spare Appearance Model",
                            randint(1, 29),
                        ),
                        (
                            "Sockets Programming in Python –Building a Python Chat Server",
                            randint(1, 29),
                        ),
                        ("Security Issue of Cloud-Based Storage", randint(1, 29)),
                        ("Pre Touch Sensing with Sea Shell Effect", randint(1, 29)),
                        (
                            "Efficient Peer to Peer Similarity Query Processing for High dimensional Data",
                            randint(1, 29),
                        ),
                        ("CALTOOL Computer-Aided Learning Tool", randint(1, 29)),
                        (
                            "XTC Algorithm Based Scalable Wireless Ad hoc Networking IEEE",
                            randint(1, 29),
                        ),
                        (
                            "Honey Pots a Security System to Identify Black Hat Community in the Networks",
                            randint(1, 29),
                        ),
                        ("Elevator Control System", randint(1, 29)),
                        ("Web-Based Online Library System", randint(1, 29)),
                        (
                            "Efficient Coding Technique for Aerospace Tele Command System",
                            randint(1, 29),
                        ),
                        (
                            "Microcontroller-Based Security System using Sonar",
                            randint(1, 29),
                        ),
                        ("Tanox Work Force", randint(1, 29)),
                        (
                            "SPIRIT –Spontaneous Information and Resource Sharing",
                            randint(1, 29),
                        ),
                        ("Software Engineering of Scientific Software", randint(1, 29)),
                        (
                            "Energy & Power Efficient, Real-Time System Scheduling",
                            randint(1, 29),
                        ),
                        ("Data-Efficient Robot Reinforcement Learning", randint(1, 29)),
                        (
                            "Gaussian Processes for Bayesian State Estimation",
                            randint(1, 29),
                        ),
                        ("Imitation Learning in Humanoid Robots", randint(1, 29)),
                        (
                            "Privacy-Preserving Data Sharing With Anonymous ID Assignment",
                            randint(1, 29),
                        ),
                        (
                            "SORT- a Self-Organizing Trust Model for Peer-to-Peer Systems",
                            randint(1, 29),
                        ),
                        ("Information Flow in Bargaining Scenarios", randint(1, 29)),
                        (
                            "Simulation and Exploration of Hybrid Systems via Automata",
                            randint(1, 29),
                        ),
                        (
                            "Combining Kinect and Stereo Depth Measurements",
                            randint(1, 29),
                        ),
                        ("Band-Aids for Broken Microprocessors", randint(1, 29)),
                        (
                            "North East West South Global Unified Reporting Utility (NEWSGURU)",
                            randint(1, 29),
                        ),
                        ("Mobile Apps in the K-12 Classroom", randint(1, 29)),
                        ("Diagnosing Computer Bugs Using Big Data", randint(1, 29)),
                        (
                            "A Railway Anti-collision System with Phis Plate Removal Sensing and Auto Track Changing",
                            randint(1, 29),
                        ),
                        (
                            "A Reverse Engineering Approach for Converting Conventional Turbo C Code to 64bit C#",
                            randint(1, 29),
                        ),
                        (
                            "Debugging Grids with Machine Learning Techniques",
                            randint(1, 29),
                        ),
                        (
                            "SMASH-Scalable Multimedia Content Analysis in a High-level Language",
                            randint(1, 29),
                        ),
                        (
                            "The Design and Implementation of a Consolidated Middle Box Architecture",
                            randint(1, 29),
                        ),
                        (
                            "Automated Low-Level Analysis and Description of Diverse Intelligent Videos (ALADDIN)",
                            randint(1, 29),
                        ),
                        (
                            "3D Mobile Game Engine Development Software Project",
                            randint(1, 29),
                        ),
                        ("Coaching Management Software", randint(1, 29)),
                        ("Bug Tracking System", randint(1, 29)),
                        (
                            "Development of a Feature-Rich Practical Online Leave Management System (LMS)",
                            randint(1, 29),
                        ),
                        (
                            "Design and Development of Speed Cash System (SCS)",
                            randint(1, 29),
                        ),
                        (
                            "Multi-Million Dollar Maintenance Using WLS Algorithms",
                            randint(1, 29),
                        ),
                        (
                            "DDOS (Distributed Denial of Service) Using Throttle Algorithm",
                            randint(1, 29),
                        ),
                        ("File System Simulation", randint(1, 29)),
                        (
                            "A Railway Anti-Collision System with Auto-Track Changing and Phis Plate Removal Sensing",
                            randint(1, 29),
                        ),
                        (
                            "Computer Folders ‘Security with a Bluetooth-Enabled Mobile Phone and Rinjdal Security Extension",
                            randint(1, 29),
                        ),
                    ]
                )
            ],
        )
