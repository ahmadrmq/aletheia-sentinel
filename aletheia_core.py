import json
import time
import re
import logging
import datetime
import uuid
import sys
import os
import random

# --- Configuration & Constants ---
LOG_FILE = "audit_log.json"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Forensic Logging (Cloudant Simulation) ---
class CloudantLogger:
    def __init__(self, filepath=LOG_FILE):
        self.filepath = filepath
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def log_violation(self, entry):
        """Append violation record to the JSON log file."""
        try:
            with open(self.filepath, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
        
        logs.append(entry)
        
        with open(self.filepath, 'w') as f:
            json.dump(logs, f, indent=4)

# --- Governance Engine ---
class GovernanceEngine:
    def __init__(self):
        # We assign risk scores to keywords for the "Forensic Report"
        self.risk_patterns = {
            r"password": 85,
            r"hack": 90,
            r"ssn": 95,
            r"secret": 75,
            r"drop table": 100
        }
        # Compile a master regex for detection
        pattern_str = "|".join(self.risk_patterns.keys())
        self.regex = re.compile(f"({pattern_str})", re.IGNORECASE)

    def mock_nlu_analysis(self):
        """Simulate Watson NLU processing delay with detailed visual feedback."""
        print(f"{Colors.CYAN}{Colors.BOLD}>> Initiating Aletheia Cortex Analysis...{Colors.ENDC}")
        
        steps = [
            ("Tokenizing Input Stream", 0.15),
            ("Extracting Entities (NER)", 0.2),
            ("Analyzing Sentiment & Tone", 0.1),
            ("Cross-referencing Threat Intelligence", 0.25)
        ]
        
        toolbar_width = 30
        
        # Draw a fancy progress bar
        sys.stdout.write("Loading: [%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width + 1)) 

        for i in range(toolbar_width):
            time.sleep(0.01) # Fast filler for visual effect
            sys.stdout.write(f"{Colors.BLUE}#{Colors.ENDC}")
            sys.stdout.flush()
        sys.stdout.write("]\n")

        # Simulate detailed steps
        for step, delay in steps:
            time.sleep(delay)  # Simulate compute time
            status = f"{Colors.BLUE}   [+]{Colors.ENDC} {step}..."
            print(status)
            
        # Final "metrics"
        latency = round(random.uniform(0.12, 0.48), 3)
        confidence = round(random.uniform(0.88, 0.99), 2)
        print(f"{Colors.CYAN}   >>> Analysis Complete. Latency: {latency}s | Model Confidence: {confidence}{Colors.ENDC}\n")

    def scan(self, text):
        """
        Scans text for violations.
        Returns: (is_safe, details_dict)
        """
        match = self.regex.search(text)
        if match:
            keyword = match.group(0).lower()
            # Find the risk score associated with the matched keyword (or default to high)
            # We iterate because the regex match is the string, not the pattern key directly
            score = 0
            for pat, s in self.risk_patterns.items():
                if re.search(pat, keyword, re.IGNORECASE):
                    score = s
                    break
            
            return False, {
                "violation_type": "Prohibited Content",
                "keyword_detected": keyword,
                "risk_score": score
            }
        return True, {}

# --- Main Application Logic ---
def main():
    # Initialize components
    logger = CloudantLogger()
    engine = GovernanceEngine()
    
    # Generate a session-based User ID
    session_user_id = str(uuid.uuid4())[:8]

    print(f"{Colors.HEADER}{Colors.BOLD}=== Aletheia Sentinel: Agentic Governance Active ==={Colors.ENDC}")
    print(f"Session User ID: {session_user_id}")
    print("Type 'exit' or 'quit' to terminate session.\n")

    while True:
        try:
            user_input = input(f"{Colors.BLUE}Sentinel > {Colors.ENDC}").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Shutting down Aletheia Sentinel...")
                break
                
            if not user_input:
                continue

            # 1. Forensic NLU Simulation
            engine.mock_nlu_analysis()

            # 2. Governance Check
            is_safe, details = engine.scan(user_input)

            # 3. Decision & Action
            timestamp = datetime.datetime.now().isoformat()
            
            if is_safe:
                # GREEN Approved Message
                print(f"\n{Colors.GREEN}{Colors.BOLD}[PASSED] Request Approved.{Colors.ENDC}")
                print(f"Payload processed: {user_input}\n")
            else:
                # RED Blocked Message
                print(f"\n{Colors.RED}{Colors.BOLD}[BLOCKED] Security Violation Detected.{Colors.ENDC}")
                
                # 4. Forensic Report
                risk_score = details.get("risk_score", 100)
                keyword = details.get("keyword_detected", "UNKNOWN")
                
                print(f"{Colors.WARNING}")
                print("+" + "-"*50 + "+")
                print(f"| {'FORENSIC REPORT':^48} |")
                print("+" + "-"*50 + "+")
                print(f"| Timestamp  : {timestamp:<35} |")
                print(f"| User ID    : {session_user_id:<35} |")
                print(f"| Violation  : {keyword:<35} |")
                print(f"| Risk Score : {risk_score:<35} |")
                print("+" + "-"*50 + "+")
                print(f"{Colors.ENDC}\n")

                # 5. Log to "Cloud"
                log_entry = {
                    "event_id": str(uuid.uuid4()),
                    "timestamp": timestamp,
                    "user_id": session_user_id,
                    "input_text": user_input,
                    "risk_assessment": details
                }
                logger.log_violation(log_entry)

        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting...")
            break

if __name__ == "__main__":
    main()
