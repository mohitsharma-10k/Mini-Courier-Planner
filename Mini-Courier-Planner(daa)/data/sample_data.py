"""
Sample Datasets for Mini-Courier Planner
Models Gurugram / NCR City Logistics Hub and Delivery Points
"""
from typing import List, Tuple
from models.parcel import Parcel
from models.delivery_point import DeliveryPoint
from models.graph import RoadGraph


def get_sample_city_graph() -> RoadGraph:
    """
    Constructs a realistic 10-node urban road network with Depot and delivery zones.
    Node 0 is the Central Warehouse Hub (Depot).
    """
    g = RoadGraph()

    # Define Nodes (ID, Name, X-coord km, Y-coord km, is_depot)
    locations = [
        DeliveryPoint(0, "Central Courier Hub (Depot)", 0.0, 0.0, is_depot=True),
        DeliveryPoint(1, "Cyber City Tower A", 2.5, 4.0),
        DeliveryPoint(2, "Sector 29 Market", 4.0, 1.5),
        DeliveryPoint(3, "Golf Course Road Ph-1", 6.0, 3.5),
        DeliveryPoint(4, "Sohna Road Hub", 3.0, -3.0),
        DeliveryPoint(5, "MG Road Metro Complex", 1.5, 2.0),
        DeliveryPoint(6, "Udyog Vihar Ph-IV", 1.0, 5.5),
        DeliveryPoint(7, "Ambience Mall Arcade", -1.5, 6.0),
        DeliveryPoint(8, "South City I Colony", 5.0, -1.0),
        DeliveryPoint(9, "K.R. Mangalam Campus Zone", -2.0, -4.0),
    ]

    for loc in locations:
        g.add_node(loc)

    # Road Segments (Node u, Node v, Distance in km)
    edges: List[Tuple[int, int, float]] = [
        # Depot connections
        (0, 5, 2.6),    # Depot -> MG Road
        (0, 4, 4.2),    # Depot -> Sohna Road
        (0, 9, 4.5),    # Depot -> KRMU Campus Zone
        (0, 2, 4.3),    # Depot -> Sector 29
        
        # Cyber City & Ambience & Udyog Vihar cluster
        (5, 1, 2.8),    # MG Road -> Cyber City
        (1, 6, 2.1),    # Cyber City -> Udyog Vihar
        (6, 7, 2.9),    # Udyog Vihar -> Ambience
        (5, 7, 5.0),    # MG Road -> Ambience direct link
        (1, 2, 3.2),    # Cyber City -> Sector 29
        
        # Golf Course & Eastern corridor
        (2, 3, 3.0),    # Sector 29 -> Golf Course
        (1, 3, 4.1),    # Cyber City -> Golf Course
        (3, 8, 4.7),    # Golf Course -> South City I
        
        # Southern & Western corridor
        (2, 8, 2.7),    # Sector 29 -> South City I
        (8, 4, 2.9),    # South City I -> Sohna Road
        (4, 9, 5.2),    # Sohna Road -> KRMU Zone
    ]

    for u, v, dist in edges:
        g.add_edge(u, v, dist, bidirectional=True)

    return g


def get_small_test_parcels() -> List[Parcel]:
    """
    Standard small dataset of 10 parcels for Phase 1 & 2 verification.
    Provides clear variety in weight, value, deadlines, and delivery points.
    """
    return [
        Parcel("P101", "Aakash Sharma",  1, weight_kg=3.5, value=75,  deadline_hour=2.0, description="Laptop Battery"),
        Parcel("P102", "Priya Verma",    2, weight_kg=1.8, value=40,  deadline_hour=4.5, description="Books & Stationery"),
        Parcel("P103", "Rohit Malhotra", 3, weight_kg=6.0, value=120, deadline_hour=1.5, description="Medical Supplies (URGENT)"),
        Parcel("P104", "Sneha Kapoor",   4, weight_kg=4.2, value=85,  deadline_hour=3.0, description="Smartphone & Accessories"),
        Parcel("P105", "Vikas Patel",    5, weight_kg=2.0, value=30,  deadline_hour=5.0, description="Apparel Order"),
        Parcel("P106", "Ananya Rao",     6, weight_kg=5.5, value=95,  deadline_hour=2.5, description="Lab Equipment Component"),
        Parcel("P107", "Manish Tiwari",  7, weight_kg=7.0, value=110, deadline_hour=6.0, description="Home Audio Speaker"),
        Parcel("P108", "Neha Gupta",     8, weight_kg=1.5, value=60,  deadline_hour=1.8, description="Express Documents"),
        Parcel("P109", "Deepak Joshi",   9, weight_kg=3.0, value=50,  deadline_hour=4.0, description="Gift Hamper"),
        Parcel("P110", "Pooja Mehta",    3, weight_kg=4.0, value=70,  deadline_hour=3.5, description="Designer Footwear"),
    ]
