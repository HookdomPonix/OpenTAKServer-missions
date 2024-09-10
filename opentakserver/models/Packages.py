import base64
import hashlib
import os.path
from pathlib import Path

from bs4 import BeautifulSoup
from androguard.core.apk import APK

from werkzeug.utils import secure_filename

from sqlalchemy import Integer, String, BLOB, Boolean, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from flask import current_app as app, request

from opentakserver.extensions import db
from opentakserver.forms.package_form import PackageForm

from xml.etree.ElementTree import tostring


class Packages(db.Model):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[str] = mapped_column(String)
    plugin_type: Mapped[str] = mapped_column(String)
    package_name: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    file_name: Mapped[str] = mapped_column(String)
    version: Mapped[str] = mapped_column(String)
    revision_code: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(Integer, nullable=True)
    apk_hash: Mapped[str] = mapped_column(Integer, nullable=True)
    os_requirement: Mapped[str] = mapped_column(Integer, nullable=True)
    tak_prereq: Mapped[str] = mapped_column(Integer, nullable=True)
    file_size: Mapped[int] = mapped_column(Integer)
    icon: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    icon_filename: Mapped[str] = mapped_column(String, nullable=True)
    install_on_enrollment: Mapped[bool] = mapped_column(Boolean, default=False)
    install_on_connection: Mapped[bool] = mapped_column(Boolean, default=False)

    def from_wtform(self, form: PackageForm):
        self.platform = form.platform.data
        self.plugin_type = form.plugin_type.data
        self.file_name = secure_filename(form.apk.data.filename)
        apk = APK(os.path.join(app.config.get("OTS_DATA_FOLDER"), "packages", self.file_name))
        self.package_name = apk.get_package()
        self.version = apk.get_androidversion_name()
        self.revision_code = apk.get_androidversion_code()
        self.os_requirement = apk.get_min_sdk_version()
        self.name = apk.get_app_name()
        self.description = form.description.data
        self.apk_hash = hashlib.sha256(form.apk.data.stream.read()).hexdigest()
        self.file_size = Path(os.path.join(app.config.get("OTS_DATA_FOLDER"), "packages", self.file_name)).stat().st_size
        self.icon = request.files['icon'].stream.read() if 'icon' in request.files else None
        self.icon_filename = secure_filename(request.files['icon'].filename) if 'icon' in request.files else None
        self.install_on_enrollment = form.install_on_enrollment.data
        self.install_on_connection = form.install_on_connection.data

        manifest = BeautifulSoup(tostring(apk.get_android_manifest_xml()).decode('utf-8'))
        meta_data = manifest.find_all("meta-data", "lxml")
        for meta in meta_data:
            if 'ns0:value' not in meta.attrs or 'ns0:name' not in meta.attrs:
                continue

            if meta.attrs['ns0:name'] == "plugin-api":
                self.tak_prereq = meta.attrs['ns0:value']
                break

        if not self.icon:
            icon_filename, icon_extension = os.path.splitext(apk.get_app_icon())
            if icon_extension == '.png':
                self.icon = apk.get_file(apk.get_app_icon())
                self.icon_filename = f"{self.package_name}.png"

    def serialize(self):
        return {
            'platform': self.platform,
            'plugin_type': self.plugin_type,
            'package_name': self.package_name,
            'name': self.name,
            'file_name': self.file_name,
            'version': self.version,
            'revision_code': self.revision_code,
            'description': self.description,
            'apk_hash': self.apk_hash,
            'os_requirement': self.os_requirement,
            'tak_prereq': self.tak_prereq,
            'file_size': self.file_size,
            'icon': f"data:image/png;base64,{base64.b64encode(self.icon).decode('utf-8')}" if self.icon else None,
            'icon_filename': self.icon_filename,
            'install_on_enrollment': self.install_on_enrollment,
            'install_on_connection': self.install_on_connection
        }

    def to_json(self):
        return self.serialize()
