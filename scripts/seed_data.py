#!/usr/bin/env python3
"""
Seed script to populate SkillUp database with initial skills and test users.
Run this after the app is running to add sample data.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine
from app.models.base import Base
from app.models.skill import Skill
from app.models.user import User, UserRole
from app.core.security import get_password_hash

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # List of Algerian skills/professions to seed
    skills_data = [
        {
            "name": "الكهرباء",
            "description": "تدريب في مجال الكهرباء والأسلاك والتجهيزات الكهربائية"
        },
        {
            "name": "النجارة",
            "description": "تدريب في مجال النجارة وتشغيل الخشب والتنجيد"
        },
        {
            "name": "الميكانيك",
            "description": "تدريب في مجال إصلاح السيارات والآلات والمحركات"
        },
        {
            "name": "التبريد والتكييف",
            "description": "تدريب في تركيب وصيانة أنظمة التبريد والتكييف"
        },
        {
            "name": "الخياطة",
            "description": "تدريب في فن الخياطة والتفصيل والتطريز"
        },
        {
            "name": "الطبخ والحلويات",
            "description": "تدريب في فنون الطهي والخبز والحلويات التقليدية"
        },
        {
            "name": "التصميم الجرافيكي",
            "description": "تدريب في التصميم الجرافيكي واستخدام برامج التصميم"
        },
        {
            "name": "البرمجة",
            "description": "تدريب في البرمجة وتطوير التطبيقات والويب"
        },
        {
            "name": "الحدادة",
            "description": "تدريب في الحدادة وتشكيل المعادن والتصنيع"
        },
        {
            "name": "البناء والعمارة",
            "description": "تدريب في البناء والهندسة المعمارية والرسم الهندسي"
        },
        {
            "name": "التجميل والعناية",
            "description": "تدريب في فنون التجميل والعناية بالشعر والجسم"
        },
        {
            "name": "الحرف اليدوية",
            "description": "تدريب في الحرف اليدوية والتقليدية والصناعات الصغيرة"
        },
    ]

    # Add skills if they don't exist
    print("🔧 إضافة المهارات...")
    for skill_data in skills_data:
        existing_skill = db.query(Skill).filter(Skill.name == skill_data["name"]).first()
        if not existing_skill:
            skill = Skill(
                name=skill_data["name"],
                description=skill_data["description"]
            )
            db.add(skill)
            print(f"  ✓ {skill_data['name']}")
    
    db.commit()
    print(f"✅ تم إضافة {len(skills_data)} مهارة بنجاح!\n")

    # Create test users if they don't exist
    print("👥 إضافة حسابات اختبار...")
    
    test_users = [
        {
            "email": "youcef@skillup.dz",
            "full_name": "يوسف محمودي",
            "password": "Demo@2025",
            "phone": "0661234567",
            "role": UserRole.TRAINEE.value
        },
        {
            "email": "fatima@skillup.dz",
            "full_name": "فاطمة حسن",
            "password": "Demo@2025",
            "phone": "0561234567",
            "role": UserRole.TRAINER.value
        },
    ]

    for user_data in test_users:
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if not existing_user:
            user = User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                password_hash=get_password_hash(user_data["password"]),
                phone=user_data["phone"],
                role=user_data["role"]
            )
            db.add(user)
            print(f"  ✓ {user_data['full_name']} ({user_data['email']})")
    
    db.commit()
    print("✅ تم إضافة حسابات الاختبار بنجاح!\n")

    print("=" * 50)
    print("🎉 تم إكمال عملية إضافة البيانات الأولية!")
    print("=" * 50)
    print("\nحسابات اختبار:")
    print("  📧 متدرب: youcef@skillup.dz / Demo@2025")
    print("  📧 مدرب:  fatima@skillup.dz / Demo@2025")
    print("\nالخطوة التالية: اذهب إلى http://localhost:8000\n")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
    db.rollback()
    sys.exit(1)

finally:
    db.close()
