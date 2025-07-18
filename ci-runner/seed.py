#!/usr/local/bin/python
import sys
import base64
import os
import uuid
import yaml
import time
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from munch import munchify

if "/opt/sbs" not in sys.path:
    sys.path.insert(0, "/opt/sbs")

from server.db.audit_mixin import metadata
from server.db.db import db, db_migrations
from server.db.domain import (
    User, Organisation, OrganisationMembership, Service, Collaboration,
    CollaborationMembership, SshKey, Aup, SchacHomeOrganisation
)
from server.tools import read_file

config_file_location = os.environ.get("CONFIG", "config/config.yml")
config = munchify(yaml.load(read_file(config_file_location), Loader=yaml.FullLoader))

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = config.database.uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.db = db

Migrate(app, db)
result = None
with app.app_context():
    while result is None:
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
        except OperationalError:
            print("Waiting for the database...")
            time.sleep(1)
db_migrations(config.database.uri)


def read_image(file_name):
    file = f"/tmp/ci-runner/{file_name}"
    with open(file, "rb") as f:
        c = f.read()
        return base64.encodebytes(c).decode("utf-8")


def _persist(db, *objs):
    required_attrs = ["created_by", "updated_by"]
    for obj in objs:
        for attr in required_attrs:
            if hasattr(obj, attr):
                setattr(obj, attr, "urn:admin")
        if isinstance(obj, User):
            aup = Aup(au_version="1", user=obj)
            if not getattr(obj, "external_id"):
                setattr(obj, "external_id", str(uuid.uuid4()))
            db.session.add(aup)
        db.session.add(obj)
        print("Add", obj)


def clean_db(db):
    tables = reversed(metadata.sorted_tables)
    for table in tables:
        db.session.execute(table.delete())
    db.session.execute(text("DELETE FROM audit_logs"))
    db.session.commit()


roadrunner = read_image("roadrunner.png")

ci_org_name = "CI Test"
ci_org_description = "CI Test description"
ci_org_sho = "ci-runner.sram.surf.nl"
ci_org_shortname = "ci"
ci_org_uuid = str(uuid.uuid4())

admin_name = "Admin"
admin_uid = "98d4d0ddd179f57c0cbbf06ae2d7094522b21eab@acc.sram.eduteams.org"
admin_email = "admin@surf.nl"
admin_username = "admin"

student_name = "Student"
student_uid = "8e7811387bc200409b395a7a156826875a4248f9@acc.sram.eduteams.org"
student_email = "student@surf.nl"
student_username = "Student"

ci_rp_eid = "APP-B1F3C5AA-5514-48A9-BBA1-EBC388540BF7"
ci_rp_name = "CI RP"

ci_co_name = "CI CO"
ci_co_shortname = "cico"
ci_co_uuid = str(uuid.uuid4())
ci_co_description = "Test CO for Test RP"

# Clean
clean_db(db)

# Users

admin = User(
    uid=admin_uid,
    name=admin_name,
    email=admin_email,
    username=admin_username
)
student = User(
    uid=student_uid,
    name=student_name,
    email=student_email,
    username=student_username
)
_persist(db, admin, student)

ssh_key_admin = SshKey(
    user=admin,
    ssh_value="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDRa9pltI/Re4384pGFe0Kw1c"
              "tP83oLxmvFITcMLwDYYuVo7yzww1uumrYRmbfUNPdKsJEKjB9dGSeTFx3Lauzq"
              "yLcTdxpoFJh4p7cF3T3zbO4XTcmdnRALmjvxfAoSTtdWKtXeyNZmQCWKi5UQ84"
              "b/4sup5/yAUc7UyZJa9YqluBKEbhsemXD6aCHdOIIhySFXg7WyOLktyum+5v7o"
              "iwOBstajtKgu5G5JOVuA9+v6gLbdiU/TLINxgFu+sw5FtbNH6sYoWdiz36depO"
              "C1Kz5R1UhiWnQp8m1KNnOQACwu1a0WsucWWE5Mu1cgLWHE5ISc7I7NH8Jyg/dZ"
              "/IQaS2fe4XqSm89fELRspb+o1zAaLEmq+ed8/Alw6DSQ2gfdryBuv5APtxAmWr"
              "u/TnMPSbECkruNjDQk6PIdSorDfJ+d6mQURyq+zxgkbECCNiBspFCGDvTtaWf/"
              "JFkF7ySGPA9eL4l3Tz91pxXLB06wYQifFEm2eWZ3d+pK7Dx4oPiEuts= pubke"
              "y@ci-runner"
)
ssh_key_student = SshKey(
    user=student,
    ssh_value="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDRa9pltI/Re4384pGFe0Kw1c"
              "tP83oLxmvFITcMLwDYYuVo7yzww1uumrYRmbfUNPdKsJEKjB9dGSeTFx3Lauzq"
              "yLcTdxpoFJh4p7cF3T3zbO4XTcmdnRALmjvxfAoSTtdWKtXeyNZmQCWKi5UQ84"
              "b/4sup5/yAUc7UyZJa9YqluBKEbhsemXD6aCHdOIIhySFXg7WyOLktyum+5v7o"
              "iwOBstajtKgu5G5JOVuA9+v6gLbdiU/TLINxgFu+sw5FtbNH6sYoWdiz36depO"
              "C1Kz5R1UhiWnQp8m1KNnOQACwu1a0WsucWWE5Mu1cgLWHE5ISc7I7NH8Jyg/dZ"
              "/IQaS2fe4XqSm89fELRspb+o1zAaLEmq+ed8/Alw6DSQ2gfdryBuv5APtxAmWr"
              "u/TnMPSbECkruNjDQk6PIdSorDfJ+d6mQURyq+zxgkbECCNiBspFCGDvTtaWf/"
              "JFkF7ySGPA9eL4l3Tz91pxXLB06wYQifFEm2eWZ3d+pK7Dx4oPiEuts= pubke"
              "y@ci-runner"
)
_persist(db, ssh_key_admin, ssh_key_student)


# Organisation

ci_org = Organisation(
    name=ci_org_name,
    description=ci_org_description,
    identifier=ci_org_uuid,
    short_name=ci_org_shortname,
    logo=roadrunner,
    category="University"
)
_persist(db, ci_org)

ci_shoorg = SchacHomeOrganisation(
    name=ci_org_sho,
    organisation=ci_org
)
_persist(db, ci_shoorg)

ci_org_member_admin = OrganisationMembership(
    role="admin",
    user=admin,
    organisation=ci_org
)
_persist(db, ci_org_member_admin)


# Service
ci_rp = Service(
    entity_id=ci_rp_eid,
    name=ci_rp_name,
    contact_email=admin.email,
    automatic_connection_allowed=True,
    logo=roadrunner,
    # If we add aup, the user will see the aup screen in SBS
    #accepted_user_policy="https://google.nl",
    privacy_policy="https://google.nl",
    allowed_organisations=[ci_org],
    abbreviation="ci-org"
)

_persist(db, ci_rp)


#ipdb.set_trace()

# Collaboration
ci_co = Collaboration(
    name=ci_co_name,
    short_name=ci_co_shortname,
    identifier=ci_co_uuid,
    global_urn=f"ucc:{ci_co_shortname}",
    description=ci_co_description,
    logo=roadrunner,
    organisation=ci_org,
    services=[ci_rp],
    join_requests=[],
    invitations=[],
    website_url="https://www.google.nl",
    accepted_user_policy="https://www.google.nl",
    disclose_email_information=True,
    disclose_member_information=True,
)
_persist(db, ci_co)

admin_ci_co = CollaborationMembership(
    role="admin",
    user=admin,
    collaboration=ci_co
)
student_ci_co = CollaborationMembership(
    role="member",
    user=student,
    collaboration=ci_co
)
_persist(db, admin_ci_co, student_ci_co)

db.session.commit()
