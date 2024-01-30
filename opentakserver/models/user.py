from dataclasses import dataclass

from opentakserver.extensions import db
from sqlalchemy import String
from flask_security.models import fsqla_v3 as fsqla
from sqlalchemy.orm import relationship


@dataclass
class User(db.Model, fsqla.FsUserMixin):
    email = db.Column(String, nullable=True)
    video_streams = relationship("VideoStream", back_populates="user")
    euds = relationship("EUD", back_populates="user")

    def serialize(self):
        return {
            'username': self.username,
            'active': self.active,
            'last_login_at': self.last_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_at': self.current_login_at,
            'current_login_ip': self.current_login_ip,
            'email': self.email,
            'login_count': self.login_count,
            'euds': [eud.serialize() for eud in self.euds],
            'video_streams': [v.serialize() for v in self.video_streams],
            'roles': [role.serialize() for role in self.roles]
        }

    def to_json(self):
        return self.serialize()
