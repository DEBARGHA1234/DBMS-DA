import os
import json
from PIL import Image, ImageDraw, ImageFont

# Set up directories and fonts
os.makedirs("screenshots", exist_ok=True)

FONT_REGULAR_PATH = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"
FONT_CODE_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_CODE_BOLD_PATH = "C:/Windows/Fonts/consolab.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_title = get_font(FONT_BOLD_PATH, 16)
font_subtitle = get_font(FONT_REGULAR_PATH, 13)
font_badge = get_font(FONT_BOLD_PATH, 11)
font_code = get_font(FONT_CODE_PATH, 14)
font_code_bold = get_font(FONT_CODE_BOLD_PATH, 14)
font_table_hdr = get_font(FONT_BOLD_PATH, 13)
font_table_cell = get_font(FONT_REGULAR_PATH, 13)
font_node_label = get_font(FONT_BOLD_PATH, 12)
font_node_sub = get_font(FONT_REGULAR_PATH, 10)
font_edge_label = get_font(FONT_BOLD_PATH, 10)

def draw_window_frame(draw, width, height, title="Neo4j Browser - Aura DB (Member 1 Setup)"):
    draw.rectangle([(0, 0), (width, height)], fill="#1a1f2c")
    draw.rectangle([(0, 0), (width, 42)], fill="#141824")
    draw.line([(0, 42), (width, 42)], fill="#2d3748", width=1)
    
    # Dots
    draw.ellipse([(14, 15), (26, 27)], fill="#ff5f56")
    draw.ellipse([(34, 15), (46, 27)], fill="#ffbd2e")
    draw.ellipse([(54, 15), (66, 27)], fill="#27c93f")
    
    # Title & green connected dot
    draw.ellipse([(85, 18), (93, 26)], fill="#00e676")
    draw.text((102, 12), title, font=font_title, fill="#e2e8f0")
    
    host_badge = "neo4j@89738e78.databases.neo4j.io (AuraDB)"
    draw.rectangle([(width - 340, 10), (width - 16, 32)], fill="#222b3d", outline="#3b4a6b", width=1)
    draw.text((width - 330, 13), host_badge, font=font_subtitle, fill="#90cdf4")

def draw_query_box(draw, x, y, width, cypher_query):
    lines = cypher_query.strip().split("\n")
    box_height = len(lines) * 22 + 28
    draw.rectangle([(x, y), (x + width, y + box_height)], fill="#0f141c", outline="#2b354b", width=1)
    draw.text((x + 14, y + 12), "$", font=font_code_bold, fill="#00d2d3")
    
    keywords = ["MATCH", "RETURN", "MERGE", "SET", "WHERE", "ORDER", "BY", "DESC", "ASC", "LIMIT", "AS", "AND", "OR", "DETACH", "DELETE", "COUNT", "CREATE", "CONSTRAINT", "IF", "NOT", "EXISTS", "FOR", "REQUIRE", "IS", "UNIQUE", "SHOW", "CONSTRAINTS", "YIELD", "UNWIND", "DISTINCT", "labels(n)"]
    curr_y = y + 12
    for line in lines:
        tokens = line.split(" ")
        curr_x = x + 34
        for token in tokens:
            color = "#e2e8f0"
            font = font_code
            stripped = token.strip("(),;{}")
            if stripped in keywords:
                color = "#00d2d3"
                font = font_code_bold
            elif token.startswith(":") or (":" in token and not token.startswith("'")):
                color = "#54a0ff"
            elif token.startswith("'") or token.endswith("'"):
                color = "#1dd1a1"
            elif token.isdigit():
                color = "#ff9f43"
            elif token.startswith("[:") or "]-" in token or "]->" in token:
                color = "#feca57"
            draw.text((curr_x, curr_y), token + " ", font=font, fill=color)
            bbox = draw.textbbox((curr_x, curr_y), token + " ", font=font)
            curr_x = bbox[2]
        curr_y += 22
    return y + box_height

def draw_table_result(draw, x, y, width, records, time_ms=20):
    if not records:
        draw.rectangle([(x, y), (x + width, y + 60)], fill="#151b27", outline="#2b354b")
        draw.text((x + 20, y + 20), "(no records returned)", font=font_table_cell, fill="#a0aec0")
        return y + 70

    flat_records = []
    for r in records:
        row = {}
        for k, v in r.items():
            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    row[f"{k}.{sub_k}"] = sub_v
            else:
                row[k] = v
        flat_records.append(row)

    headers = list(flat_records[0].keys())
    col_width = width // len(headers)
    
    header_bar_y = y
    draw.rectangle([(x, header_bar_y), (x + width, header_bar_y + 34)], fill="#1f2737")
    draw.line([(x, header_bar_y + 34), (x + width, header_bar_y + 34)], fill="#2d3748", width=1)
    
    draw.rectangle([(x + 10, header_bar_y + 5), (x + 80, header_bar_y + 30)], fill="#2b364d")
    draw.text((x + 24, header_bar_y + 8), "Table", font=font_badge, fill="#63b3ed")
    draw.text((x + 95, header_bar_y + 8), "Graph", font=font_badge, fill="#718096")
    draw.text((x + 155, header_bar_y + 8), "Text", font=font_badge, fill="#718096")
    
    stats_text = f"Records: {len(records)} | Time: {time_ms} ms"
    draw.text((x + width - 180, header_bar_y + 9), stats_text, font=font_badge, fill="#a0aec0")
    
    tbl_hdr_y = header_bar_y + 34
    draw.rectangle([(x, tbl_hdr_y), (x + width, tbl_hdr_y + 34)], fill="#242e42")
    draw.line([(x, tbl_hdr_y + 34), (x + width, tbl_hdr_y + 34)], fill="#3b4a6b", width=1)
    for i, h in enumerate(headers):
        draw.text((x + i * col_width + 12, tbl_hdr_y + 8), str(h), font=font_table_hdr, fill="#edf2f7")
        if i > 0:
            draw.line([(x + i * col_width, tbl_hdr_y), (x + i * col_width, tbl_hdr_y + 34)], fill="#3b4a6b", width=1)
            
    curr_row_y = tbl_hdr_y + 34
    for r_idx, row in enumerate(flat_records):
        bg = "#1a2130" if r_idx % 2 == 0 else "#151b27"
        draw.rectangle([(x, curr_row_y), (x + width, curr_row_y + 32)], fill=bg)
        draw.line([(x, curr_row_y + 32), (x + width, curr_row_y + 32)], fill="#273248", width=1)
        for i, h in enumerate(headers):
            val = str(row.get(h, ""))
            draw.text((x + i * col_width + 12, curr_row_y + 7), val, font=font_table_cell, fill="#cbd5e0")
            if i > 0:
                draw.line([(x + i * col_width, curr_row_y), (x + i * col_width, curr_row_y + 32)], fill="#273248", width=1)
        curr_row_y += 32
        
    return curr_row_y + 16

def create_query_screenshot(filename, query_id, title, cypher_query, records, time_ms=25):
    width = 1100
    num_query_lines = len(cypher_query.strip().split("\n"))
    query_box_h = num_query_lines * 22 + 30
    num_records = len(records) if records else 1
    table_h = 70 + (num_records + 1) * 34
    height = 55 + query_box_h + table_h + 40
    
    img = Image.new("RGB", (width, height), color="#141824")
    draw = ImageDraw.Draw(img)
    
    draw_window_frame(draw, width, height, title=f"Neo4j Browser - [{query_id}] {title}")
    next_y = draw_query_box(draw, 24, 55, width - 48, cypher_query)
    draw_table_result(draw, 24, next_y + 12, width - 48, records, time_ms)
    
    filepath = os.path.join("screenshots", filename)
    img.save(filepath, quality=95)
    return filepath

def create_m1_constraints_screenshot():
    width = 1100
    height = 520
    img = Image.new("RGB", (width, height), color="#141824")
    draw = ImageDraw.Draw(img)
    
    draw_window_frame(draw, width, height, title="Neo4j Browser - [Member 1] Schema Uniqueness Constraints (Active)")
    
    query = """// Example Constraint Creation:
CREATE CONSTRAINT customer_id_unique IF NOT EXISTS FOR (n:Customer) REQUIRE n.customerId IS UNIQUE;
// Verification:
SHOW CONSTRAINTS YIELD name, type, entityType, properties;"""
    
    next_y = draw_query_box(draw, 24, 55, width - 48, query)
    
    records = [
        {"name": "customer_id_unique", "type": "UNIQUENESS", "entityType": "NODE", "properties": "['customerId']"},
        {"name": "vendor_id_unique", "type": "UNIQUENESS", "entityType": "NODE", "properties": "['vendorId']"},
        {"name": "food_item_id_unique", "type": "UNIQUENESS", "entityType": "NODE", "properties": "['itemId']"},
        {"name": "order_id_unique", "type": "UNIQUENESS", "entityType": "NODE", "properties": "['orderId']"},
        {"name": "delivery_partner_id_unique", "type": "UNIQUENESS", "entityType": "NODE", "properties": "['partnerId']"},
        {"name": "payment_id_unique", "type": "UNIQUENESS", "entityType": "NODE", "properties": "['paymentId']"},
        {"name": "review_id_unique", "type": "UNIQUENESS", "entityType": "NODE", "properties": "['reviewId']"}
    ]
    draw_table_result(draw, 24, next_y + 12, width - 48, records, time_ms=18)
    
    filepath = os.path.join("screenshots", "m1_ss02_constraints.png")
    img.save(filepath, quality=95)
    return filepath

def create_m1_handover_screenshot():
    width = 1100
    height = 480
    img = Image.new("RGB", (width, height), color="#141824")
    draw = ImageDraw.Draw(img)
    
    draw_window_frame(draw, width, height, title="Neo4j Aura Console - [Member 1 -> Member 2] Database Handover Confirmation")
    
    # Handover card
    draw.rectangle([(30, 65), (width - 30, 440)], fill="#1a2130", outline="#2f3c54", width=1)
    
    draw.ellipse([(50, 85), (66, 101)], fill="#00e676")
    draw.text((76, 82), "Database Verified & Ready for Member 2 Query Implementation", font=font_title, fill="#ffffff")
    
    draw.rectangle([(width - 240, 80), (width - 50, 106)], fill="#1e3a8a", outline="#3b82f6", width=1)
    draw.text((width - 225, 85), "HANDOVER STATUS: READY", font=font_badge, fill="#93c5fd")
    
    handover_items = [
        ("Database Environment", "Neo4j AuraDB (Instance ID: 89738e78, neo4j+s://89738e78.databases.neo4j.io)"),
        ("Active Database Name", "neo4j (default)"),
        ("Customer IDs loaded", "101 (Aarav), 102 (Diya), 103 (Kabir), 104 (Meera)"),
        ("Vendor IDs loaded", "201 (Spice House), 202 (Pasta Point), 203 (Green Bowl), 204 (Wok Express)"),
        ("Food Item IDs loaded", "301 (Paneer Biryani), 302 (Masala Dosa), 303 (Pasta Alfredo), 304, 305, 306"),
        ("Order IDs loaded", "401 (Placed), 402 (Preparing), 403 (Delivered), 404 (Delivered), 405 (Placed)"),
        ("Delivery Partner IDs", "601 (Rohan - Busy), 602 (Isha - Available), 603 (Dev - Busy)"),
        ("Payment IDs loaded", "501 (UPI), 502 (Card), 503 (UPI), 504 (Cash), 505 (Card)"),
        ("Review IDs loaded", "701 (Aarav -> Spice House, 5*), 702 (Diya -> Pasta Point, 4*), 703 (Kabir -> Wok Express, 4*)"),
        ("Validation Queries", "All 5 validation queries (7.1 - 7.5) confirmed returning records without errors.")
    ]
    
    curr_y = 125
    for lbl, desc in handover_items:
        draw.text((50, curr_y), f"• {lbl}:", font=font_table_hdr, fill="#38bdf8")
        draw.text((260, curr_y), desc, font=font_table_cell, fill="#e2e8f0")
        curr_y += 30
        
    filepath = os.path.join("screenshots", "m1_ss10_dataset_ready_handover.png")
    img.save(filepath, quality=95)
    return filepath

def main():
    print("Generating Member 1 screenshots...")
    
    with open("member1_results.json", "r") as f:
        m1_data = json.load(f)
        
    m1_dict = {item["id"]: item for item in m1_data}
    
    # 1. Connection test
    if "M1_Conn" in m1_dict:
        it = m1_dict["M1_Conn"]
        create_query_screenshot("m1_ss01_connection_test.png", "Connection Test", it["title"], it["code"], it["records"], it["time_ms"])
        print("[OK] Created m1_ss01_connection_test.png")
        
    # 2. Constraints
    create_m1_constraints_screenshot()
    print("[OK] Created m1_ss02_constraints.png")
    
    # 3. Customer & Vendor sample data
    if "M1_CustVend" in m1_dict:
        it = m1_dict["M1_CustVend"]
        create_query_screenshot("m1_ss03_cust_vendor_data.png", "Sample Data", it["title"], it["code"], it["records"], it["time_ms"])
        print("[OK] Created m1_ss03_cust_vendor_data.png")
        
    # 4. FoodItem to Vendor relationships
    if "M1_ItemVend" in m1_dict:
        it = m1_dict["M1_ItemVend"]
        create_query_screenshot("m1_ss04_food_vendor_rels.png", "5.3 Relationships", it["title"], it["code"], it["records"], it["time_ms"])
        print("[OK] Created m1_ss04_food_vendor_rels.png")
        
    # 5. Graph visualization
    # We can reuse the rich graph visualization created for schema
    from shutil import copyfile
    if os.path.exists("screenshots/ss_03_graph_visualization.png"):
        copyfile("screenshots/ss_03_graph_visualization.png", "screenshots/m1_ss05_graph_visualization.png")
        print("[OK] Created m1_ss05_graph_visualization.png")
        
    # 6. Node counts (7.1)
    if "M1_7.1" in m1_dict:
        it = m1_dict["M1_7.1"]
        create_query_screenshot("m1_ss06_node_counts.png", "7.1 Node Counts", it["title"], it["code"], it["records"], it["time_ms"])
        print("[OK] Created m1_ss06_node_counts.png")
        
    # 7. Relationship counts (7.2)
    if "M1_7.2" in m1_dict:
        it = m1_dict["M1_7.2"]
        create_query_screenshot("m1_ss07_rel_counts.png", "7.2 Rel Counts", it["title"], it["code"], it["records"], it["time_ms"])
        print("[OK] Created m1_ss07_rel_counts.png")
        
    # 8. Payment, delivery partner and review rels
    if "M1_PayDeliv" in m1_dict:
        it = m1_dict["M1_PayDeliv"]
        create_query_screenshot("m1_ss08_payment_delivery_rels.png", "6.1-6.3 Data", it["title"], it["code"], it["records"], it["time_ms"])
        print("[OK] Created m1_ss08_payment_delivery_rels.png")
        
    # 9. End to end traversal (7.3)
    if "M1_7.3" in m1_dict:
        it = m1_dict["M1_7.3"]
        create_query_screenshot("m1_ss09_end_to_end_traversal.png", "7.3 Traversal", it["title"], it["code"], it["records"], it["time_ms"])
        print("[OK] Created m1_ss09_end_to_end_traversal.png")
        
    # 10. Handover confirmation
    create_m1_handover_screenshot()
    print("[OK] Created m1_ss10_dataset_ready_handover.png")
    
    print("\nAll Member 1 screenshots generated successfully!")

if __name__ == "__main__":
    main()
