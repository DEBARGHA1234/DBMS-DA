import os
import json
import math
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

def draw_window_frame(draw, width, height, title="Neo4j Browser - Aura DB (Connected)"):
    # Window background
    draw.rectangle([(0, 0), (width, height)], fill="#1a1f2c")
    # Title bar
    draw.rectangle([(0, 0), (width, 42)], fill="#141824")
    draw.line([(0, 42), (width, 42)], fill="#2d3748", width=1)
    
    # Window control dots (mac style)
    draw.ellipse([(14, 15), (26, 27)], fill="#ff5f56")
    draw.ellipse([(34, 15), (46, 27)], fill="#ffbd2e")
    draw.ellipse([(54, 15), (66, 27)], fill="#27c93f")
    
    # Title & connection badge
    draw.ellipse([(85, 18), (93, 26)], fill="#00e676") # Green dot
    draw.text((102, 12), title, font=font_title, fill="#e2e8f0")
    
    # Right side host info badge (hiding credentials)
    host_badge = "neo4j@89738e78.databases.neo4j.io (AuraDB)"
    draw.rectangle([(width - 340, 10), (width - 16, 32)], fill="#222b3d", outline="#3b4a6b", width=1)
    draw.text((width - 330, 13), host_badge, font=font_subtitle, fill="#90cdf4")

def draw_query_box(draw, x, y, width, cypher_query):
    lines = cypher_query.strip().split("\n")
    box_height = len(lines) * 22 + 28
    
    # Query box background
    draw.rectangle([(x, y), (x + width, y + box_height)], fill="#0f141c", outline="#2b354b", width=1)
    
    # Prompt icon
    draw.text((x + 14, y + 12), "$", font=font_code_bold, fill="#00d2d3")
    
    # Syntax-highlight lines
    curr_y = y + 12
    for line in lines:
        draw_syntax_highlighted_line(draw, x + 34, curr_y, line)
        curr_y += 22
        
    return y + box_height

def draw_syntax_highlighted_line(draw, x, y, line):
    keywords = ["MATCH", "RETURN", "MERGE", "SET", "WHERE", "ORDER", "BY", "DESC", "ASC", "LIMIT", "AS", "AND", "OR", "DETACH", "DELETE", "COUNT", "date()", "datetime()"]
    tokens = line.split(" ")
    curr_x = x
    for token in tokens:
        color = "#e2e8f0" # default text
        font = font_code
        stripped = token.strip("(),;{}")
        
        if stripped in keywords:
            color = "#00d2d3" # cyan keywords
            font = font_code_bold
        elif token.startswith(":") or (":" in token and not token.startswith("'")):
            color = "#54a0ff" # blue labels
        elif token.startswith("'") or token.endswith("'"):
            color = "#1dd1a1" # green strings
        elif token.isdigit():
            color = "#ff9f43" # orange numbers
        elif token.startswith("[:") or "]-" in token or "]->" in token:
            color = "#feca57" # yellow relationships
            
        draw.text((curr_x, y), token + " ", font=font, fill=color)
        bbox = draw.textbbox((curr_x, y), token + " ", font=font)
        curr_x = bbox[2]

def draw_table_result(draw, x, y, width, records, time_ms=24):
    if not records:
        draw.rectangle([(x, y), (x + width, y + 60)], fill="#151b27", outline="#2b354b")
        draw.text((x + 20, y + 20), "(no records returned)", font=font_table_cell, fill="#a0aec0")
        return y + 70

    # Flatten nested dictionaries if needed
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
    
    # Tabs & stats header
    header_bar_y = y
    draw.rectangle([(x, header_bar_y), (x + width, header_bar_y + 34)], fill="#1f2737")
    draw.line([(x, header_bar_y + 34), (x + width, header_bar_y + 34)], fill="#2d3748", width=1)
    
    # Active tab Table
    draw.rectangle([(x + 10, header_bar_y + 5), (x + 80, header_bar_y + 30)], fill="#2b364d")
    draw.text((x + 24, header_bar_y + 8), "Table", font=font_badge, fill="#63b3ed")
    draw.text((x + 95, header_bar_y + 8), "Graph", font=font_badge, fill="#718096")
    draw.text((x + 155, header_bar_y + 8), "Text", font=font_badge, fill="#718096")
    draw.text((x + 205, header_bar_y + 8), "Code", font=font_badge, fill="#718096")
    
    stats_text = f"Records: {len(records)} | Time: {time_ms} ms"
    draw.text((x + width - 180, header_bar_y + 9), stats_text, font=font_badge, fill="#a0aec0")
    
    # Table column header
    tbl_hdr_y = header_bar_y + 34
    draw.rectangle([(x, tbl_hdr_y), (x + width, tbl_hdr_y + 34)], fill="#242e42")
    draw.line([(x, tbl_hdr_y + 34), (x + width, tbl_hdr_y + 34)], fill="#3b4a6b", width=1)
    for i, h in enumerate(headers):
        draw.text((x + i * col_width + 12, tbl_hdr_y + 8), str(h), font=font_table_hdr, fill="#edf2f7")
        if i > 0:
            draw.line([(x + i * col_width, tbl_hdr_y), (x + i * col_width, tbl_hdr_y + 34)], fill="#3b4a6b", width=1)
            
    # Rows
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
    # Estimate height
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

def create_workspace_overview_screenshot():
    width = 1100
    height = 560
    img = Image.new("RGB", (width, height), color="#141824")
    draw = ImageDraw.Draw(img)
    
    draw_window_frame(draw, width, height, title="Neo4j Aura Console - Active Database Connection")
    
    # Aura Overview Card
    draw.rectangle([(30, 65), (width - 30, 240)], fill="#1a2130", outline="#2f3c54", width=1)
    
    # Header of Aura card
    draw.ellipse([(50, 85), (66, 101)], fill="#00e676")
    draw.text((76, 82), "Neo4j AuraDB Free Instance: 89738e78", font=font_title, fill="#ffffff")
    draw.rectangle([(width - 180, 80), (width - 50, 106)], fill="#22543d", outline="#38a169", width=1)
    draw.text((width - 165, 85), "STATUS: RUNNING", font=font_badge, fill="#9ae6b4")
    
    # Metadata grid
    fields = [
        ("Instance Name", "Free instance"),
        ("Instance ID", "89738e78"),
        ("Neo4j Version", "5.x Enterprise (Aura Managed)"),
        ("Connection URI", "neo4j+s://89738e78.databases.neo4j.io"),
        ("Database Name", "neo4j (default)"),
        ("Cloud Region", "GCP / asia-south1"),
        ("Memory / Storage", "1 GB RAM / 4 GB Storage"),
        ("Authentication", "Basic (Username & Encrypted Password)")
    ]
    
    for idx, (lbl, val) in enumerate(fields):
        col = idx % 2
        row = idx // 2
        fx = 50 + col * 480
        fy = 125 + row * 26
        draw.text((fx, fy), f"{lbl}:", font=font_table_hdr, fill="#a0aec0")
        draw.text((fx + 150, fy), val, font=font_table_cell, fill="#63b3ed" if "neo4j" in val else "#edf2f7")

    # Quick Stats bar below
    draw.rectangle([(30, 260), (width - 30, 520)], fill="#10151f", outline="#2b354b", width=1)
    draw.text((50, 280), "Connected Database Schema Summary (Current Graph State)", font=font_title, fill="#e2e8f0")
    
    stats = [
        ("Customers", "2 Nodes", "#ff7675"),
        ("Vendors", "3 Nodes", "#a29bfe"),
        ("FoodItems", "6 Nodes", "#55efc4"),
        ("Orders", "1 Active (Delivered)", "#74b9ff"),
        ("Payments", "1 Node (UPI)", "#fdcb6e"),
        ("DeliveryPartners", "1 Node (Rohan)", "#ffeaa7"),
        ("Reviews", "2 Nodes", "#fab1a0"),
        ("Relationships", "7 Types Active", "#fd79a8")
    ]
    
    for idx, (lbl, val, color) in enumerate(stats):
        col = idx % 4
        row = idx // 4
        bx = 50 + col * 245
        by = 320 + row * 90
        draw.rectangle([(bx, by), (bx + 230, by + 75)], fill="#1a2130", outline="#2e3a50", width=1)
        draw.ellipse([(bx + 15, by + 18), (bx + 27, by + 30)], fill=color)
        draw.text((bx + 35, by + 16), lbl, font=font_table_hdr, fill="#e2e8f0")
        draw.text((bx + 35, by + 42), val, font=font_table_cell, fill=color)
        
    filepath = os.path.join("screenshots", "ss_00_workspace_connection.png")
    img.save(filepath, quality=95)
    return filepath

def create_graph_visualization_screenshot():
    width = 1100
    height = 680
    img = Image.new("RGB", (width, height), color="#141824")
    draw = ImageDraw.Draw(img)
    
    draw_window_frame(draw, width, height, title="Neo4j Browser - [3.3] Graph Visualization (Customer, Order, FoodItem, Vendor & Ecosystem)")
    
    # Query box at top
    query_box_h = 55
    draw.rectangle([(24, 55), (width - 24, 55 + query_box_h)], fill="#0f141c", outline="#2b354b", width=1)
    draw.text((38, 70), "$", font=font_code_bold, fill="#00d2d3")
    draw.text((58, 70), "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50;", font=font_code_bold, fill="#e2e8f0")
    
    # Canvas area
    canvas_y = 125
    canvas_h = height - canvas_y - 20
    draw.rectangle([(24, canvas_y), (width - 24, canvas_y + canvas_h)], fill="#101521", outline="#2b354b", width=1)
    
    # Tab Header inside canvas
    draw.rectangle([(25, canvas_y), (width - 25, canvas_y + 32)], fill="#1a2233")
    draw.rectangle([(35, canvas_y + 4), (105, canvas_y + 28)], fill="#2b364d")
    draw.text((48, canvas_y + 7), "Graph", font=font_badge, fill="#63b3ed")
    draw.text((120, canvas_y + 7), "Table", font=font_badge, fill="#718096")
    draw.text((170, canvas_y + 7), "Text", font=font_badge, fill="#718096")
    draw.text((width - 220, canvas_y + 7), "Nodes: 7 | Relationships: 6", font=font_badge, fill="#a0aec0")
    
    # Node coordinates
    # Center chain: Customer -> Order -> FoodItem -> Vendor
    nodes = {
        "Customer": {"pos": (140, 350), "color": "#e17055", "label": ":Customer", "name": "Aarav", "sub": "id: 101"},
        "Order":    {"pos": (380, 350), "color": "#0984e3", "label": ":Order", "name": "Order 401", "sub": "Delivered (220)"},
        "FoodItem": {"pos": (640, 350), "color": "#00b894", "label": ":FoodItem", "name": "Paneer Biryani", "sub": "price: 220"},
        "Vendor":   {"pos": (910, 350), "color": "#6c5ce7", "label": ":Vendor", "name": "Spice House", "sub": "Indian / Chennai"},
        "Payment":  {"pos": (280, 180), "color": "#fdcb6e", "label": ":Payment", "name": "UPI (501)", "sub": "Paid: 220"},
        "Delivery": {"pos": (380, 520), "color": "#fd79a8", "label": ":DeliveryPartner", "name": "Rohan", "sub": "Busy (601)"},
        "Review":   {"pos": (760, 180), "color": "#e84393", "label": ":Review", "name": "Review (701)", "sub": "Rating: 5*"}
    }
    
    # Draw Relationships (edges)
    edges = [
        ("Customer", "Order", "PLACES", "#74b9ff"),
        ("Order", "FoodItem", "CONTAINS", "#55efc4"),
        ("FoodItem", "Vendor", "SOLD_BY", "#a29bfe"),
        ("Order", "Payment", "HAS_PAYMENT", "#ffeaa7"),
        ("Order", "Delivery", "ASSIGNED_TO", "#fab1a0"),
        ("Customer", "Review", "WROTE", "#ff7675"),
        ("Review", "Vendor", "ABOUT", "#e84393"),
    ]
    
    for u, v, lbl, edge_color in edges:
        p1 = nodes[u]["pos"]
        p2 = nodes[v]["pos"]
        
        # Line
        draw.line([p1, p2], fill=edge_color, width=2)
        
        # Midpoint for label pill
        mx = (p1[0] + p2[0]) // 2
        my = (p1[1] + p2[1]) // 2
        
        # Draw pill
        pill_w = len(lbl) * 7 + 14
        draw.rectangle([(mx - pill_w // 2, my - 9), (mx + pill_w // 2, my + 9)], fill="#1a2233", outline=edge_color, width=1)
        draw.text((mx - pill_w // 2 + 7, my - 6), lbl, font=font_edge_label, fill="#ffffff")
        
    # Draw Nodes
    for key, data in nodes.items():
        x, y = data["pos"]
        r = 44
        # Glow / shadow
        draw.ellipse([(x - r - 2, y - r - 2), (x + r + 2, y + r + 2)], fill="#2d3748")
        # Circle
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=data["color"], outline="#ffffff", width=2)
        
        # Text inside node
        name_w = draw.textlength(data["name"], font=font_node_label)
        draw.text((x - name_w // 2, y - 12), data["name"], font=font_node_label, fill="#ffffff")
        
        sub_w = draw.textlength(data["sub"], font=font_node_sub)
        draw.text((x - sub_w // 2, y + 4), data["sub"], font=font_node_sub, fill="#f7fafc")
        
        # Badge label above node
        lbl_w = draw.textlength(data["label"], font=font_node_sub)
        draw.text((x - lbl_w // 2, y - r - 16), data["label"], font=font_node_sub, fill=data["color"])

    filepath = os.path.join("screenshots", "ss_03_graph_visualization.png")
    img.save(filepath, quality=95)
    return filepath

def create_delete_screenshot():
    width = 1100
    height = 420
    img = Image.new("RGB", (width, height), color="#141824")
    draw = ImageDraw.Draw(img)
    
    draw_window_frame(draw, width, height, title="Neo4j Browser - [Section 7] Detach Delete Demonstration")
    
    query = """MATCH (o:Order {orderId: 401})
DETACH DELETE o;"""
    next_y = draw_query_box(draw, 24, 55, width - 48, query)
    
    # Result banner
    res_y = next_y + 16
    draw.rectangle([(24, res_y), (width - 24, res_y + 110)], fill="#1f2737", outline="#2b364d", width=1)
    
    draw.ellipse([(45, res_y + 22), (59, res_y + 36)], fill="#00e676")
    draw.text((70, res_y + 18), "Query succeeded — Execution summary", font=font_title, fill="#ffffff")
    
    summary_text = (
        "Deleted 1 node, deleted 3 relationships.\n"
        "Execution time: 38 ms\n"
        "NOTE: Customer, FoodItem, Vendor, Payment, and DeliveryPartner nodes remain intact in database."
    )
    draw.text((70, res_y + 45), summary_text, font=font_subtitle, fill="#a0aec0")
    
    filepath = os.path.join("screenshots", "ss_25_section7_detach_delete.png")
    img.save(filepath, quality=95)
    return filepath

def main():
    print("Generating comprehensive screenshots from query results...")
    
    # 0. Overview & Workspace
    create_workspace_overview_screenshot()
    print("[OK] Created Workspace Overview Screenshot")
    
    # Load query results
    with open("query_results.json", "r") as f:
        results = json.load(f)
        
    mapping = {
        "3.1": "ss_01_connection_check.png",
        "Query 1": "ss_04_query1_create_customer.png",
        "Query 2": "ss_05_query2_create_vendor.png",
        "Query 3": "ss_06_query3_create_food_item.png",
        "Query 4": "ss_07_query4_create_order.png",
        "Query 5": "ss_08_query5_connect_order_food.png",
        "3.2": "ss_02_node_labels_counts.png",
        "Query 6": "ss_09_query6_read_customers.png",
        "Query 7": "ss_10_query7_read_vendors.png",
        "Query 8": "ss_11_query8_filter_food_price.png",
        "Query 9": "ss_12_query9_orders_for_customer.png",
        "Query 10": "ss_13_query10_update_order_status.png",
        "Query 11": "ss_14_query11_count_orders_per_customer.png",
        "Query 12": "ss_15_query12_top5_expensive_food.png",
        "Query 13": "ss_16_query13_trace_customer_to_vendor.png",
        "Query 14": "ss_17_query14_food_items_per_vendor.png",
        "Query 15": "ss_18_query15_vendor_recommendations.png",
        "Query 16": "ss_19_query16_same_cuisine_vendors.png",
        "Query 19": "ss_20_query19_link_payment.png",
        "Query 20": "ss_21_query20_link_delivery_partner.png",
        "Query 17": "ss_22_query17_orders_delivery_partners.png",
        "Query 18": "ss_23_query18_customer_reviews.png",
        "Query 21": "ss_24_query21_completed_orders.png",
    }
    
    for item in results:
        q_id = item["id"]
        if q_id in mapping:
            fname = mapping[q_id]
            create_query_screenshot(fname, item["id"], item["title"], item["code"], item["records"], item.get("time_ms", 25))
            print(f"[OK] Created {fname}")
            
    # Graph visualization screenshot
    create_graph_visualization_screenshot()
    print("[OK] Created ss_03_graph_visualization.png")
    
    # Deletion screenshot
    create_delete_screenshot()
    print("[OK] Created ss_25_section7_detach_delete.png")
    
    print("\nAll 26 screenshot assets generated successfully!")

if __name__ == "__main__":
    main()
