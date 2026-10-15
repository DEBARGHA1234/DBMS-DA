// ==============================================================================
// DBMS DA3: COMPLETE NEO4J IMPLEMENTATION SCRIPT
// Mini-Project: Multi-Vendor Food Delivery System
// Technology: Neo4j Graph Database (AuraDB Enterprise 5.x)
// Execution Order: PART 1 (Member 1 Work) -> PART 2 (Member 2 Work)
// ==============================================================================

// ==============================================================================
// PART 1: MEMBER 1 — SETUP, SCHEMA CONSTRAINTS & SAMPLE DATA
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. Connection Test
// ------------------------------------------------------------------------------
RETURN 'Neo4j is working' AS status;

// ------------------------------------------------------------------------------
// 2. Create Uniqueness Constraints (Section 4)
// ------------------------------------------------------------------------------
CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
FOR (n:Customer) REQUIRE n.customerId IS UNIQUE;

CREATE CONSTRAINT vendor_id_unique IF NOT EXISTS
FOR (n:Vendor) REQUIRE n.vendorId IS UNIQUE;

CREATE CONSTRAINT food_item_id_unique IF NOT EXISTS
FOR (n:FoodItem) REQUIRE n.itemId IS UNIQUE;

CREATE CONSTRAINT order_id_unique IF NOT EXISTS
FOR (n:Order) REQUIRE n.orderId IS UNIQUE;

CREATE CONSTRAINT delivery_partner_id_unique IF NOT EXISTS
FOR (n:DeliveryPartner) REQUIRE n.partnerId IS UNIQUE;

CREATE CONSTRAINT payment_id_unique IF NOT EXISTS
FOR (n:Payment) REQUIRE n.paymentId IS UNIQUE;

CREATE CONSTRAINT review_id_unique IF NOT EXISTS
FOR (n:Review) REQUIRE n.reviewId IS UNIQUE;

// Verify constraints:
SHOW CONSTRAINTS YIELD name, type, entityType, properties;

// ------------------------------------------------------------------------------
// 3. Load Sample Data (Section 5)
// ------------------------------------------------------------------------------

// 5.1 Create customers
UNWIND [
 {id: 101, name: 'Aarav', email: 'aarav@example.com'},
 {id: 102, name: 'Diya', email: 'diya@example.com'},
 {id: 103, name: 'Kabir', email: 'kabir@example.com'},
 {id: 104, name: 'Meera', email: 'meera@example.com'}
] AS row
MERGE (c:Customer {customerId: row.id})
SET c.name = row.name, c.email = row.email;

// 5.2 Create vendors
UNWIND [
 {id: 201, name: 'Spice House', cuisine: 'Indian', location: 'Chennai'},
 {id: 202, name: 'Pasta Point', cuisine: 'Italian', location: 'Chennai'},
 {id: 203, name: 'Green Bowl', cuisine: 'Healthy', location: 'Chennai'},
 {id: 204, name: 'Wok Express', cuisine: 'Chinese', location: 'Chennai'}
] AS row
MERGE (v:Vendor {vendorId: row.id})
SET v.name = row.name, v.cuisine = row.cuisine, v.location = row.location;

// 5.3 Create food items and connect each to its vendor ([:SOLD_BY])
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

// 5.4 Create orders and connect customers ([:PLACES])
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

// 5.5 Connect orders to food items ([:CONTAINS])
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

// ------------------------------------------------------------------------------
// 4. Add Delivery, Payment and Review Data (Section 6)
// ------------------------------------------------------------------------------

// 6.1 Create delivery partners and assign orders ([:ASSIGNED_TO])
UNWIND [
 {id: 601, name: 'Rohan', availability: 'Busy'},
 {id: 602, name: 'Isha', availability: 'Available'},
 {id: 603, name: 'Dev', availability: 'Busy'}
] AS row
MERGE (d:DeliveryPartner {partnerId: row.id})
SET d.name = row.name, d.availability = row.availability;

MATCH (o:Order {orderId: 401}), (d:DeliveryPartner {partnerId: 601}) MERGE (o)-[:ASSIGNED_TO]->(d);
MATCH (o:Order {orderId: 402}), (d:DeliveryPartner {partnerId: 602}) MERGE (o)-[:ASSIGNED_TO]->(d);
MATCH (o:Order {orderId: 403}), (d:DeliveryPartner {partnerId: 603}) MERGE (o)-[:ASSIGNED_TO]->(d);

// 6.2 Create payments and connect them to orders ([:HAS_PAYMENT])
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

// 6.3 Create reviews and connect customers to vendors ([:WROTE] & [:ABOUT])
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

// ------------------------------------------------------------------------------
// 5. Member 1 Database Validation Queries (Section 7)
// ------------------------------------------------------------------------------

// 7.1 Count nodes by label
MATCH (n)
UNWIND labels(n) AS label
RETURN label, count(*) AS nodeCount
ORDER BY label;

// 7.2 Count relationships by type
MATCH ()-[r]->()
RETURN type(r) AS relationshipType, count(*) AS relationshipCount
ORDER BY relationshipType;

// 7.3 Check customer-to-order-to-item-to-vendor paths
MATCH (c:Customer)-[:PLACES]->(o:Order)
      -[:CONTAINS]->(f:FoodItem)
      -[:SOLD_BY]->(v:Vendor)
RETURN c.name, o.orderId, f.name, v.name
ORDER BY o.orderId;

// 7.4 View a graph sample
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 60;

// 7.5 Confirm required labels exist
MATCH (n)
RETURN DISTINCT labels(n) AS nodeLabels
ORDER BY nodeLabels;


// ==============================================================================
// PART 2: MEMBER 2 — QUERY IMPLEMENTATION & DEMONSTRATION
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. Before You Start Verification
// ------------------------------------------------------------------------------

// Query 3.1 Check database connection
RETURN 'Neo4j connection successful' AS status;

// Query 3.2 Check available node labels and records
MATCH (n)
RETURN labels(n) AS labels, count(*) AS records
ORDER BY records DESC;

// Query 3.3 View a sample of the graph
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 50;

// ------------------------------------------------------------------------------
// 2. Core CRUD Queries
// ------------------------------------------------------------------------------

// Query 1 — Create a customer
MERGE (c:Customer {customerId: 101})
SET c.name = 'Aarav',
    c.email = 'aarav@example.com'
RETURN c;

// Query 2 — Create a vendor
MERGE (v:Vendor {vendorId: 201})
SET v.name = 'Spice House',
    v.cuisine = 'Indian',
    v.location = 'Chennai'
RETURN v;

// Query 3 — Create a food item and connect it to a vendor
MATCH (v:Vendor {vendorId: 201})
MERGE (f:FoodItem {itemId: 301})
SET f.name = 'Paneer Biryani',
    f.price = 220,
    f.category = 'Main Course'
MERGE (f)-[:SOLD_BY]->(v)
RETURN f, v;

// Query 4 — Create an order and connect it to a customer
MATCH (c:Customer {customerId: 101})
MERGE (o:Order {orderId: 401})
SET o.status = 'Placed',
    o.totalAmount = 220,
    o.orderDate = date()
MERGE (c)-[:PLACES]->(o)
RETURN c, o;

// Query 5 — Connect the order to a food item
MATCH (o:Order {orderId: 401}),
      (f:FoodItem {itemId: 301})
MERGE (o)-[r:CONTAINS]->(f)
SET r.quantity = 1
RETURN o, r, f;

// Query 6 — Read all customers
MATCH (c:Customer)
RETURN c.customerId, c.name, c.email
ORDER BY c.name;

// Query 7 — Read all vendors
MATCH (v:Vendor)
RETURN v.vendorId, v.name, v.cuisine, v.location
ORDER BY v.name;

// Query 8 — List food items under a chosen price (< 300)
MATCH (f:FoodItem)
WHERE f.price < 300
RETURN f.name, f.price, f.category
ORDER BY f.price ASC;

// Query 9 — Find orders for a specific customer (101)
MATCH (c:Customer {customerId: 101})-[:PLACES]->(o:Order)
RETURN c.name, o.orderId, o.status, o.totalAmount
ORDER BY o.orderDate DESC;

// Query 10 — Update an order status
MATCH (o:Order {orderId: 401})
SET o.status = 'Delivered'
RETURN o.orderId, o.status;

// ------------------------------------------------------------------------------
// 3. Aggregations & Ranking
// ------------------------------------------------------------------------------

// Query 11 — Count orders per customer
MATCH (c:Customer)-[:PLACES]->(o:Order)
RETURN c.name AS customer,
       count(o) AS totalOrders
ORDER BY totalOrders DESC;

// Query 12 — Find the five most expensive food items
MATCH (f:FoodItem)
RETURN f.name, f.price
ORDER BY f.price DESC
LIMIT 5;

// ------------------------------------------------------------------------------
// 4. Graph-Specific Queries (Multi-Hop Traversal & Recommendations)
// ------------------------------------------------------------------------------

// Query 13 — Trace customer -> order -> food item -> vendor (Multi-hop traversal)
MATCH (c:Customer)-[:PLACES]->(o:Order)
      -[:CONTAINS]->(f:FoodItem)
      -[:SOLD_BY]->(v:Vendor)
RETURN c.name AS customer,
       o.orderId AS orderId,
       f.name AS foodItem,
       v.name AS vendor;

// Query 14 — Count food items sold by each vendor
MATCH (f:FoodItem)-[:SOLD_BY]->(v:Vendor)
RETURN v.name AS vendor,
       count(f) AS menuItems
ORDER BY menuItems DESC;

// Query 15 — Basic vendor recommendations from order history
MATCH (c:Customer {customerId: 101})
      -[:PLACES]->(:Order)
      -[:CONTAINS]->(:FoodItem)
      -[:SOLD_BY]->(v:Vendor)
RETURN v.name AS vendor,
       v.cuisine AS cuisine,
       count(*) AS matchingOrderPaths
ORDER BY matchingOrderPaths DESC;

// Query 16 — Find vendors in the same cuisine as a vendor
MATCH (base:Vendor {vendorId: 201})
MATCH (other:Vendor)
WHERE other.cuisine = base.cuisine
  AND other.vendorId <> base.vendorId
RETURN other.name, other.cuisine, other.location;

// Query 17 — Find orders and their delivery partners
MATCH (o:Order)-[:ASSIGNED_TO]->(d:DeliveryPartner)
RETURN o.orderId, o.status, d.name AS deliveryPartner;

// Query 18 — Find customer reviews and reviewed vendors
MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(v:Vendor)
RETURN c.name AS customer,
       v.name AS vendor,
       r.rating AS rating,
       r.comment AS comment
ORDER BY rating DESC;

// ------------------------------------------------------------------------------
// 5. Payment and Delivery Operations
// ------------------------------------------------------------------------------

// Query 19 — Create/link a payment
MATCH (o:Order {orderId: 401})
MERGE (p:Payment {paymentId: 501})
SET p.amount = 220,
    p.method = 'UPI',
    p.status = 'Paid'
MERGE (o)-[:HAS_PAYMENT]->(p)
RETURN o, p;

// Query 20 — Create/link a delivery partner
MATCH (o:Order {orderId: 401})
MERGE (d:DeliveryPartner {partnerId: 601})
SET d.name = 'Rohan',
    d.availability = 'Busy'
MERGE (o)-[:ASSIGNED_TO]->(d)
RETURN o, d;

// Query 21 — Find completed/delivered orders
MATCH (c:Customer)-[:PLACES]->(o:Order)
WHERE o.status = 'Delivered'
RETURN c.name, o.orderId, o.totalAmount, o.status;

// ------------------------------------------------------------------------------
// 6. Deletion Operation Demonstration (Section 7)
// ------------------------------------------------------------------------------
MATCH (o:Order {orderId: 401})
DETACH DELETE o;
