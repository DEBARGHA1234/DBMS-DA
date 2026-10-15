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
        # Step 0: Ensure base sample dataset exists so all queries have rich results
        print("Ensuring foundational schema and sample dataset...")
        
        # Additional supporting vendors and items for rich traversal, filtering, and recommendations
        session.run("""
        MERGE (v2:Vendor {vendorId: 202})
        SET v2.name = 'Curry Leaf', v2.cuisine = 'Indian', v2.location = 'Chennai'
        MERGE (v3:Vendor {vendorId: 203})
        SET v3.name = 'Dragon Wok', v3.cuisine = 'Chinese', v3.location = 'Bangalore'
        MERGE (c2:Customer {customerId: 102})
        SET c2.name = 'Priya', c2.email = 'priya@example.com'
        MERGE (f2:FoodItem {itemId: 302})
        SET f2.name = 'Butter Chicken', f2.price = 320, f2.category = 'Main Course'
        MERGE (f3:FoodItem {itemId: 303})
        SET f3.name = 'Masala Dosa', f3.price = 110, f3.category = 'Breakfast'
        MERGE (f4:FoodItem {itemId: 304})
        SET f4.name = 'Schezwan Noodles', f4.price = 240, f4.category = 'Main Course'
        MERGE (f5:FoodItem {itemId: 305})
        SET f5.name = 'Tandoori Platter', f5.price = 450, f5.category = 'Starters'
        MERGE (f2)-[:SOLD_BY]->(v2)
        MERGE (f3)-[:SOLD_BY]->(v2)
        MERGE (f4)-[:SOLD_BY]->(v3)
        MERGE (f5)-[:SOLD_BY]->(v2)
        MERGE (r1:Review {reviewId: 701})
        SET r1.rating = 5, r1.comment = 'Authentic spices and very fast delivery!'
        MERGE (r2:Review {reviewId: 702})
        SET r2.rating = 4, r2.comment = 'Delicious crispy dosas and great sambar.'
        MERGE (c2)-[:WROTE]->(r2)
        MERGE (r2)-[:ABOUT]->(v2)
        """)
        
        queries_to_execute = [
            ("3.1", "Check database connection", 
             "RETURN 'Neo4j connection successful' AS status;"),
            
            ("Query 1", "Create a customer (Aarav)", 
             """MERGE (c:Customer {customerId: 101})
SET c.name = 'Aarav',
    c.email = 'aarav@example.com'
RETURN c;"""),
             
            ("Query 2", "Create a vendor (Spice House)", 
             """MERGE (v:Vendor {vendorId: 201})
SET v.name = 'Spice House',
    v.cuisine = 'Indian',
    v.location = 'Chennai'
RETURN v;"""),
             
            ("Query 3", "Create food item and connect to vendor", 
             """MATCH (v:Vendor {vendorId: 201})
MERGE (f:FoodItem {itemId: 301})
SET f.name = 'Paneer Biryani',
    f.price = 220,
    f.category = 'Main Course'
MERGE (f)-[:SOLD_BY]->(v)
RETURN f, v;"""),
             
            ("Query 4", "Create order and connect to customer", 
             """MATCH (c:Customer {customerId: 101})
MERGE (o:Order {orderId: 401})
SET o.status = 'Placed',
    o.totalAmount = 220,
    o.orderDate = date()
MERGE (c)-[:PLACES]->(o)
RETURN c, o;"""),
             
            ("Query 5", "Connect order to food item", 
             """MATCH (o:Order {orderId: 401}),
      (f:FoodItem {itemId: 301})
MERGE (o)-[r:CONTAINS]->(f)
SET r.quantity = 1
RETURN o, r, f;"""),

            ("Review Link", "Link sample review to Aarav and Spice House",
             """MATCH (c:Customer {customerId: 101}), (v:Vendor {vendorId: 201})
MERGE (r:Review {reviewId: 701})
SET r.rating = 5, r.comment = 'Authentic spices and very fast delivery!'
MERGE (c)-[:WROTE]->(r)
MERGE (r)-[:ABOUT]->(v)
RETURN c, r, v;"""),

            ("3.2", "Check available node labels and records", 
             """MATCH (n)
RETURN labels(n) AS labels, count(*) AS records
ORDER BY records DESC;"""),
             
            ("3.3", "View sample of graph nodes and relationships", 
             """MATCH (n)-[r]->(m)
RETURN type(r) AS relationship, labels(n)[0] AS fromNode, labels(m)[0] AS toNode, count(*) AS count
ORDER BY count DESC;"""),
             
            ("Query 6", "Read all customers", 
             """MATCH (c:Customer)
RETURN c.customerId, c.name, c.email
ORDER BY c.name;"""),
             
            ("Query 7", "Read all vendors", 
             """MATCH (v:Vendor)
RETURN v.vendorId, v.name, v.cuisine, v.location
ORDER BY v.name;"""),
             
            ("Query 8", "List food items under a chosen price (< 300)", 
             """MATCH (f:FoodItem)
WHERE f.price < 300
RETURN f.name, f.price, f.category
ORDER BY f.price ASC;"""),
             
            ("Query 9", "Find orders for a specific customer (101)", 
             """MATCH (c:Customer {customerId: 101})-[:PLACES]->(o:Order)
RETURN c.name, o.orderId, o.status, o.totalAmount
ORDER BY o.orderDate DESC;"""),
             
            ("Query 10", "Update order status", 
             """MATCH (o:Order {orderId: 401})
SET o.status = 'Delivered'
RETURN o.orderId, o.status;"""),
             
            ("Query 11", "Count orders per customer", 
             """MATCH (c:Customer)-[:PLACES]->(o:Order)
RETURN c.name AS customer,
       count(o) AS totalOrders
ORDER BY totalOrders DESC;"""),
             
            ("Query 12", "Find five most expensive food items", 
             """MATCH (f:FoodItem)
RETURN f.name, f.price
ORDER BY f.price DESC
LIMIT 5;"""),
             
            ("Query 13", "Trace customer -> order -> food item -> vendor", 
             """MATCH (c:Customer)-[:PLACES]->(o:Order)
      -[:CONTAINS]->(f:FoodItem)
      -[:SOLD_BY]->(v:Vendor)
RETURN c.name AS customer,
       o.orderId AS orderId,
       f.name AS foodItem,
       v.name AS vendor;"""),
             
            ("Query 14", "Count food items sold by each vendor", 
             """MATCH (f:FoodItem)-[:SOLD_BY]->(v:Vendor)
RETURN v.name AS vendor,
       count(f) AS menuItems
ORDER BY menuItems DESC;"""),
             
            ("Query 15", "Basic vendor recommendations from order history", 
             """MATCH (c:Customer {customerId: 101})
      -[:PLACES]->(:Order)
      -[:CONTAINS]->(:FoodItem)
      -[:SOLD_BY]->(v:Vendor)
RETURN v.name AS vendor,
       v.cuisine AS cuisine,
       count(*) AS matchingOrderPaths
ORDER BY matchingOrderPaths DESC;"""),
             
            ("Query 16", "Find vendors in the same cuisine as vendor 201", 
             """MATCH (base:Vendor {vendorId: 201})
MATCH (other:Vendor)
WHERE other.cuisine = base.cuisine
  AND other.vendorId <> base.vendorId
RETURN other.name, other.cuisine, other.location;"""),
             
            ("Query 19", "Create/link a payment", 
             """MATCH (o:Order {orderId: 401})
MERGE (p:Payment {paymentId: 501})
SET p.amount = 220,
    p.method = 'UPI',
    p.status = 'Paid'
MERGE (o)-[:HAS_PAYMENT]->(p)
RETURN o, p;"""),
             
            ("Query 20", "Create/link a delivery partner", 
             """MATCH (o:Order {orderId: 401})
MERGE (d:DeliveryPartner {partnerId: 601})
SET d.name = 'Rohan',
    d.availability = 'Busy'
MERGE (o)-[:ASSIGNED_TO]->(d)
RETURN o, d;"""),
             
            ("Query 17", "Find orders and their delivery partners", 
             """MATCH (o:Order)-[:ASSIGNED_TO]->(d:DeliveryPartner)
RETURN o.orderId, o.status, d.name AS deliveryPartner;"""),
             
            ("Query 18", "Find customer reviews and reviewed vendors", 
             """MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(v:Vendor)
RETURN c.name AS customer,
       v.name AS vendor,
       r.rating AS rating,
       r.comment AS comment
ORDER BY rating DESC;"""),
             
            ("Query 21", "Find completed/delivered orders", 
             """MATCH (c:Customer)-[:PLACES]->(o:Order)
WHERE o.status = 'Delivered'
RETURN c.name, o.orderId, o.totalAmount, o.status;"""),
        ]

        results_data = []
        for q_id, q_title, q_code in queries_to_execute:
            print(f"Executing [{q_id}]: {q_title}...")
            recs, summary = run_cypher(session, q_code)
            results_data.append({
                "id": q_id,
                "title": q_title,
                "code": q_code,
                "records": recs,
                "time_ms": summary.result_available_after
            })
            print(f"   -> Returned {len(recs)} records in {summary.result_available_after}ms")

        # Save results to json for screenshot generator
        with open("query_results.json", "w") as f:
            json.dump(results_data, f, indent=2, default=str)
        print("\nAll queries executed successfully and saved to query_results.json!")

if __name__ == "__main__":
    main()
