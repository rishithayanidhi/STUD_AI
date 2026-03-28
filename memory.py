"""
PostgreSQL-backed memory system for storing and retrieving tickets.
Automatic fallback to JSON if database unavailable.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# PostgreSQL imports
try:
    import psycopg2  # type: ignore
    from psycopg2.extras import execute_values  # type: ignore
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️  psycopg2 not installed. Install with: pip install psycopg2-binary")

# JSON fallback
MEMORY_FILE = Path(__file__).parent / "tickets.json"


class MemorySystem:
    """PostgreSQL-backed memory for autonomous ops tickets."""
    
    def __init__(self):
        """Initialize memory system - try PostgreSQL, fall back to JSON."""
        self.use_postgres = False
        self.conn = None
        self.tickets = []  # Fallback list
        
        # Try to connect to PostgreSQL
        if POSTGRES_AVAILABLE:
            self._init_postgres()
        else:
            print("⚠️  psycopg2 not installed. Using JSON file fallback.")
            print("   To use PostgreSQL: pip install psycopg2-binary")
        
        # Always load JSON as fallback
        self.load_from_file()
    
    def _init_postgres(self) -> None:
        """Initialize PostgreSQL connection and create tables."""
        try:
            # Get connection parameters from environment or use defaults
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "autonomous_ops")
            db_user = os.getenv("DB_USER", "postgres")
            db_password = os.getenv("DB_PASSWORD", "postgres")
            
            # Connect to PostgreSQL
            self.conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password,
                connect_timeout=5
            )
            
            # Create tables if they don't exist
            self._create_tables()
            self.use_postgres = True
            print(f"✅ PostgreSQL connected: {db_user}@{db_host}:{db_port}/{db_name}")
            
        except Exception as e:
            print(f"⚠️  PostgreSQL connection failed: {e}")
            print("   Using JSON file fallback instead")
            self.use_postgres = False
            if self.conn:
                self.conn.close()
                self.conn = None
    
    def _create_tables(self) -> None:
        """Create necessary PostgreSQL tables."""
        if not self.conn:
            return
        
        cursor = self.conn.cursor()
        try:
            # Main tickets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    ticket_id VARCHAR(255) UNIQUE NOT NULL,
                    issue TEXT NOT NULL,
                    priority VARCHAR(50),
                    category VARCHAR(50),
                    team VARCHAR(255),
                    confidence FLOAT,
                    decision JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for faster searches
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tickets_issue 
                ON tickets USING GIN (to_tsvector('english', issue))
            """)
            
            # Actions log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS actions_log (
                    id SERIAL PRIMARY KEY,
                    ticket_id VARCHAR(255) REFERENCES tickets(ticket_id),
                    action VARCHAR(255),
                    status VARCHAR(50),
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
            
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()
        finally:
            cursor.close()
    
    def store_ticket(self, issue: str, decision: dict) -> None:
        """Store ticket in PostgreSQL (or JSON fallback)."""
        ticket_id = issue[:20].replace(" ", "_").lower()
        
        # Store in PostgreSQL if available
        if self.use_postgres and self.conn:
            self._store_in_postgres(ticket_id, issue, decision)
        
        # Always store in JSON as backup
        ticket = {
            "issue": issue,
            "decision": decision,
            "id": ticket_id,
            "timestamp": datetime.now().isoformat()
        }
        self.tickets.append(ticket)
        self.save_to_file()
    
    def _store_in_postgres(self, ticket_id: str, issue: str, decision: dict) -> None:
        """Store ticket in PostgreSQL."""
        if not self.conn:
            return
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO tickets 
                (ticket_id, issue, priority, category, team, confidence, decision)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticket_id) DO UPDATE SET
                    updated_at = CURRENT_TIMESTAMP,
                    decision = EXCLUDED.decision
            """, (
                ticket_id,
                issue,
                decision.get("priority"),
                decision.get("category"),
                decision.get("team"),
                decision.get("confidence", 0.0),
                json.dumps(decision)
            ))
            self.conn.commit()
            
        except Exception as e:
            print(f"PostgreSQL insert error: {e}")
            self.conn.rollback()
        finally:
            cursor.close()
    
    def find_similar_tickets(self, issue: str, n_results: int = 3) -> List[str]:
        """Find similar past tickets using PostgreSQL or fallback."""
        if self.use_postgres and self.conn:
            return self._find_similar_postgres(issue, n_results)
        
        # Fallback: simple substring matching
        similar = []
        for ticket in self.tickets:
            if any(word in ticket["issue"].lower() for word in issue.lower().split()):
                similar.append(ticket["issue"])
        return similar[:n_results]
    
    def _find_similar_postgres(self, issue: str, n_results: int) -> List[str]:
        """Find similar tickets using PostgreSQL full-text search."""
        if not self.conn:
            return []
        
        cursor = self.conn.cursor()
        try:
            # Use PostgreSQL full-text search
            cursor.execute("""
                SELECT issue 
                FROM tickets
                WHERE to_tsvector('english', issue) @@ 
                      plainto_tsquery('english', %s)
                ORDER BY ts_rank(to_tsvector('english', issue), 
                        plainto_tsquery('english', %s)) DESC
                LIMIT %s
            """, (issue, issue, n_results))
            
            results = cursor.fetchall()
            return [row[0] for row in results] if results else []
            
        except Exception as e:
            print(f"PostgreSQL search error: {e}")
            return []
        finally:
            cursor.close()
    
    def get_tickets(self, limit: int = 100) -> List[dict]:
        """Get all tickets from PostgreSQL or JSON."""
        if self.use_postgres and self.conn:
            return self._get_tickets_postgres(limit)
        
        return self.tickets[:limit]
    
    def _get_tickets_postgres(self, limit: int) -> List[dict]:
        """Retrieve tickets from PostgreSQL."""
        if not self.conn:
            return []
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT ticket_id, issue, priority, category, team, 
                       confidence, decision, created_at
                FROM tickets
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            
            results = cursor.fetchall()
            tickets = []
            for row in results:
                tickets.append({
                    "id": row[0],
                    "issue": row[1],
                    "priority": row[2],
                    "category": row[3],
                    "team": row[4],
                    "confidence": row[5],
                    "decision": json.loads(row[6]) if row[6] else {},
                    "created_at": row[7].isoformat() if row[7] else None
                })
            return tickets
            
        except Exception as e:
            print(f"PostgreSQL retrieve error: {e}")
            return []
        finally:
            cursor.close()
    
    def get_stats(self) -> dict:
        """Get memory statistics."""
        if self.use_postgres and self.conn:
            return self._get_stats_postgres()
        
        return {
            "total_tickets": len(self.tickets),
            "storage": "JSON (file-based)",
            "backend": "Local file system"
        }
    
    def _get_stats_postgres(self) -> dict:
        """Get stats from PostgreSQL."""
        if not self.conn:
            return {}
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM tickets")
            count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT priority, COUNT(*) 
                FROM tickets 
                GROUP BY priority
            """)
            priority_dist = dict(cursor.fetchall())
            
            return {
                "total_tickets": count,
                "storage": "PostgreSQL",
                "backend": "Relational database",
                "priority_distribution": priority_dist
            }
            
        except Exception as e:
            print(f"PostgreSQL stats error: {e}")
            return {}
        finally:
            cursor.close()
    
    def save_to_file(self) -> None:
        """Persist memory to JSON (backup)."""
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump(self.tickets, f, indent=2)
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def load_from_file(self) -> None:
        """Load tickets from JSON (for initialization)."""
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE) as f:
                    self.tickets = json.load(f)
            except Exception as e:
                print(f"Error loading JSON: {e}")
                self.tickets = []
    
    def __del__(self):
        """Close PostgreSQL connection on cleanup."""
        if self.conn:
            try:
                self.conn.close()
            except:
                pass


# Global instance
memory = MemorySystem()
