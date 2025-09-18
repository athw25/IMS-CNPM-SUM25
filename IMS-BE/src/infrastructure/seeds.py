from __future__ import annotations
import datetime as dt
from infrastructure.databases import db
from security.rbac import Roles
from utils.time import utcnow
from domain.models.identity import User, InternProfile
from domain.models.recruitment import RecruitmentCampaign, CampaignStatus, Application, ApplicationStatus
from domain.models.training import TrainingProgram, Project
from domain.models.assignment import Assignment, AssignmentStatus
from domain.models.evaluation import Evaluation
from domain.models.schedule import ScheduleItem, ScheduleType
from domain.models.kpi import KPIRecord
from domain.models.messaging import Notification, ChatThread, ChatMessage

def seed_demo():
    db.create_all()
    if not db.session.query(User.id).filter_by(email="admin@ims.local").first():
        admin = User(email="admin@ims.local", name="Admin Root", role=Roles.Admin); admin.set_password("password")
        hr = User(email="hr@ims.local", name="HR Manager", role=Roles.HR); hr.set_password("password")
        coord = User(email="coord@ims.local", name="Coordinator", role=Roles.Coordinator); coord.set_password("password")
        mentor = User(email="mentor@ims.local", name="Mentor One", role=Roles.Mentor); mentor.set_password("password")
        intern = User(email="intern@ims.local", name="Intern Demo", role=Roles.Intern); intern.set_password("password")
        db.session.add_all([admin, hr, coord, mentor, intern]); db.session.commit()

        ip = InternProfile(user_id=intern.id, school="Tech U", major="CS", gpa=3.5, status="Active",
                           start_date=dt.date.today(), end_date=dt.date.today() + dt.timedelta(days=90))
        ip.skills_json = '["python","sql"]'
        db.session.add(ip); db.session.commit()

        camp = RecruitmentCampaign(title="Fall Internship 2025", status=CampaignStatus.Open,
                                   description="Open hiring for interns", created_by=hr.id)
        db.session.add(camp); db.session.commit()
        app1 = Application(camp_id=camp.id, user_id=intern.id, status=ApplicationStatus.Pending, note="Excited to join")
        db.session.add(app1); db.session.commit()

        prog = TrainingProgram(title="Data Platform Intern Program", goal="Learn ETL, analytics", created_by=coord.id)
        db.session.add(prog); db.session.commit()
        proj = Project(prog_id=prog.id, title="Build ETL pipeline", description="From raw logs to warehouse", owner_id=mentor.id)
        db.session.add(proj); db.session.commit()
        asg = Assignment(proj_id=proj.id, intern_id=ip.id, status=AssignmentStatus.Pending,
                         due_date=dt.date.today() + dt.timedelta(days=14))
        db.session.add(asg); db.session.commit()

        ev = Evaluation(intern_id=ip.id, evaluator_id=mentor.id, score=85, comment="Good start")
        db.session.add(ev); db.session.commit()

        s1 = ScheduleItem(intern_id=ip.id, title="Onboarding", type=ScheduleType.Onboarding,
                          start_time=utcnow(), end_time=utcnow() + dt.timedelta(hours=2), location="HQ")
        s2 = ScheduleItem(intern_id=ip.id, title="Training: SQL 101", type=ScheduleType.Training,
                          start_time=utcnow() + dt.timedelta(days=1), end_time=utcnow() + dt.timedelta(days=1, hours=2), location="Lab A")
        db.session.add_all([s1, s2]); db.session.commit()

        k1 = KPIRecord(intern_id=ip.id, kpi_key="tasks_completed", value=3, period="month", note="Week 1 done")
        k2 = KPIRecord(intern_id=ip.id, kpi_key="bugs_reported", value=1, period="month", note="Minor defects")
        db.session.add_all([k1, k2]); db.session.commit()

        n1 = Notification(user_id=intern.id, type="welcome"); n1.set_payload({"msg": "Welcome to IMS!"})
        n2 = Notification(user_id=intern.id, type="reminder"); n2.set_payload({"msg": "Training tomorrow at 9am"})
        db.session.add_all([n1, n2]); db.session.commit()

        t = ChatThread(user_a_id=mentor.id, user_b_id=intern.id)
        db.session.add(t); db.session.commit()
        m1 = ChatMessage(thread_id=t.id, sender_id=mentor.id, content="Hi, welcome on board!")
        m2 = ChatMessage(thread_id=t.id, sender_id=intern.id, content="Thank you! Looking forward to learning.")
        db.session.add_all([m1, m2]); db.session.commit()
        print("Seeded demo data.")
    else:
        print("Seed already exists; skipping.")
