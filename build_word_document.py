import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_FILE = "DBMS_DA3_Member2_Neo4j_Query_Implementation.docx"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    
    doc.add_paragraph() # Spacing

def add_image_figure(doc, img_rel_path, caption_text):
    full_path = os.path.abspath(img_rel_path)
    if os.path.exists(full_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(full_path, width=Inches(6.2))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run(f"Figure: {caption_text}")
        run_cap.font.name = "Segoe UI"
        run_cap.font.size = Pt(9.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    else:
        p_err = doc.add_paragraph(f"[Image missing: {img_rel_path}]")
        p_err.runs[0].font.color.rgb = RGBColor(0xEF, 0x44, 0x44)

def add_callout(doc, title, text, bg_color="F0F9FF", border_color="0284C7"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"✦ {title}\n")
    run_t.font.name = "Segoe UI"
    run_t.font.bold = True
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = RGBColor(0x03, 0x69, 0xA1)
    
    run_b = p.add_run(text)
    run_b.font.name = "Segoe UI"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    
    doc.add_paragraph()

def build_docx():
    print("Building comprehensive Word Document with all screenshots and query implementations...")
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
    # Set default style font
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Segoe UI'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    
    # ==============================================================================
    # COVER / HEADER TITLE
    # ==============================================================================
    p_pre = doc.add_paragraph()
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pre.paragraph_format.space_before = Pt(10)
    p_pre.paragraph_format.space_after = Pt(4)
    r_pre = p_pre.add_run("DBMS DA3 ASSESSMENT IMPLEMENTATION REPORT")
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Member 2: Neo4j Query Implementation Guide")
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run("Mini-Project: Multi-Vendor Food Delivery System\nComprehensive Execution Proof, Graph Visualizations, Cypher Queries & Viva Preparation")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Metadata Table
    tbl_meta = doc.add_table(rows=5, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Selected Technology", "Neo4j Graph Database (AuraDB Cloud Instance: 89738e78)"),
        ("Query Language", "Cypher (Declarative Graph Query Language)"),
        ("Project Scope", "Multi-Vendor Food Delivery System (Customer, Vendor, Item, Order, Partner, Payment, Review)"),
        ("Role Responsibility", "Member 2: Query Implementation, CRUD, Traversal, Recommendations & Visualizations"),
        ("Target Demonstration Date", "20 October 2026 (In-Person DBMS Lab Demonstration)")
    ]
    for row_idx, (k, v) in enumerate(meta_info):
        c0 = tbl_meta.cell(row_idx, 0)
        c1 = tbl_meta.cell(row_idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=80, bottom=80, left=120, right=120)
        set_cell_margins(c1, top=80, bottom=80, left=120, right=120)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # ==============================================================================
    # SECTION 1: EXECUTIVE SUMMARY & ASSUMED GRAPH MODEL
    # ==============================================================================
    h1 = doc.add_heading("1. Executive Summary & Graph Data Model", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    
    doc.add_paragraph(
        "This implementation guide provides complete evidence of the Cypher queries developed and executed for the "
        "Multi-Vendor Food Delivery System on a live Neo4j AuraDB instance. The graph schema models entities and real-time relationships "
        "connecting Customers, Orders, Food Items, Vendors, Delivery Partners, Payments, and Reviews."
    )
    
    # Graph Model Tables
    doc.add_heading("Assumed Node Labels & Property Schema", level=2)
    tbl_nodes = doc.add_table(rows=8, cols=3)
    tbl_nodes.alignment = WD_TABLE_ALIGNMENT.CENTER
    node_rows = [
        ("Node Label", "Key Identifier", "Example Properties"),
        ("Customer", "customerId (Integer)", "name, email"),
        ("Vendor", "vendorId (Integer)", "name, cuisine, location"),
        ("FoodItem", "itemId (Integer)", "name, price, category"),
        ("Order", "orderId (Integer)", "status, totalAmount, orderDate"),
        ("DeliveryPartner", "partnerId (Integer)", "name, availability"),
        ("Payment", "paymentId (Integer)", "amount, method, status"),
        ("Review", "reviewId (Integer)", "rating, comment")
    ]
    for r_idx, (c0_t, c1_t, c2_t) in enumerate(node_rows):
        for col_idx, text in enumerate([c0_t, c1_t, c2_t]):
            c = tbl_nodes.cell(r_idx, col_idx)
            set_cell_margins(c, top=70, bottom=70, left=100, right=100)
            if r_idx == 0:
                set_cell_background(c, "1E293B")
                p = c.paragraphs[0]
                run = p.add_run(text)
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
                p = c.paragraphs[0]
                run = p.add_run(text)
                run.font.size = Pt(9.0)
                if col_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
                    
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    doc.add_heading("Relationship Topology & Directionality", level=2)
    doc.add_paragraph(
        "Relationships represent first-class citizens in Neo4j. The following directed relationships form the graph topology:"
    )
    rels = [
        "(Customer)-[:PLACES]->(Order): Models order placements initiated by a customer.",
        "(Order)-[:CONTAINS {quantity}]->(FoodItem): Links individual ordered food items and quantities.",
        "(FoodItem)-[:SOLD_BY]->(Vendor): Associates food items directly with their preparing vendor restaurant.",
        "(Order)-[:ASSIGNED_TO]->(DeliveryPartner): Tracks driver dispatch and availability status.",
        "(Order)-[:HAS_PAYMENT]->(Payment): Records transactional payment method and settlement state.",
        "(Customer)-[:WROTE]->(Review): Links feedback authored by customers.",
        "(Review)-[:ABOUT]->(Vendor): Maps feedback directly to the reviewed vendor establishment."
    ]
    for r in rels:
        p_r = doc.add_paragraph(r, style='List Bullet')
        p_r.paragraph_format.space_after = Pt(2)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Active Connection Overview Screenshot
    add_image_figure(doc, "screenshots/ss_00_workspace_connection.png", "Live Neo4j AuraDB Active Instance Overview (ID: 89738e78, Status: Running)")

    # ==============================================================================
    # SECTION 2: SETUP & PRE-FLIGHT CHECKS
    # ==============================================================================
    doc.add_heading("2. Before You Start: Setup & Connectivity Checks", level=1)
    doc.add_paragraph(
        "Prior to executing application logic, pre-flight checks confirm secure Bolt connectivity to the Aura cloud database, "
        "inspect registered labels, and verify relationship topologies."
    )
    
    # 2.1 Check database connection
    doc.add_heading("2.1 Check Database Connection (Query 3.1)", level=2)
    doc.add_paragraph("Verifies low-latency round-trip connectivity from Cypher client to Neo4j Aura.")
    add_code_block(doc, "RETURN 'Neo4j connection successful' AS status;")
    add_image_figure(doc, "screenshots/ss_01_connection_check.png", "Query 3.1: Database Connection Verification")
    
    # 2.2 Check available node labels and records
    doc.add_heading("2.2 Inspect Node Labels and Record Counts (Query 3.2)", level=2)
    doc.add_paragraph("Aggregates all labels and record counts across the graph to confirm loaded entities.")
    add_code_block(doc, "MATCH (n)\nRETURN labels(n) AS labels, count(*) AS records\nORDER BY records DESC;")
    add_image_figure(doc, "screenshots/ss_02_node_labels_counts.png", "Query 3.2: Node Labels and Population Distribution")
    
    # 2.3 Sample Graph Visualization
    doc.add_heading("2.3 Complete Graph Ecosystem Visualization (Query 3.3)", level=2)
    doc.add_paragraph(
        "Renders the active graph ecosystem showing Customer, Order, FoodItem, Vendor, Payment, DeliveryPartner, and Review nodes with directed edges."
    )
    add_code_block(doc, "MATCH (n)-[r]->(m)\nRETURN n, r, m\nLIMIT 50;")
    add_image_figure(doc, "screenshots/ss_03_graph_visualization.png", "Query 3.3: Neo4j Graph Visualizer showing multi-entity connectivity")
    
    # ==============================================================================
    # SECTION 3: CRUD & MERGE OPERATIONS
    # ==============================================================================
    doc.add_heading("3. Core CRUD Operations (Create, Read, Update)", level=1)
    doc.add_paragraph(
        "Demonstrates idempotent entity creation via MERGE, establishing relationships, attribute updates, and query filtering."
    )
    
    # Query 1
    doc.add_heading("Query 1 — Create a Customer (Aarav, customerId: 101)", level=2)
    doc.add_paragraph("Uses MERGE with customerId to prevent duplicate customer nodes upon subsequent executions.")
    add_code_block(doc, "MERGE (c:Customer {customerId: 101})\nSET c.name = 'Aarav',\n    c.email = 'aarav@example.com'\nRETURN c;")
    add_image_figure(doc, "screenshots/ss_04_query1_create_customer.png", "Query 1: Idempotent Customer Creation using MERGE")
    
    # Query 2
    doc.add_heading("Query 2 — Create a Vendor (Spice House, vendorId: 201)", level=2)
    doc.add_paragraph("Provisions the vendor establishment with cuisine specialization and geographical location.")
    add_code_block(doc, "MERGE (v:Vendor {vendorId: 201})\nSET v.name = 'Spice House',\n    v.cuisine = 'Indian',\n    v.location = 'Chennai'\nRETURN v;")
    add_image_figure(doc, "screenshots/ss_05_query2_create_vendor.png", "Query 2: Vendor Creation with Attributes")
    
    # Query 3
    doc.add_heading("Query 3 — Create Food Item & Connect to Vendor", level=2)
    doc.add_paragraph("Creates Paneer Biryani and links it via [:SOLD_BY] relationship to Spice House.")
    add_code_block(doc, "MATCH (v:Vendor {vendorId: 201})\nMERGE (f:FoodItem {itemId: 301})\nSET f.name = 'Paneer Biryani',\n    f.price = 220,\n    f.category = 'Main Course'\nMERGE (f)-[:SOLD_BY]->(v)\nRETURN f, v;")
    add_image_figure(doc, "screenshots/ss_06_query3_create_food_item.png", "Query 3: Menu Item Creation and Vendor Association")
    
    # Query 4
    doc.add_heading("Query 4 — Create Order & Connect to Customer", level=2)
    doc.add_paragraph("Creates Order 401 with placed status and connects it to Customer Aarav via [:PLACES].")
    add_code_block(doc, "MATCH (c:Customer {customerId: 101})\nMERGE (o:Order {orderId: 401})\nSET o.status = 'Placed',\n    o.totalAmount = 220,\n    o.orderDate = date()\nMERGE (c)-[:PLACES]->(o)\nRETURN c, o;")
    add_image_figure(doc, "screenshots/ss_07_query4_create_order.png", "Query 4: Order Creation Linked to Customer")
    
    # Query 5
    doc.add_heading("Query 5 — Connect Order to Food Item ([CONTAINS])", level=2)
    doc.add_paragraph("Establishes the [:CONTAINS] edge between Order 401 and FoodItem 301 with property quantity: 1.")
    add_code_block(doc, "MATCH (o:Order {orderId: 401}),\n      (f:FoodItem {itemId: 301})\nMERGE (o)-[r:CONTAINS]->(f)\nSET r.quantity = 1\nRETURN o, r, f;")
    add_image_figure(doc, "screenshots/ss_08_query5_connect_order_food.png", "Query 5: Order-to-Item Relationship with Edge Properties")
    
    # Query 6
    doc.add_heading("Query 6 — Read All Customers", level=2)
    doc.add_paragraph("Retrieves customer records alphabetically sorted by name.")
    add_code_block(doc, "MATCH (c:Customer)\nRETURN c.customerId, c.name, c.email\nORDER BY c.name;")
    add_image_figure(doc, "screenshots/ss_09_query6_read_customers.png", "Query 6: Reading All Customer Entities")
    
    # Query 7
    doc.add_heading("Query 7 — Read All Vendors", level=2)
    doc.add_paragraph("Fetches all registered restaurant partners with cuisine and location details.")
    add_code_block(doc, "MATCH (v:Vendor)\nRETURN v.vendorId, v.name, v.cuisine, v.location\nORDER BY v.name;")
    add_image_figure(doc, "screenshots/ss_10_query7_read_vendors.png", "Query 7: Reading All Vendor Profiles")
    
    # Query 8
    doc.add_heading("Query 8 — Filter Food Items Under Chosen Price (< 300)", level=2)
    doc.add_paragraph("Demonstrates numeric filtering using WHERE f.price < 300 sorted in ascending order.")
    add_code_block(doc, "MATCH (f:FoodItem)\nWHERE f.price < 300\nRETURN f.name, f.price, f.category\nORDER BY f.price ASC;")
    add_image_figure(doc, "screenshots/ss_11_query8_filter_food_price.png", "Query 8: Filter Menu Items by Budget (< 300)")
    
    # Query 9
    doc.add_heading("Query 9 — Find Orders for Specific Customer (Aarav, 101)", level=2)
    doc.add_paragraph("Traverses (Customer {customerId: 101})-[:PLACES]->(Order) to list order history.")
    add_code_block(doc, "MATCH (c:Customer {customerId: 101})-[:PLACES]->(o:Order)\nRETURN c.name, o.orderId, o.status, o.totalAmount\nORDER BY o.orderDate DESC;")
    add_image_figure(doc, "screenshots/ss_12_query9_orders_for_customer.png", "Query 9: Customer-Specific Order History Traversal")
    
    # Query 10
    doc.add_heading("Query 10 — Update Order Status (SET status = 'Delivered')", level=2)
    doc.add_paragraph("Demonstrates state mutation by updating Order 401 status from 'Placed' to 'Delivered'.")
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nSET o.status = 'Delivered'\nRETURN o.orderId, o.status;")
    add_image_figure(doc, "screenshots/ss_13_query10_update_order_status.png", "Query 10: Mutating Order Lifecycle State")

    # ==============================================================================
    # SECTION 4: AGGREGATION & SORTING QUERIES
    # ==============================================================================
    doc.add_heading("4. Aggregation, Counting & Ranking Queries", level=1)
    doc.add_paragraph(
        "Graph aggregations compute metrics without requiring costly foreign-key JOIN cascades."
    )
    
    # Query 11
    doc.add_heading("Query 11 — Count Orders Per Customer", level=2)
    doc.add_paragraph("Computes total order volume per customer using Cypher's count(o) aggregation.")
    add_code_block(doc, "MATCH (c:Customer)-[:PLACES]->(o:Order)\nRETURN c.name AS customer,\n       count(o) AS totalOrders\nORDER BY totalOrders DESC;")
    add_image_figure(doc, "screenshots/ss_14_query11_count_orders_per_customer.png", "Query 11: Order Volume Aggregation per Customer")
    
    # Query 12
    doc.add_heading("Query 12 — Find the Five Most Expensive Food Items", level=2)
    doc.add_paragraph("Applies ORDER BY price DESC LIMIT 5 to rank premium menu items across vendors.")
    add_code_block(doc, "MATCH (f:FoodItem)\nRETURN f.name, f.price\nORDER BY f.price DESC\nLIMIT 5;")
    add_image_figure(doc, "screenshots/ss_15_query12_top5_expensive_food.png", "Query 12: Top 5 Highest Priced Menu Offerings")

    # ==============================================================================
    # SECTION 5: GRAPH-SPECIFIC QUERIES (MULTI-HOP TRAVERSALS & RECOMMENDATIONS)
    # ==============================================================================
    doc.add_heading("5. Graph-Specific Queries (Multi-Hop Traversal & Recommendations)", level=1)
    doc.add_paragraph(
        "Demonstrates graph database superiority where index-free adjacency enables zero-cost multi-hop traversals "
        "and contextual recommendation engines."
    )
    
    # Query 13
    doc.add_heading("Query 13 — Multi-Hop Traversal: Customer → Order → Item → Vendor", level=2)
    doc.add_paragraph(
        "Traverses 3 relationship hops in a single continuous path: (Customer)-[:PLACES]->(Order)-[:CONTAINS]->(FoodItem)-[:SOLD_BY]->(Vendor)."
    )
    add_code_block(doc, "MATCH (c:Customer)-[:PLACES]->(o:Order)\n      -[:CONTAINS]->(f:FoodItem)\n      -[:SOLD_BY]->(v:Vendor)\nRETURN c.name AS customer,\n       o.orderId AS orderId,\n       f.name AS foodItem,\n       v.name AS vendor;")
    add_image_figure(doc, "screenshots/ss_16_query13_trace_customer_to_vendor.png", "Query 13: 3-Hop Graph Traversal Across Core Entities")
    
    add_callout(
        doc,
        "Why Graphs Excel at Multi-Hop Traversal (Relational vs Neo4j)",
        "In a relational RDBMS, this query requires joining 4 distinct tables (customers, orders, order_items, vendors) "
        "with three expensive B-tree index lookups. In Neo4j, each node stores direct pointers to its adjacent relationships "
        "(index-free adjacency), executing in constant O(1) time per pointer dereference regardless of graph size!"
    )
    
    # Query 14
    doc.add_heading("Query 14 — Count Menu Items Sold by Each Vendor", level=2)
    doc.add_paragraph("Aggregates catalog size per restaurant partner by traversing reverse incoming [:SOLD_BY] edges.")
    add_code_block(doc, "MATCH (f:FoodItem)-[:SOLD_BY]->(v:Vendor)\nRETURN v.name AS vendor,\n       count(f) AS menuItems\nORDER BY menuItems DESC;")
    add_image_figure(doc, "screenshots/ss_17_query14_food_items_per_vendor.png", "Query 14: Menu Item Inventory Count per Vendor")
    
    # Query 15
    doc.add_heading("Query 15 — Basic Vendor Recommendations from Order History", level=2)
    doc.add_paragraph(
        "Recommends vendors and cuisines based on past ordering affinity paths for a given customer."
    )
    add_code_block(doc, "MATCH (c:Customer {customerId: 101})\n      -[:PLACES]->(:Order)\n      -[:CONTAINS]->(:FoodItem)\n      -[:SOLD_BY]->(v:Vendor)\nRETURN v.name AS vendor,\n       v.cuisine AS cuisine,\n       count(*) AS matchingOrderPaths\nORDER BY matchingOrderPaths DESC;")
    add_image_figure(doc, "screenshots/ss_18_query15_vendor_recommendations.png", "Query 15: History-Driven Vendor Recommendation Engine")
    
    # Query 16
    doc.add_heading("Query 16 — Find Similar Vendors by Shared Cuisine", level=2)
    doc.add_paragraph("Discovers alternative vendors offering the same cuisine type while excluding the base vendor.")
    add_code_block(doc, "MATCH (base:Vendor {vendorId: 201})\nMATCH (other:Vendor)\nWHERE other.cuisine = base.cuisine\n  AND other.vendorId <> base.vendorId\nRETURN other.name, other.cuisine, other.location;")
    add_image_figure(doc, "screenshots/ss_19_query16_same_cuisine_vendors.png", "Query 16: Content-Based Cuisine Similarity Match")
    
    # Query 17
    doc.add_heading("Query 17 — Find Orders and Assigned Delivery Partners", level=2)
    doc.add_paragraph("Inspects driver assignments across orders to monitor fulfillment capacity.")
    add_code_block(doc, "MATCH (o:Order)-[:ASSIGNED_TO]->(d:DeliveryPartner)\nRETURN o.orderId, o.status, d.name AS deliveryPartner;")
    add_image_figure(doc, "screenshots/ss_22_query17_orders_delivery_partners.png", "Query 17: Dispatch Traversal to Delivery Partners")
    
    # Query 18
    doc.add_heading("Query 18 — Find Customer Reviews and Reviewed Vendors", level=2)
    doc.add_paragraph("Traverses (Customer)-[:WROTE]->(Review)-[:ABOUT]->(Vendor) to extract qualitative sentiment.")
    add_code_block(doc, "MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(v:Vendor)\nRETURN c.name AS customer,\n       v.name AS vendor,\n       r.rating AS rating,\n       r.comment AS comment\nORDER BY rating DESC;")
    add_image_figure(doc, "screenshots/ss_23_query18_customer_reviews.png", "Query 18: Feedback and Rating Graph Traversal")

    # ==============================================================================
    # SECTION 6: PAYMENT & DELIVERY OPERATIONS
    # ==============================================================================
    doc.add_heading("6. Payment Settlement & Fulfillment Operations", level=1)
    doc.add_paragraph(
        "Models the financial transaction and logistics partner assignment as integrated nodes in the delivery graph."
    )
    
    # Query 19
    doc.add_heading("Query 19 — Create and Link Payment Node", level=2)
    doc.add_paragraph("Creates Payment 501 (UPI, Rs 220, Paid) and binds it to Order 401 via [:HAS_PAYMENT].")
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nMERGE (p:Payment {paymentId: 501})\nSET p.amount = 220,\n    p.method = 'UPI',\n    p.status = 'Paid'\nMERGE (o)-[:HAS_PAYMENT]->(p)\nRETURN o, p;")
    add_image_figure(doc, "screenshots/ss_20_query19_link_payment.png", "Query 19: Financial Transaction Graph Integration")
    
    # Query 20
    doc.add_heading("Query 20 — Create and Link Delivery Partner Node", level=2)
    doc.add_paragraph("Assigns DeliveryPartner 601 (Rohan, status: Busy) to Order 401 via [:ASSIGNED_TO].")
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nMERGE (d:DeliveryPartner {partnerId: 601})\nSET d.name = 'Rohan',\n    d.availability = 'Busy'\nMERGE (o)-[:ASSIGNED_TO]->(d)\nRETURN o, d;")
    add_image_figure(doc, "screenshots/ss_21_query20_link_delivery_partner.png", "Query 20: Courier Driver Assignment")
    
    # Query 21
    doc.add_heading("Query 21 — Find Completed and Delivered Orders", level=2)
    doc.add_paragraph("Filters orders that have reached terminal fulfillment state 'Delivered'.")
    add_code_block(doc, "MATCH (c:Customer)-[:PLACES]->(o:Order)\nWHERE o.status = 'Delivered'\nRETURN c.name, o.orderId, o.totalAmount, o.status;")
    add_image_figure(doc, "screenshots/ss_24_query21_completed_orders.png", "Query 21: Successfully Delivered Orders Audit")

    # ==============================================================================
    # SECTION 7: DELETION OPERATION (RUN LAST)
    # ==============================================================================
    doc.add_heading("7. Deletion Operation Demonstration (Section 7)", level=1)
    doc.add_paragraph(
        "Demonstrates safe node removal using DETACH DELETE. A basic DELETE query fails in Neo4j if a node retains "
        "incident relationships. DETACH DELETE atomically severs all connected edges before destroying the node."
    )
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nDETACH DELETE o;")
    add_image_figure(doc, "screenshots/ss_25_section7_detach_delete.png", "Section 7: DETACH DELETE Execution and Edge Pruning")
    
    add_callout(
        doc,
        "Critical Integrity Behavior: DELETE vs DETACH DELETE",
        "In Neo4j, executing 'DELETE o' on an order with attached [:PLACES], [:CONTAINS], or [:ASSIGNED_TO] relationships "
        "triggers an integrity error: 'Cannot delete node because it still has relationships'. "
        "'DETACH DELETE' first deletes all incoming and outgoing relationships of the target node, then safely purges the node itself. "
        "Importantly, related nodes (Customer, FoodItem, Vendor, Payment, DeliveryPartner) remain intact!",
        bg_color="FEF2F2",
        border_color="EF4444"
    )

    # ==============================================================================
    # SECTION 8: SCREENSHOT CHECKLIST MATRIX
    # ==============================================================================
    doc.add_heading("8. Member 2 Screenshot Verification Checklist", level=1)
    doc.add_paragraph(
        "All required demonstration items from Section 9 of the project guide have been completed, verified, and cataloged below:"
    )
    
    tbl_chk = doc.add_table(rows=12, cols=3)
    tbl_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    chk_rows = [
        ("Required Evidence Item", "Query Reference", "Verification Status"),
        ("Connected Neo4j Browser/Workspace (hide credentials)", "Workspace Overview", "[VERIFIED] Captured (Figure 1 & Fig 2)"),
        ("Node labels and record counts", "Query 3.2", "[VERIFIED] Captured (Figure 3)"),
        ("Graph visualization (Customer, Order, Item, Vendor connected)", "Query 3.3", "[VERIFIED] Captured (Figure 4)"),
        ("Successful create/merge query and its result", "Queries 1–5", "[VERIFIED] Captured (Figures 5–9)"),
        ("Read/filter/sort query results", "Queries 6–9", "[VERIFIED] Captured (Figures 10–13)"),
        ("Update query showing the new order status", "Query 10", "[VERIFIED] Captured (Figure 14)"),
        ("Aggregation result: orders per customer / items per vendor", "Queries 11 & 14", "[VERIFIED] Captured (Figures 15 & 18)"),
        ("Multi-hop traversal query (customer -> order -> item -> vendor)", "Query 13", "[VERIFIED] Captured (Figure 17)"),
        ("Recommendation query and result", "Query 15 & 16", "[VERIFIED] Captured (Figures 19 & 20)"),
        ("Payment/delivery relationship query result", "Queries 17, 19, 20", "[VERIFIED] Captured (Figures 21–23)"),
        ("Deletion query after all other evidence captured", "Section 7", "[VERIFIED] Captured (Figure 25)")
    ]
    for r_idx, (c0_t, c1_t, c2_t) in enumerate(chk_rows):
        for col_idx, text in enumerate([c0_t, c1_t, c2_t]):
            c = tbl_chk.cell(r_idx, col_idx)
            set_cell_margins(c, top=65, bottom=65, left=90, right=90)
            if r_idx == 0:
                set_cell_background(c, "1E293B")
                p = c.paragraphs[0]
                run = p.add_run(text)
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
                p = c.paragraphs[0]
                run = p.add_run(text)
                run.font.size = Pt(9.0)
                if col_idx == 2:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0x16, 0xA3, 0x4A)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # ==============================================================================
    # SECTION 9: VIVA VOCE QUESTIONS & COMPREHENSIVE ANSWERS
    # ==============================================================================
    doc.add_heading("9. Viva Preparation: Questions & Comprehensive Answers", level=1)
    doc.add_paragraph(
        "Below are the essential viva voce questions and technical responses for the Member 2 in-person lab evaluation:"
    )
    
    viva_qa = [
        ("Q1. What is Neo4j?",
         "Neo4j is an ACID-compliant, open-source property graph database management system. It stores data natively as nodes (entities), directed relationships (edges), and key-value properties attached to both nodes and edges."),
        
        ("Q2. What is Cypher?",
         "Cypher is Neo4j's declarative graph query language. It uses ASCII-art syntax (such as (c:Customer)-[:PLACES]->(o:Order)) to visually describe graph pattern matching, data extraction, and modifications without requiring explicit traversal algorithms."),
         
        ("Q3. What is a node?",
         "A node is a fundamental graph discrete entity representing a business domain object (such as a Customer, Vendor, Order, or FoodItem). Nodes can have one or more labels and arbitrary key-value properties."),
         
        ("Q4. What is a relationship?",
         "A relationship is a typed, directed connection linking exactly two nodes (e.g., [:PLACES] from Customer to Order). In Neo4j, relationships are first-class data elements that can also store properties (such as quantity or timestamp)."),
         
        ("Q5. What is the difference between CREATE and MERGE?",
         "CREATE unconditionally instantiates a new node or relationship every time it runs, potentially producing duplicates. MERGE performs an idempotent match-or-create operation: it matches an existing pattern if present, or creates the pattern if absent."),
         
        ("Q6. What does MATCH do in Cypher?",
         "MATCH specifies the graph pattern that Neo4j should locate within the database. It is analogous to the SELECT and FROM/JOIN clauses in SQL, identifying subgraphs that satisfy the specified structure."),
         
        ("Q7. What does SET do in Cypher?",
         "SET is used to mutate existing nodes or relationships by adding or modifying properties (e.g., SET o.status = 'Delivered') or assigning labels."),
         
        ("Q8. What is DETACH DELETE and when is it required?",
         "In Neo4j, a node with connected relationships cannot be deleted using standard DELETE due to referential integrity constraints. DETACH DELETE atomically deletes all incident relationships attached to the node before deleting the node itself."),
         
        ("Q9. Why use Neo4j for this Multi-Vendor Food Delivery Project?",
         "Food delivery involves densely interconnected multi-entity relationships: Customers place Orders, Orders contain Items, Items belong to Vendors, Orders assign Drivers and Payments. In SQL, querying across these entities requires 4-5 table joins with multiplicative join complexity. Neo4j uses index-free adjacency to traverse connections in constant O(1) time per step, enabling real-time recommendation engines and sub-second multi-hop lookups."),
         
        ("Q10. What is graph traversal?",
         "Graph traversal is the process of visiting connected nodes by following relationships along specific path patterns (e.g., tracing customer -> order -> food item -> vendor).")
    ]
    
    for q, a in viva_qa:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.font.bold = True
        r_q.font.size = Pt(10.5)
        r_q.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
        
        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(8)
        r_a = p_a.add_run(f"Ans: {a}")
        r_a.font.size = Pt(10.0)
        r_a.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # ==============================================================================
    # SECTION 10: MEMBER 2 SUBMISSION ARTIFACTS
    # ==============================================================================
    doc.add_heading("10. Member 2 Submission Deliverables Summary", level=1)
    doc.add_paragraph(
        "As outlined in Section 12 of the assessment guide, the following assets have been prepared and tested for final submission and handover:"
    )
    
    delivs = [
        ("1. Tested Cypher Script (queries.cypher)", "Contains all verified, production-ready Cypher queries organized by section."),
        ("2. Visual Evidence Repository (screenshots/)", "Contains 26 high-resolution captured screenshots proving execution across every required operation."),
        ("3. Implementation Report (.docx)", "This comprehensive document compiling problem statement, schema, queries, visual evidence, checklist, and viva solutions."),
        ("4. Handover to Member 3", "Structured data outputs and screenshots ready for direct inclusion into the overall project report and presentation deck.")
    ]
    for title, desc in delivs:
        p_d = doc.add_paragraph(style='List Bullet')
        p_d.paragraph_format.space_after = Pt(3)
        r_dt = p_d.add_run(f"{title}: ")
        r_dt.font.bold = True
        r_dt.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        r_dd = p_d.add_run(desc)
        r_dd.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        
    doc.save(DOCX_FILE)
    print(f"\n[OK] Document successfully generated and saved to: {DOCX_FILE}")
    print(f"File size: {os.path.getsize(DOCX_FILE)} bytes")

if __name__ == "__main__":
    build_docx()
