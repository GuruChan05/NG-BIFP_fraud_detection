"""
Seed script for NG-BIFP Fraud Detection System.
Idempotent: only seeds when database is empty.
"""
import random
import uuid
from datetime import datetime, timedelta
from app.db.base import SessionLocal
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)


SEED_USERS = [
    {
        "email": "admin@ngbifp.com",
        "password": "Admin@123456",
        "username": "admin",
        "full_name": "System Administrator",
        "role": "admin",
        "is_admin": True,
        "department": "IT Security",
    },
    {
        "email": "analyst@ngbifp.com",
        "password": "Analyst@123456",
        "username": "analyst",
        "full_name": "Fraud Analyst",
        "role": "analyst",
        "is_admin": False,
        "department": "Fraud Analytics",
    },
    {
        "email": "demo@ngbifp.com",
        "password": "Demo@123456",
        "username": "demo",
        "full_name": "Demo User",
        "role": "user",
        "is_admin": False,
        "department": "General",
    },
]

MERCHANTS = [
    ("Amazon", "E-commerce"),
    ("Walmart", "Retail"),
    ("Starbucks", "Food & Beverage"),
    ("Netflix", "Entertainment"),
    ("Shell Gas Station", "Fuel"),
    ("CVS Pharmacy", "Healthcare"),
    ("Best Buy", "Electronics"),
    ("McDonald's", "Food & Beverage"),
    ("Home Depot", "Home Improvement"),
    ("Uber", "Transportation"),
    ("Unknown Merchant", "Unknown"),
    ("Crypto Exchange XYZ", "Cryptocurrency"),
    ("Foreign Wire Transfer", "Finance"),
    ("ATM Withdrawal", "Finance"),
    ("Online Gaming Store", "Entertainment"),
]

LOCATIONS = [
    "New York, USA", "Los Angeles, USA", "Chicago, USA",
    "Houston, USA", "London, UK", "Paris, France",
    "Tokyo, Japan", "Mumbai, India", "Sydney, Australia",
    "Unknown Location",
]


def seed_if_empty():
    """Seed the database only when the users table is empty."""
    from app.db.models.user import User
    from app.db.models.transaction import Transaction
    from app.db.models.notification import Notification
    from app.db.models.device import Device
    from app.db.models.role import Role

    db = SessionLocal()
    try:
        count = db.query(User).count()
        if count > 0:
            logger.info("Database already seeded — skipping.")
            return

        logger.info("Seeding database with demo data...")

        # ── 1. Create roles ──────────────────────────────────────────────────
        role_objects = {}
        for role_name in ("admin", "analyst", "user"):
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(
                    name=role_name,
                    description=f"{role_name.capitalize()} role",
                    is_system=True,
                )
                db.add(role)
            role_objects[role_name] = role
        db.flush()

        # ── 2. Create users ──────────────────────────────────────────────────
        created_users = []
        for u in SEED_USERS:
            user = User(
                email=u["email"],
                username=u["username"],
                full_name=u["full_name"],
                hashed_password=get_password_hash(u["password"]),
                is_active=True,
                is_admin=u["is_admin"],
                is_verified=True,
                department=u["department"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(user)
            db.flush()  # get the id

            # Assign role
            role = role_objects.get(u["role"])
            if role and role not in user.roles:
                user.roles.append(role)

            created_users.append(user)

        db.flush()

        # ── 3. Create devices (5 total, tied to admin user) ──────────────────
        admin_user = created_users[0]
        device_types = [
            ("mobile", "iOS 17", "Safari"),
            ("desktop", "Windows 11", "Chrome"),
            ("tablet", "Android 13", "Firefox"),
            ("desktop", "macOS 14", "Safari"),
            ("mobile", "Android 12", "Chrome"),
        ]
        for dtype, os_name, browser in device_types:
            dev = Device(
                device_id=str(uuid.uuid4()),
                user_id=admin_user.id,
                device_type=dtype,
                os=os_name,
                browser=browser,
                trust_score=round(random.uniform(0.6, 0.99), 2),
                is_trusted="trusted",
                last_seen=datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
                created_at=datetime.utcnow(),
            )
            db.add(dev)

        db.flush()

        # ── 4. Create transactions (50) ──────────────────────────────────────
        random.seed(42)
        transaction_ids = []
        for i in range(50):
            is_fraud = i < 10  # first 10 are fraudulent
            merchant, category = random.choice(MERCHANTS)
            if is_fraud:
                merchant = random.choice(
                    ["Unknown Merchant", "Crypto Exchange XYZ", "Foreign Wire Transfer"]
                )
                category = "Unknown"
            amount = round(random.uniform(10.0, 9999.99) if not is_fraud else random.uniform(500.0, 9999.99), 2)
            risk_score = round(random.uniform(0.7, 0.99) if is_fraud else random.uniform(0.01, 0.35), 4)
            txn = Transaction(
                user_id=admin_user.id,
                amount=amount,
                transaction_type=random.choice(["debit", "credit", "transfer"]),
                merchant=merchant,
                merchant_category=category,
                location=random.choice(LOCATIONS) if not is_fraud else "Unknown Location",
                device_id=str(uuid.uuid4()),
                risk_score=risk_score,
                is_fraudulent="fraudulent" if is_fraud else "legitimate",
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            )
            db.add(txn)
            db.flush()
            transaction_ids.append(txn.id)

        db.flush()

        # ── 5. Create notifications (10: 5 unread, 5 read) ───────────────────
        notif_data = [
            ("Fraud Alert", "Suspicious transaction detected on your account.", "alert", False, transaction_ids[0]),
            ("Login from new device", "A new login was detected from an unknown device.", "warning", False, None),
            ("High Risk Transaction", "A high-risk transaction was flagged for review.", "alert", False, transaction_ids[1]),
            ("Account Verified", "Your account has been successfully verified.", "success", False, None),
            ("Weekly Report Ready", "Your fraud detection report for this week is ready.", "info", False, None),
            ("Password Changed", "Your password was changed successfully.", "success", True, None),
            ("Transaction Completed", "Your transfer of $1,200 was completed.", "info", True, transaction_ids[10]),
            ("System Maintenance", "Scheduled maintenance on Saturday 2–4 AM UTC.", "info", True, None),
            ("New Feature Available", "Real-time fraud alerts are now available.", "info", True, None),
            ("Fraud Resolved", "The disputed transaction has been resolved in your favor.", "success", True, transaction_ids[2]),
        ]
        for title, message, ntype, is_read, txn_id in notif_data:
            notif = Notification(
                user_id=admin_user.id,
                title=title,
                message=message,
                notification_type=ntype,
                is_read=is_read,
                related_transaction_id=txn_id,
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 168)),
                updated_at=datetime.utcnow(),
            )
            db.add(notif)

        db.commit()
        logger.info(
            "✅ Seeding complete: %d users, 50 transactions, 10 notifications, 5 devices.",
            len(created_users),
        )

    except Exception as exc:
        db.rollback()
        logger.error("❌ Seeding failed: %s", exc, exc_info=True)
    finally:
        db.close()
