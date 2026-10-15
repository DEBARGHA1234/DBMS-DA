import os
import certifi
import ssl
from dotenv import load_dotenv
import neo4j

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME", "89738e78")
password = os.getenv("NEO4J_PASSWORD")

print(f"Connecting to: {uri}")
print(f"Username: {user}")

try:
    with neo4j.GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        print("[SUCCESS] Connectivity verified!")
        with driver.session() as session:
            record = session.run("RETURN 'Connection verified successfully!' AS status, datetime() AS ts").single()
            print(f"[SUCCESS] Query response: {record['status']} at {record['ts']}")
except Exception as e:
    print(f"Connection error: {type(e).__name__}: {e}")
