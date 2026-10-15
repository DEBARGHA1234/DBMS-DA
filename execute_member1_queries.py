import os
import certifi
import json
from dotenv import load_dotenv
import neo4j

load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = neo4j.GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def run_cypher(session, query, params=None):
    result = session.run(query, params or {})
    records = [record.data() for record in result]
    summary = result.consume()
    return records, summary

def main():
    print(f"Connecting to Neo4j Aura at {URI}...")
    with driver.session() as session:
        # Step 1: Connection Test
        print("1. Running Connection Test...")
        rec1, sum1 = run_cypher(session, "RETURN 'Neo4j is working' AS status;")
        print(f"   -> Result: {rec1}")

        # Step 2: Create Uniqueness Constraints
        print("2. Creating uniqueness constraints...")
        constraints = [
            ("customer_id_unique", "CREATE CONSTRAINT customer_id_unique IF NOT EXISTS FOR (n:Customer) REQUIRE n.customerId IS UNIQUE;"),
            ("vendor_id_unique", "CREATE CONSTRAINT vendor_id_unique IF NOT EXISTS FOR (n:Vendor) REQUIRE n.vendorId IS UNIQUE;"),
            ("food_item_id_unique", "CREATE CONSTRAINT food_item_id_unique IF NOT EXISTS FOR (n:FoodItem) REQUIRE n.itemId IS UNIQUE;"),
            ("order_id_unique", "CREATE CONSTRAINT order_id_unique IF NOT EXISTS FOR (n:Order) REQUIRE n.orderId IS UNIQUE;"),
            ("delivery_partner_id_unique", "CREATE CONSTRAINT delivery_partner_id_unique IF NOT EXISTS FOR (n:DeliveryPartner) REQUIRE n.partnerId IS UNIQUE;"),
            ("payment_id_unique", "CREATE CONSTRAINT payment_id_unique IF NOT EXISTS FOR (n:Payment) REQUIRE n.paymentId IS UNIQUE;"),
            ("review_id_unique", "CREATE CONSTRAINT review_id_unique IF NOT EXISTS FOR (n:Review) REQUIRE n.reviewId IS UNIQUE;")
        ]
        for name, cypher in constraints:
            session.run(cypher)
            print(f"   -> Constraint ensured: {name}")

        # Check existing constraints
        constraints_res = session.run("SHOW CONSTRAINTS YIELD name, type, entityType, properties;").data()
        print(f"   -> Active constraints in DB: {len(constraints_res)}")

        # Step 3: Load Sample Data
        print("3. Loading 5.1 Customers...")
        run_cypher(session, """
        UNWIND [
          {id: 101, name: 'Aarav', email: 'aarav@example.com'},
          {id: 102, name: 'Diya', email: 'diya@example.com'},
          {id: 103, name: 'Kabir', email: 'kabir@example.com'},
          {id: 104, name: 'Meera', email: 'meera@example.com'}
        ] AS row
        MERGE (c:Customer {customerId: row.id})
        SET c.name = row.name, c.email = row.email;
        """)

        print("4. Loading 5.2 Vendors...")
        run_cypher(session, """
        UNWIND [
          {id: 201, name: 'Spice House', cuisine: 'Indian', location: 'Chennai'},
          {id: 202, name: 'Pasta Point', cuisine: 'Italian', location: 'Chennai'},
          {id: 203, name: 'Green Bowl', cuisine: 'Healthy', location: 'Chennai'},
          {id: 204, name: 'Wok Express', cuisine: 'Chinese', location: 'Chennai'}
        ] AS row
        MERGE (v:Vendor {vendorId: row.id})
        SET v.name = row.name, v.cuisine = row.cuisine, v.location = row.location;
        """)

        print("5. Loading 5.3 Food Items & SOLD_BY...")
        run_cypher(session, """
        UNWIND [
          {id: 301, name: 'Paneer Biryani', price: 220, category: 'Main Course', vendorId: 201},
          {id: 302, name: 'Masala Dosa', price: 120, category: 'Breakfast', vendorId: 201},
          {id: 303, name: 'Pasta Alfredo', price: 260, category: 'Main Course', vendorId: 202},
          {id: 304, name: 'Veg Salad Bowl', price: 180, category: 'Healthy', vendorId: 203},
          {id: 305, name: 'Veg Noodles', price: 190, category: 'Main Course', vendorId: 204},
          {id: 306, name: 'Margherita Pizza', price: 280, category: 'Main Course', vendorId: 202}
        ] AS row
        MATCH (v:Vendor {vendorId: row.vendorId})
        MERGE (f:FoodItem {itemId: row.id})
        SET f.name = row.name, f.price = row.price, f.category = row.category
        MERGE (f)-[:SOLD_BY]->(v);
        """)

        print("6. Loading 5.4 Orders & PLACES...")
        run_cypher(session, """
        UNWIND [
          {id: 401, customerId: 101, status: 'Placed', total: 220, day: '2026-10-13'},
          {id: 402, customerId: 102, status: 'Preparing', total: 380, day: '2026-10-13'},
          {id: 403, customerId: 101, status: 'Delivered', total: 260, day: '2026-10-12'},
          {id: 404, customerId: 103, status: 'Delivered', total: 190, day: '2026-10-11'},
          {id: 405, customerId: 104, status: 'Placed', total: 280, day: '2026-10-13'}
        ] AS row
        MATCH (c:Customer {customerId: row.customerId})
        MERGE (o:Order {orderId: row.id})
        SET o.status = row.status,
            o.totalAmount = row.total,
            o.orderDate = date(row.day)
        MERGE (c)-[:PLACES]->(o);
        """)

        print("7. Loading 5.5 Connect orders to food items CONTAINS...")
        run_cypher(session, """
        UNWIND [
          {orderId: 401, itemId: 301, quantity: 1},
          {orderId: 402, itemId: 302, quantity: 1},
          {orderId: 402, itemId: 304, quantity: 1},
          {orderId: 403, itemId: 303, quantity: 1},
          {orderId: 404, itemId: 305, quantity: 1},
          {orderId: 405, itemId: 306, quantity: 1}
        ] AS row
        MATCH (o:Order {orderId: row.orderId}),
              (f:FoodItem {itemId: row.itemId})
        MERGE (o)-[r:CONTAINS]->(f)
        SET r.quantity = row.quantity;
        """)

        print("8. Loading 6.1 Delivery Partners & ASSIGNED_TO...")
        run_cypher(session, """
        UNWIND [
          {id: 601, name: 'Rohan', availability: 'Busy'},
          {id: 602, name: 'Isha', availability: 'Available'},
          {id: 603, name: 'Dev', availability: 'Busy'}
        ] AS row
        MERGE (d:DeliveryPartner {partnerId: row.id})
        SET d.name = row.name, d.availability = row.availability;
        """)
        run_cypher(session, """
        MATCH (o:Order {orderId: 401}), (d:DeliveryPartner {partnerId: 601})
        MERGE (o)-[:ASSIGNED_TO]->(d);
        """)
        run_cypher(session, """
        MATCH (o:Order {orderId: 402}), (d:DeliveryPartner {partnerId: 602})
        MERGE (o)-[:ASSIGNED_TO]->(d);
        """)
        run_cypher(session, """
        MATCH (o:Order {orderId: 403}), (d:DeliveryPartner {partnerId: 603})
        MERGE (o)-[:ASSIGNED_TO]->(d);
        """)

        print("9. Loading 6.2 Payments & HAS_PAYMENT...")
        run_cypher(session, """
        UNWIND [
          {id: 501, orderId: 401, amount: 220, method: 'UPI', status: 'Paid'},
          {id: 502, orderId: 402, amount: 380, method: 'Card', status: 'Pending'},
          {id: 503, orderId: 403, amount: 260, method: 'UPI', status: 'Paid'},
          {id: 504, orderId: 404, amount: 190, method: 'Cash', status: 'Paid'},
          {id: 505, orderId: 405, amount: 280, method: 'Card', status: 'Pending'}
        ] AS row
        MATCH (o:Order {orderId: row.orderId})
        MERGE (p:Payment {paymentId: row.id})
        SET p.amount = row.amount, p.method = row.method, p.status = row.status
        MERGE (o)-[:HAS_PAYMENT]->(p);
        """)

        print("10. Loading 6.3 Reviews & WROTE / ABOUT...")
        run_cypher(session, """
        UNWIND [
          {id: 701, customerId: 101, vendorId: 201, rating: 5, comment: 'Great taste'},
          {id: 702, customerId: 102, vendorId: 202, rating: 4, comment: 'Good pasta'},
          {id: 703, customerId: 103, vendorId: 204, rating: 4, comment: 'Quick service'}
        ] AS row
        MATCH (c:Customer {customerId: row.customerId}),
              (v:Vendor {vendorId: row.vendorId})
        MERGE (r:Review {reviewId: row.id})
        SET r.rating = row.rating, r.comment = row.comment
        MERGE (c)-[:WROTE]->(r)
        MERGE (r)-[:ABOUT]->(v);
        """)

        # Step 4: Validation Queries
        print("11. Running Validation Queries...")
        
        # 7.1 Count nodes by label
        q7_1 = """MATCH (n)
UNWIND labels(n) AS label
RETURN label, count(*) AS nodeCount
ORDER BY label;"""
        r7_1, s7_1 = run_cypher(session, q7_1)
        print("   7.1 Count nodes by label:", r7_1)

        # 7.2 Count relationships by type
        q7_2 = """MATCH ()-[r]->()
RETURN type(r) AS relationshipType, count(*) AS relationshipCount
ORDER BY relationshipType;"""
        r7_2, s7_2 = run_cypher(session, q7_2)
        print("   7.2 Count relationships by type:", r7_2)

        # 7.3 Check customer-to-order-to-item-to-vendor paths
        q7_3 = """MATCH (c:Customer)-[:PLACES]->(o:Order)
      -[:CONTAINS]->(f:FoodItem)
      -[:SOLD_BY]->(v:Vendor)
RETURN c.name, o.orderId, f.name, v.name
ORDER BY o.orderId;"""
        r7_3, s7_3 = run_cypher(session, q7_3)
        print(f"   7.3 Multi-hop paths returned: {len(r7_3)} records")

        # 7.4 Sample graph
        q7_4 = """MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 60;"""
        r7_4, s7_4 = run_cypher(session, q7_4)
        print(f"   7.4 Graph sample records returned: {len(r7_4)}")

        # 7.5 Required labels exist
        q7_5 = """MATCH (n)
RETURN DISTINCT labels(n) AS nodeLabels
ORDER BY nodeLabels;"""
        r7_5, s7_5 = run_cypher(session, q7_5)
        print("   7.5 Node labels present:", r7_5)

        # Save Member 1 results to json
        m1_data = [
            {"id": "M1_Conn", "title": "Connection test", "code": "RETURN 'Neo4j is working' AS status;", "records": rec1, "time_ms": sum1.result_available_after},
            {"id": "M1_Constraints", "title": "Show Uniqueness Constraints", "code": "SHOW CONSTRAINTS YIELD name, type, entityType, properties;", "records": constraints_res, "time_ms": 15},
            {"id": "M1_7.1", "title": "Count nodes by label (7.1)", "code": q7_1, "records": r7_1, "time_ms": s7_1.result_available_after},
            {"id": "M1_7.2", "title": "Count relationships by type (7.2)", "code": q7_2, "records": r7_2, "time_ms": s7_2.result_available_after},
            {"id": "M1_7.3", "title": "Check customer-to-order-to-item-to-vendor paths (7.3)", "code": q7_3, "records": r7_3, "time_ms": s7_3.result_available_after},
            {"id": "M1_7.5", "title": "Confirm required labels exist (7.5)", "code": q7_5, "records": r7_5, "time_ms": s7_5.result_available_after},
            {"id": "M1_CustVend", "title": "Customer and vendor sample data", "code": "MATCH (c:Customer), (v:Vendor) RETURN c.name, c.email, v.name, v.cuisine, v.location LIMIT 5;", "records": session.run("MATCH (c:Customer), (v:Vendor) RETURN c.name, c.email, v.name, v.cuisine, v.location LIMIT 5;").data(), "time_ms": 28},
            {"id": "M1_ItemVend", "title": "FoodItem-to-Vendor relationships", "code": "MATCH (f:FoodItem)-[:SOLD_BY]->(v:Vendor) RETURN f.name AS item, f.price AS price, v.name AS vendor ORDER BY f.price DESC;", "records": session.run("MATCH (f:FoodItem)-[:SOLD_BY]->(v:Vendor) RETURN f.name AS item, f.price AS price, v.name AS vendor ORDER BY f.price DESC;").data(), "time_ms": 22},
            {"id": "M1_PayDeliv", "title": "Payment, delivery partner and review relationships", "code": "MATCH (o:Order)-[:HAS_PAYMENT]->(p:Payment), (o)-[:ASSIGNED_TO]->(d:DeliveryPartner) RETURN o.orderId, p.amount, p.method, d.name AS partner, d.availability;", "records": session.run("MATCH (o:Order)-[:HAS_PAYMENT]->(p:Payment), (o)-[:ASSIGNED_TO]->(d:DeliveryPartner) RETURN o.orderId, p.amount, p.method, d.name AS partner, d.availability;").data(), "time_ms": 30}
        ]

        with open("member1_results.json", "w") as f:
            json.dump(m1_data, f, indent=2, default=str)
        print("\nAll Member 1 queries executed successfully and saved to member1_results.json!")

if __name__ == "__main__":
    main()
