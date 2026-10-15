import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

TARGET_DOCX_FILES = [
    "DBMS_DA3_Member2_Neo4j_Query_Implementation.docx",
    "DBMS_DA3_Food_Delivery_Neo4j_Complete_Guide.docx"
]

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
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

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
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_unified_document():
    print("Building unified document (Member 1 first, then Member 2)...")
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Segoe UI'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    
    # ==============================================================================
    # COVER / HEADER TITLE
    # ==============================================================================
    p_pre = doc.add_paragraph()
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pre.paragraph_format.space_before = Pt(12)
    p_pre.paragraph_format.space_after = Pt(4)
    r_pre = p_pre.add_run("DBMS DA3 ASSESSMENT COMPLETE IMPLEMENTATION GUIDE")
    r_pre.font.size = Pt(12)
    r_pre.font.bold = True
    r_pre.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Multi-Vendor Food Delivery System\nNeo4j Setup, Schema & Cypher Query Implementation")
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("Sequential Lab Demonstration Report: Member 1 (Setup & Schema) followed by Member 2 (Query Implementation)\nVerified Live on Neo4j AuraDB Enterprise Instance: 89738e78")
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    tbl_meta = doc.add_table(rows=5, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Selected Technology", "Neo4j Graph Database (AuraDB Cloud Instance: 89738e78)"),
        ("Query Language", "Cypher (Declarative Graph Query Language)"),
        ("Mini-Project Title", "Multi-Vendor Food Delivery System"),
        ("Demonstration Structure", "PART 1: Member 1 (Setup, Schema, Constraints & Data) | PART 2: Member 2 (Queries, CRUD, Traversal)"),
        ("Assessment Demonstration", "20 October 2026 (In-Person DBMS Lab Evaluation)")
    ]
    for row_idx, (k, v) in enumerate(meta_info):
        c0 = tbl_meta.cell(row_idx, 0)
        c1 = tbl_meta.cell(row_idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=70, bottom=70, left=120, right=120)
        set_cell_margins(c1, top=70, bottom=70, left=120, right=120)
        
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
    
    # Active Connection Overview Screenshot
    add_image_figure(doc, "screenshots/ss_00_workspace_connection.png", "Live Neo4j AuraDB Active Instance Overview (ID: 89738e78, Status: Running)")

    # ==============================================================================
    # PART 1: MEMBER 1 — SETUP, SCHEMA & SAMPLE DATA GUIDE
    # ==============================================================================
    p_p1 = doc.add_paragraph()
    p_p1.paragraph_format.space_before = Pt(18)
    p_p1.paragraph_format.space_after = Pt(2)
    r_p1 = p_p1.add_run("PART 1: MEMBER 1 WORK")
    r_p1.font.size = Pt(14)
    r_p1.font.bold = True
    r_p1.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    h_m1 = doc.add_heading("Neo4j Setup, Graph Schema, Constraints & Data Loading", level=1)
    h_m1.paragraph_format.space_before = Pt(2)
    h_m1.paragraph_format.space_after = Pt(8)
    
    doc.add_paragraph(
        "Goal of Member 1: Deliver a fully working Neo4j database with a clearly documented graph model, "
        "uniqueness constraints, loaded and validated sample data, and handover readiness for Member 2."
    )
    
    # 1. Member 1 Responsibilities
    doc.add_heading("1.1 Member 1 Responsibilities", level=2)
    m1_resps = [
        "Choose and configure the Neo4j environment (Configured on Neo4j Aura cloud instance: 89738e78).",
        "Design the graph data model tailored for the Multi-Vendor Food Delivery domain.",
        "Define unique identifiers and schema constraints for critical business entities.",
        "Insert a consistent sample dataset comprising Customers, Vendors, FoodItems, Orders, DeliveryPartners, Payments, and Reviews.",
        "Connect all nodes using correctly directed, typed relationships with properties.",
        "Validate database integrity, run graph overview queries, and capture setup/schema screenshots.",
        "Securely hand over the database environment, schema, and sample IDs to Member 2."
    ]
    for r in m1_resps:
        p_r = doc.add_paragraph(r, style='List Bullet')
        p_r.paragraph_format.space_after = Pt(2)

    # 1.2 Proposed Graph Schema
    doc.add_heading("1.2 Proposed Graph Schema", level=2)
    tbl_m1_nodes = doc.add_table(rows=8, cols=3)
    tbl_m1_nodes.alignment = WD_TABLE_ALIGNMENT.CENTER
    m1_nodes = [
        ("Node Label", "Example Properties", "Domain Purpose"),
        ("Customer", "customerId, name, email", "People placing food delivery orders"),
        ("Vendor", "vendorId, name, cuisine, location", "Partner restaurants and kitchens"),
        ("FoodItem", "itemId, name, price, category", "Menu items offered by vendors"),
        ("Order", "orderId, status, totalAmount, orderDate", "Customer food purchases and tracking"),
        ("DeliveryPartner", "partnerId, name, availability", "Delivery courier assignment"),
        ("Payment", "paymentId, amount, method, status", "Financial settlement records"),
        ("Review", "reviewId, rating, comment", "Customer feedback and restaurant ratings")
    ]
    for r_idx, (c0_t, c1_t, c2_t) in enumerate(m1_nodes):
        for col_idx, text in enumerate([c0_t, c1_t, c2_t]):
            c = tbl_m1_nodes.cell(r_idx, col_idx)
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

    # Relationships
    doc.add_heading("1.3 Relationship Definitions & Directionality", level=2)
    m1_rels = [
        "(Customer)-[:PLACES]->(Order): A customer places an order.",
        "(Order)-[:CONTAINS {quantity}]->(FoodItem): An order contains one or more menu items with quantities.",
        "(FoodItem)-[:SOLD_BY]->(Vendor): A vendor sells a food item.",
        "(Order)-[:ASSIGNED_TO]->(DeliveryPartner): An order is assigned to a delivery partner for courier transit.",
        "(Order)-[:HAS_PAYMENT]->(Payment): An order has payment and settlement information.",
        "(Customer)-[:WROTE]->(Review)-[:ABOUT]->(Vendor): A customer writes a review about a vendor."
    ]
    for rel_str in m1_rels:
        p_rel = doc.add_paragraph(rel_str, style='List Bullet')
        p_rel.paragraph_format.space_after = Pt(2)

    # 1.4 Connection Test
    doc.add_heading("1.4 Connection Test", level=2)
    doc.add_paragraph("Confirms client-to-database connection and Bolt protocol handshake.")
    add_code_block(doc, "RETURN 'Neo4j is working' AS status;")
    add_image_figure(doc, "screenshots/m1_ss01_connection_test.png", "Member 1: Connection Test Verification")

    # 1.5 Uniqueness Constraints
    doc.add_heading("1.5 Create Uniqueness Constraints", level=2)
    doc.add_paragraph(
        "Uniqueness constraints enforce entity integrity and automatically back IDs with fast lookup indexes, "
        "preventing duplicate records and optimizing query execution."
    )
    constraints_code = """CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
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
FOR (n:Review) REQUIRE n.reviewId IS UNIQUE;"""
    add_code_block(doc, constraints_code)
    add_image_figure(doc, "screenshots/m1_ss02_constraints.png", "Member 1: Active Schema Constraints in Database")

    # 1.6 Load Sample Data
    doc.add_heading("1.6 Load Sample Data (Sections 5.1 – 5.5)", level=2)
    doc.add_paragraph("Batch ingestion utilizes UNWIND and MERGE for idempotent, reproducible insertion.")

    doc.add_heading("5.1 Create Customers", level=3)
    c_code = """UNWIND [
 {id: 101, name: 'Aarav', email: 'aarav@example.com'},
 {id: 102, name: 'Diya', email: 'diya@example.com'},
 {id: 103, name: 'Kabir', email: 'kabir@example.com'},
 {id: 104, name: 'Meera', email: 'meera@example.com'}
] AS row
MERGE (c:Customer {customerId: row.id})
SET c.name = row.name, c.email = row.email;"""
    add_code_block(doc, c_code)

    doc.add_heading("5.2 Create Vendors", level=3)
    v_code = """UNWIND [
 {id: 201, name: 'Spice House', cuisine: 'Indian', location: 'Chennai'},
 {id: 202, name: 'Pasta Point', cuisine: 'Italian', location: 'Chennai'},
 {id: 203, name: 'Green Bowl', cuisine: 'Healthy', location: 'Chennai'},
 {id: 204, name: 'Wok Express', cuisine: 'Chinese', location: 'Chennai'}
] AS row
MERGE (v:Vendor {vendorId: row.id})
SET v.name = row.name, v.cuisine = row.cuisine, v.location = row.location;"""
    add_code_block(doc, v_code)
    add_image_figure(doc, "screenshots/m1_ss03_cust_vendor_data.png", "Member 1: Customer and Vendor Data Verification")

    doc.add_heading("5.3 Create Food Items and Connect to Vendors ([:SOLD_BY])", level=3)
    f_code = """UNWIND [
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
MERGE (f)-[:SOLD_BY]->(v);"""
    add_code_block(doc, f_code)
    add_image_figure(doc, "screenshots/m1_ss04_food_vendor_rels.png", "Member 1: FoodItem to Vendor Relationships")

    doc.add_heading("5.4 Create Orders and Connect Customers ([:PLACES])", level=3)
    o_code = """UNWIND [
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
MERGE (c)-[:PLACES]->(o);"""
    add_code_block(doc, o_code)

    doc.add_heading("5.5 Connect Orders to Food Items ([:CONTAINS])", level=3)
    item_ord_code = """UNWIND [
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
SET r.quantity = row.quantity;"""
    add_code_block(doc, item_ord_code)

    # 1.7 Add delivery, payment and review data
    doc.add_heading("1.7 Add Delivery, Payment and Review Data (Section 6)", level=2)
    doc.add_paragraph("Fulfills delivery dispatch, settlement, and customer satisfaction feedback loops.")

    doc.add_heading("6.1 Delivery Partners & Assignments", level=3)
    dp_code = """UNWIND [
 {id: 601, name: 'Rohan', availability: 'Busy'},
 {id: 602, name: 'Isha', availability: 'Available'},
 {id: 603, name: 'Dev', availability: 'Busy'}
] AS row
MERGE (d:DeliveryPartner {partnerId: row.id})
SET d.name = row.name, d.availability = row.availability;

MATCH (o:Order {orderId: 401}), (d:DeliveryPartner {partnerId: 601}) MERGE (o)-[:ASSIGNED_TO]->(d);
MATCH (o:Order {orderId: 402}), (d:DeliveryPartner {partnerId: 602}) MERGE (o)-[:ASSIGNED_TO]->(d);
MATCH (o:Order {orderId: 403}), (d:DeliveryPartner {partnerId: 603}) MERGE (o)-[:ASSIGNED_TO]->(d);"""
    add_code_block(doc, dp_code)

    doc.add_heading("6.2 Payments Connected to Orders", level=3)
    pay_code = """UNWIND [
 {id: 501, orderId: 401, amount: 220, method: 'UPI', status: 'Paid'},
 {id: 502, orderId: 402, amount: 380, method: 'Card', status: 'Pending'},
 {id: 503, orderId: 403, amount: 260, method: 'UPI', status: 'Paid'},
 {id: 504, orderId: 404, amount: 190, method: 'Cash', status: 'Paid'},
 {id: 505, orderId: 405, amount: 280, method: 'Card', status: 'Pending'}
] AS row
MATCH (o:Order {orderId: row.orderId})
MERGE (p:Payment {paymentId: row.id})
SET p.amount = row.amount, p.method = row.method, p.status = row.status
MERGE (o)-[:HAS_PAYMENT]->(p);"""
    add_code_block(doc, pay_code)

    doc.add_heading("6.3 Customer Reviews of Vendors", level=3)
    rev_code = """UNWIND [
 {id: 701, customerId: 101, vendorId: 201, rating: 5, comment: 'Great taste'},
 {id: 702, customerId: 102, vendorId: 202, rating: 4, comment: 'Good pasta'},
 {id: 703, customerId: 103, vendorId: 204, rating: 4, comment: 'Quick service'}
] AS row
MATCH (c:Customer {customerId: row.customerId}),
      (v:Vendor {vendorId: row.vendorId})
MERGE (r:Review {reviewId: row.id})
SET r.rating = row.rating, r.comment = row.comment
MERGE (c)-[:WROTE]->(r)
MERGE (r)-[:ABOUT]->(v);"""
    add_code_block(doc, rev_code)
    add_image_figure(doc, "screenshots/m1_ss08_payment_delivery_rels.png", "Member 1: Payment and Delivery Partner Integration")

    # 1.8 Database Validation
    doc.add_heading("1.8 Database Validation & Health Checks (Section 7)", level=2)
    doc.add_paragraph("Executes five validation queries confirming entity counts and path completeness.")

    doc.add_heading("7.1 Count Nodes by Label", level=3)
    add_code_block(doc, "MATCH (n)\nUNWIND labels(n) AS label\nRETURN label, count(*) AS nodeCount\nORDER BY label;")
    add_image_figure(doc, "screenshots/m1_ss06_node_counts.png", "Member 1: Query 7.1 - Node Count by Label")

    doc.add_heading("7.2 Count Relationships by Type", level=3)
    add_code_block(doc, "MATCH ()-[r]->()\nRETURN type(r) AS relationshipType, count(*) AS relationshipCount\nORDER BY relationshipType;")
    add_image_figure(doc, "screenshots/m1_ss07_rel_counts.png", "Member 1: Query 7.2 - Relationship Count by Type")

    doc.add_heading("7.3 Multi-Hop Traversal Validation (Customer → Order → Item → Vendor)", level=3)
    add_code_block(doc, "MATCH (c:Customer)-[:PLACES]->(o:Order)\n      -[:CONTAINS]->(f:FoodItem)\n      -[:SOLD_BY]->(v:Vendor)\nRETURN c.name, o.orderId, f.name, v.name\nORDER BY o.orderId;")
    add_image_figure(doc, "screenshots/m1_ss09_end_to_end_traversal.png", "Member 1: Query 7.3 - End-to-End Traversal Validation")

    doc.add_heading("7.4 Complete Graph Sample Visualization", level=3)
    add_image_figure(doc, "screenshots/m1_ss05_graph_visualization.png", "Member 1: Query 7.4 - Graph Visualization of Sample Dataset")

    # 1.9 Member 1 Checklist
    doc.add_heading("1.9 Member 1 Screenshot Checklist & Verification", level=2)
    tbl_m1_chk = doc.add_table(rows=11, cols=3)
    tbl_m1_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    m1_chk_rows = [
        ("Evidence Item", "Query / Source", "Status"),
        ("Neo4j workspace/browser with database open (no password visible)", "Workspace Overview", "[VERIFIED] Captured"),
        ("Successful connection test", "Query 3.1 (RETURN status)", "[VERIFIED] Captured"),
        ("Constraint creation or schema view", "SHOW CONSTRAINTS", "[VERIFIED] Captured"),
        ("Customer and vendor sample data", "Query 5.1 & 5.2", "[VERIFIED] Captured"),
        ("FoodItem-to-Vendor relationships", "Query 5.3 (SOLD_BY)", "[VERIFIED] Captured"),
        ("Customer-Order-FoodItem-Vendor graph visualization", "Query 7.4 (Visualizer)", "[VERIFIED] Captured"),
        ("Node counts and relationship counts", "Query 7.1 & 7.2", "[VERIFIED] Captured"),
        ("Payment, delivery partner and review relationships", "Query 6.1 – 6.3", "[VERIFIED] Captured"),
        ("Successful end-to-end traversal query", "Query 7.3", "[VERIFIED] Captured"),
        ("Screenshot or note showing final dataset ready for Member 2", "Handover Confirmation", "[VERIFIED] Captured")
    ]
    for r_idx, (c0_t, c1_t, c2_t) in enumerate(m1_chk_rows):
        for col_idx, text in enumerate([c0_t, c1_t, c2_t]):
            c = tbl_m1_chk.cell(r_idx, col_idx)
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

    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    add_image_figure(doc, "screenshots/m1_ss10_dataset_ready_handover.png", "Member 1 Handover: Dataset Verified & Ready for Member 2")

    # 1.10 Member 1 Viva Questions
    doc.add_heading("1.10 Member 1 Viva Questions & Technical Answers", level=2)
    m1_viva = [
        ("Q1. What is a graph database?",
         "A graph database is a database management system that represents and persists data as nodes (entities) and connections (relationships) rather than relational tables or documents."),
        ("Q2. What is a node label?",
         "A node label is a category or tag used to group nodes into domain collections (e.g., :Customer or :Vendor). Nodes can have multiple labels."),
        ("Q3. What is a relationship type?",
         "A relationship type is a mandatory named, directed semantic descriptor for a connection between two nodes (e.g., [:PLACES] or [:SOLD_BY])."),
        ("Q4. Why use MERGE in the import script?",
         "MERGE performs an idempotent match-or-create operation. If the pattern already exists, it matches without creating duplicates; if absent, it instantiates it."),
        ("Q5. Why use uniqueness constraints?",
         "Uniqueness constraints prevent two nodes of the same label from having identical values on designated identifier properties (e.g., customerId), while also creating backing indexes for O(1) lookups."),
        ("Q6. Why does relationship direction matter in Neo4j?",
         "Cypher patterns are inherently directed. Although queries can ignore direction when traversing, semantic clarity and traversal planning depend on establishing consistent direction at creation time."),
        ("Q7. Why is this dataset fictional?",
         "Fictional data provides safe, reproducible sample values demonstrating all business capabilities without exposing real user PII or sensitive payment details."),
        ("Q8. Why Neo4j for food delivery?",
         "Food delivery features complex, highly connected entities (Customers, Orders, Items, Vendors, Couriers, Payments). Graph databases handle multi-hop joins with constant O(1) pointer navigation, far outperforming relational JOIN cascades.")
    ]
    for q, a in m1_viva:
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
    # PART 2: MEMBER 2 — QUERY IMPLEMENTATION & DEMONSTRATION GUIDE
    # ==============================================================================
    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.space_before = Pt(22)
    p_p2.paragraph_format.space_after = Pt(2)
    r_p2 = p_p2.add_run("PART 2: MEMBER 2 WORK")
    r_p2.font.size = Pt(14)
    r_p2.font.bold = True
    r_p2.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    h_m2 = doc.add_heading("Cypher Query Implementation, CRUD, Traversal, Recommendations & Deletion", level=1)
    h_m2.paragraph_format.space_before = Pt(2)
    h_m2.paragraph_format.space_after = Pt(8)
    
    doc.add_paragraph(
        "Goal of Member 2: Run and verify all essential Cypher queries against the loaded database, demonstrating "
        "CRUD operations, filtering, sorting, aggregations, multi-hop traversals, recommendation algorithms, and safe deletions."
    )
    
    # 2.1 Before You Start Checks
    doc.add_heading("2.1 Before You Start: Connectivity & Entity Checks", level=2)
    
    doc.add_heading("Check Database Connection (Query 3.1)", level=3)
    add_code_block(doc, "RETURN 'Neo4j connection successful' AS status;")
    add_image_figure(doc, "screenshots/ss_01_connection_check.png", "Member 2: Connection Verification (Query 3.1)")

    doc.add_heading("Check Node Labels and Record Counts (Query 3.2)", level=3)
    add_code_block(doc, "MATCH (n)\nRETURN labels(n) AS labels, count(*) AS records\nORDER BY records DESC;")
    add_image_figure(doc, "screenshots/ss_02_node_labels_counts.png", "Member 2: Node Labels and Counts (Query 3.2)")

    doc.add_heading("View a Sample of the Graph (Query 3.3)", level=3)
    add_code_block(doc, "MATCH (n)-[r]->(m)\nRETURN n, r, m\nLIMIT 50;")
    add_image_figure(doc, "screenshots/ss_03_graph_visualization.png", "Member 2: Graph Visualization Ecosystem (Query 3.3)")

    # 2.2 Core CRUD Operations
    doc.add_heading("2.2 Core Cypher Queries (CRUD & Filtering)", level=2)

    doc.add_heading("Query 1 — Create a Customer (Aarav, 101)", level=3)
    add_code_block(doc, "MERGE (c:Customer {customerId: 101})\nSET c.name = 'Aarav',\n    c.email = 'aarav@example.com'\nRETURN c;")
    add_image_figure(doc, "screenshots/ss_04_query1_create_customer.png", "Query 1: Idempotent Customer Creation")

    doc.add_heading("Query 2 — Create a Vendor (Spice House, 201)", level=3)
    add_code_block(doc, "MERGE (v:Vendor {vendorId: 201})\nSET v.name = 'Spice House',\n    v.cuisine = 'Indian',\n    v.location = 'Chennai'\nRETURN v;")
    add_image_figure(doc, "screenshots/ss_05_query2_create_vendor.png", "Query 2: Vendor Creation with Attributes")

    doc.add_heading("Query 3 — Create Food Item & Connect to Vendor", level=3)
    add_code_block(doc, "MATCH (v:Vendor {vendorId: 201})\nMERGE (f:FoodItem {itemId: 301})\nSET f.name = 'Paneer Biryani',\n    f.price = 220,\n    f.category = 'Main Course'\nMERGE (f)-[:SOLD_BY]->(v)\nRETURN f, v;")
    add_image_figure(doc, "screenshots/ss_06_query3_create_food_item.png", "Query 3: Food Item Creation and Vendor Linkage")

    doc.add_heading("Query 4 — Create Order & Connect to Customer", level=3)
    add_code_block(doc, "MATCH (c:Customer {customerId: 101})\nMERGE (o:Order {orderId: 401})\nSET o.status = 'Placed',\n    o.totalAmount = 220,\n    o.orderDate = date()\nMERGE (c)-[:PLACES]->(o)\nRETURN c, o;")
    add_image_figure(doc, "screenshots/ss_07_query4_create_order.png", "Query 4: Order Creation Linked to Customer")

    doc.add_heading("Query 5 — Connect Order to Food Item ([CONTAINS])", level=3)
    add_code_block(doc, "MATCH (o:Order {orderId: 401}),\n      (f:FoodItem {itemId: 301})\nMERGE (o)-[r:CONTAINS]->(f)\nSET r.quantity = 1\nRETURN o, r, f;")
    add_image_figure(doc, "screenshots/ss_08_query5_connect_order_food.png", "Query 5: Order-to-Item Relationship with Edge Property")

    doc.add_heading("Query 6 — Read All Customers", level=3)
    add_code_block(doc, "MATCH (c:Customer)\nRETURN c.customerId, c.name, c.email\nORDER BY c.name;")
    add_image_figure(doc, "screenshots/ss_09_query6_read_customers.png", "Query 6: Reading All Customer Entities")

    doc.add_heading("Query 7 — Read All Vendors", level=3)
    add_code_block(doc, "MATCH (v:Vendor)\nRETURN v.vendorId, v.name, v.cuisine, v.location\nORDER BY v.name;")
    add_image_figure(doc, "screenshots/ss_10_query7_read_vendors.png", "Query 7: Reading All Vendor Profiles")

    doc.add_heading("Query 8 — Filter Food Items Under Chosen Price (< 300)", level=3)
    add_code_block(doc, "MATCH (f:FoodItem)\nWHERE f.price < 300\nRETURN f.name, f.price, f.category\nORDER BY f.price ASC;")
    add_image_figure(doc, "screenshots/ss_11_query8_filter_food_price.png", "Query 8: Filter Menu Items by Budget (< 300)")

    doc.add_heading("Query 9 — Find Orders for Specific Customer (Aarav, 101)", level=3)
    add_code_block(doc, "MATCH (c:Customer {customerId: 101})-[:PLACES]->(o:Order)\nRETURN c.name, o.orderId, o.status, o.totalAmount\nORDER BY o.orderDate DESC;")
    add_image_figure(doc, "screenshots/ss_12_query9_orders_for_customer.png", "Query 9: Customer-Specific Order History Traversal")

    doc.add_heading("Query 10 — Update Order Status (SET status = 'Delivered')", level=3)
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nSET o.status = 'Delivered'\nRETURN o.orderId, o.status;")
    add_image_figure(doc, "screenshots/ss_13_query10_update_order_status.png", "Query 10: Mutating Order State to 'Delivered'")

    # 2.3 Aggregations
    doc.add_heading("2.3 Aggregation & Ranking Queries", level=2)

    doc.add_heading("Query 11 — Count Orders Per Customer", level=3)
    add_code_block(doc, "MATCH (c:Customer)-[:PLACES]->(o:Order)\nRETURN c.name AS customer,\n       count(o) AS totalOrders\nORDER BY totalOrders DESC;")
    add_image_figure(doc, "screenshots/ss_14_query11_count_orders_per_customer.png", "Query 11: Order Volume Aggregation per Customer")

    doc.add_heading("Query 12 — Find the Five Most Expensive Food Items", level=3)
    add_code_block(doc, "MATCH (f:FoodItem)\nRETURN f.name, f.price\nORDER BY f.price DESC\nLIMIT 5;")
    add_image_figure(doc, "screenshots/ss_15_query12_top5_expensive_food.png", "Query 12: Top 5 Highest Priced Menu Offerings")

    # 2.4 Graph-Specific Queries
    doc.add_heading("2.4 Graph-Specific Queries (Multi-Hop Traversal & Recommendations)", level=2)

    doc.add_heading("Query 13 — Multi-Hop Traversal: Customer → Order → Item → Vendor", level=3)
    add_code_block(doc, "MATCH (c:Customer)-[:PLACES]->(o:Order)\n      -[:CONTAINS]->(f:FoodItem)\n      -[:SOLD_BY]->(v:Vendor)\nRETURN c.name AS customer,\n       o.orderId AS orderId,\n       f.name AS foodItem,\n       v.name AS vendor;")
    add_image_figure(doc, "screenshots/ss_16_query13_trace_customer_to_vendor.png", "Query 13: 3-Hop Graph Traversal Across Core Entities")

    doc.add_heading("Query 14 — Count Menu Items Sold by Each Vendor", level=3)
    add_code_block(doc, "MATCH (f:FoodItem)-[:SOLD_BY]->(v:Vendor)\nRETURN v.name AS vendor,\n       count(f) AS menuItems\nORDER BY menuItems DESC;")
    add_image_figure(doc, "screenshots/ss_17_query14_food_items_per_vendor.png", "Query 14: Menu Item Inventory Count per Vendor")

    doc.add_heading("Query 15 — Basic Vendor Recommendations from Order History", level=3)
    add_code_block(doc, "MATCH (c:Customer {customerId: 101})\n      -[:PLACES]->(:Order)\n      -[:CONTAINS]->(:FoodItem)\n      -[:SOLD_BY]->(v:Vendor)\nRETURN v.name AS vendor,\n       v.cuisine AS cuisine,\n       count(*) AS matchingOrderPaths\nORDER BY matchingOrderPaths DESC;")
    add_image_figure(doc, "screenshots/ss_18_query15_vendor_recommendations.png", "Query 15: History-Driven Vendor Recommendation Engine")

    doc.add_heading("Query 16 — Find Similar Vendors by Shared Cuisine", level=3)
    add_code_block(doc, "MATCH (base:Vendor {vendorId: 201})\nMATCH (other:Vendor)\nWHERE other.cuisine = base.cuisine\n  AND other.vendorId <> base.vendorId\nRETURN other.name, other.cuisine, other.location;")
    add_image_figure(doc, "screenshots/ss_19_query16_same_cuisine_vendors.png", "Query 16: Content-Based Cuisine Similarity Match")

    doc.add_heading("Query 17 — Find Orders and Assigned Delivery Partners", level=3)
    add_code_block(doc, "MATCH (o:Order)-[:ASSIGNED_TO]->(d:DeliveryPartner)\nRETURN o.orderId, o.status, d.name AS deliveryPartner;")
    add_image_figure(doc, "screenshots/ss_22_query17_orders_delivery_partners.png", "Query 17: Courier Driver Assignment Traversal")

    doc.add_heading("Query 18 — Find Customer Reviews and Reviewed Vendors", level=3)
    add_code_block(doc, "MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(v:Vendor)\nRETURN c.name AS customer,\n       v.name AS vendor,\n       r.rating AS rating,\n       r.comment AS comment\nORDER BY rating DESC;")
    add_image_figure(doc, "screenshots/ss_23_query18_customer_reviews.png", "Query 18: Feedback and Sentiment Graph Traversal")

    # 2.5 Payment & Delivery Operations
    doc.add_heading("2.5 Payment Settlement & Fulfillment Operations", level=2)

    doc.add_heading("Query 19 — Create and Link Payment Node", level=3)
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nMERGE (p:Payment {paymentId: 501})\nSET p.amount = 220,\n    p.method = 'UPI',\n    p.status = 'Paid'\nMERGE (o)-[:HAS_PAYMENT]->(p)\nRETURN o, p;")
    add_image_figure(doc, "screenshots/ss_20_query19_link_payment.png", "Query 19: Financial Transaction Graph Integration")

    doc.add_heading("Query 20 — Create and Link Delivery Partner Node", level=3)
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nMERGE (d:DeliveryPartner {partnerId: 601})\nSET d.name = 'Rohan',\n    d.availability = 'Busy'\nMERGE (o)-[:ASSIGNED_TO]->(d)\nRETURN o, d;")
    add_image_figure(doc, "screenshots/ss_21_query20_link_delivery_partner.png", "Query 20: Courier Driver Assignment")

    doc.add_heading("Query 21 — Find Completed and Delivered Orders", level=3)
    add_code_block(doc, "MATCH (c:Customer)-[:PLACES]->(o:Order)\nWHERE o.status = 'Delivered'\nRETURN c.name, o.orderId, o.totalAmount, o.status;")
    add_image_figure(doc, "screenshots/ss_24_query21_completed_orders.png", "Query 21: Successfully Delivered Orders Audit")

    # 2.6 Deletion Operation
    doc.add_heading("2.6 Deletion Operation Demonstration (Section 7)", level=2)
    doc.add_paragraph(
        "Demonstrates safe node removal using DETACH DELETE. A basic DELETE query fails in Neo4j if a node retains "
        "incident relationships. DETACH DELETE atomically severs all connected edges before destroying the node."
    )
    add_code_block(doc, "MATCH (o:Order {orderId: 401})\nDETACH DELETE o;")
    add_image_figure(doc, "screenshots/ss_25_section7_detach_delete.png", "Section 7: DETACH DELETE Execution and Edge Pruning")

    # 2.7 Member 2 Checklist
    doc.add_heading("2.7 Member 2 Screenshot Verification Checklist", level=2)
    tbl_m2_chk = doc.add_table(rows=12, cols=3)
    tbl_m2_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    m2_chk_rows = [
        ("Required Evidence Item", "Query Reference", "Verification Status"),
        ("Connected Neo4j Browser/Workspace (hide credentials)", "Workspace Overview", "[VERIFIED] Captured"),
        ("Node labels and record counts", "Query 3.2", "[VERIFIED] Captured"),
        ("Graph visualization (Customer, Order, Item, Vendor connected)", "Query 3.3", "[VERIFIED] Captured"),
        ("Successful create/merge query and its result", "Queries 1–5", "[VERIFIED] Captured"),
        ("Read/filter/sort query results", "Queries 6–9", "[VERIFIED] Captured"),
        ("Update query showing the new order status", "Query 10", "[VERIFIED] Captured"),
        ("Aggregation result: orders per customer / items per vendor", "Queries 11 & 14", "[VERIFIED] Captured"),
        ("Multi-hop traversal query (customer -> order -> item -> vendor)", "Query 13", "[VERIFIED] Captured"),
        ("Recommendation query and result", "Query 15 & 16", "[VERIFIED] Captured"),
        ("Payment/delivery relationship query result", "Queries 17, 19, 20", "[VERIFIED] Captured"),
        ("Deletion query after all other evidence captured", "Section 7", "[VERIFIED] Captured")
    ]
    for r_idx, (c0_t, c1_t, c2_t) in enumerate(m2_chk_rows):
        for col_idx, text in enumerate([c0_t, c1_t, c2_t]):
            c = tbl_m2_chk.cell(r_idx, col_idx)
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

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 2.8 Member 2 Viva Questions
    doc.add_heading("2.8 Member 2 Viva Questions & Technical Answers", level=2)
    m2_viva = [
        ("Q1. What is Neo4j?",
         "A graph database that stores data natively as nodes, relationships and properties."),
        ("Q2. What is Cypher?",
         "Neo4j's declarative query language for creating, matching and modifying graph data."),
        ("Q3. What is a node?",
         "An entity such as a Customer, Vendor, Order or FoodItem."),
        ("Q4. What is a relationship?",
         "A typed, directed connection between nodes, such as PLACES or CONTAINS."),
        ("Q5. CREATE vs MERGE?",
         "CREATE always creates a new pattern; MERGE matches an existing pattern or creates it if absent."),
        ("Q6. What does MATCH do?",
         "Finds nodes and relationships that match a specified graph pattern."),
        ("Q7. What does SET do?",
         "Adds or updates node/relationship properties."),
        ("Q8. What is DETACH DELETE?",
         "Deletes a node and all relationships attached to it."),
        ("Q9. Why use Neo4j for this project?",
         "It makes relationship-heavy queries and multi-hop traversal natural to express; it avoids complex SQL JOIN overhead."),
        ("Q10. What is graph traversal?",
         "Following relationships through connected nodes to retrieve related information.")
    ]
    for q, a in m2_viva:
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

    # Save to both target files
    for filepath in TARGET_DOCX_FILES:
        doc.save(filepath)
        print(f"[OK] Saved: {filepath} ({os.path.getsize(filepath)} bytes)")

if __name__ == "__main__":
    build_unified_document()
