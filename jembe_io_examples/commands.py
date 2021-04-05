from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask


def init_commands(app: "Flask"):
    @app.cli.command("load-data")
    def load_data():
        from .db import db
        from .models import Project

        # Create database
        db.create_all()

        db.session.bulk_insert_mappings(
            Project,
            [
                dict(id=index, name=name, description=None,)
                for index, name in enumerate(
                    [
                        "Voice-based E-mail for the Blind",
                        "Automated Robot for Military System (ARMS)",
                        "Unique ID (UID) Management System Project",
                        "Online Voting Using Bluetooth Enabled Mobile Phone",
                        "Wi-Fi Based Mobile Quiz",
                        "Inter-Operability of 802.11e and 802.11",
                        "Semi-Supervised Learning using Graph Kernels",
                        "Gram-Based Fuzzy Keyword Search over Encrypted Data in Cloud Computing",
                        "Battery Optimizer for Android Mobile Devices",
                        "Visual Tracking Using Spare Appearance Model",
                        "Sockets Programming in Python –Building a Python Chat Server",
                        "Security Issue of Cloud-Based Storage",
                        "Pre Touch Sensing with Sea Shell Effect",
                        "Efficient Peer to Peer Similarity Query Processing for High dimensional Data",
                        "CALTOOL Computer-Aided Learning Tool",
                        "XTC Algorithm Based Scalable Wireless Ad hoc Networking IEEE",
                        "Honey Pots a Security System to Identify Black Hat Community in the Networks",
                        "Elevator Control System",
                        "Web-Based Online Library System",
                        "Efficient Coding Technique for Aerospace Tele Command System",
                        "Microcontroller-Based Security System using Sonar",
                        "Tanox Work Force",
                        "SPIRIT –Spontaneous Information and Resource Sharing",
                        "Software Engineering of Scientific Software",
                        "Energy & Power Efficient, Real-Time System Scheduling",
                        "Data-Efficient Robot Reinforcement Learning",
                        "Gaussian Processes for Bayesian State Estimation",
                        "Imitation Learning in Humanoid Robots",
                        "Privacy-Preserving Data Sharing With Anonymous ID Assignment",
                        "SORT- a Self-Organizing Trust Model for Peer-to-Peer Systems",
                        "Information Flow in Bargaining Scenarios",
                        "Simulation and Exploration of Hybrid Systems via Automata",
                        "Combining Kinect and Stereo Depth Measurements",
                        "Band-Aids for Broken Microprocessors",
                        "North East West South Global Unified Reporting Utility (NEWSGURU)",
                        "Mobile Apps in the K-12 Classroom",
                        "Diagnosing Computer Bugs Using Big Data",
                        "A Railway Anti-collision System with Phis Plate Removal Sensing and Auto Track Changing",
                        "A Reverse Engineering Approach for Converting Conventional Turbo C Code to 64bit C#",
                        "Debugging Grids with Machine Learning Techniques",
                        "SMASH-Scalable Multimedia Content Analysis in a High-level Language",
                        "The Design and Implementation of a Consolidated Middle Box Architecture",
                        "Automated Low-Level Analysis and Description of Diverse Intelligent Videos (ALADDIN)",
                        "3D Mobile Game Engine Development Software Project",
                        "Coaching Management Software",
                        "Bug Tracking System",
                        "Development of a Feature-Rich Practical Online Leave Management System (LMS)",
                        "Design and Development of Speed Cash System (SCS)",
                        "Multi-Million Dollar Maintenance Using WLS Algorithms",
                        "DDOS (Distributed Denial of Service) Using Throttle Algorithm",
                        "File System Simulation",
                        "A Railway Anti-Collision System with Auto-Track Changing and Phis Plate Removal Sensing",
                        "Computer Folders ‘Security with a Bluetooth-Enabled Mobile Phone and Rinjdal Security Extension",
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
