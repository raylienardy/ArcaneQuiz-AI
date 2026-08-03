import pytest
from app.export.session_manager import get_session_manager, ExportSessionManager
from app.export.session import SessionStatus, ExportSession

class TestExportSessionManager:
    def test_create_session(self, clean_session_manager):
        mgr = clean_session_manager
        session = mgr.create_session(export_format="pdf", question_count=10)
        assert session.session_id is not None
        assert session.status == SessionStatus.CREATED
        assert session.question_count == 10

    def test_update_session_status(self, clean_session_manager):
        mgr = clean_session_manager
        session = mgr.create_session(export_format="pdf")
        updated = mgr.update_session(session.session_id, status=SessionStatus.PREVIEW_READY)
        assert updated.status == SessionStatus.PREVIEW_READY

    def test_close_session(self, clean_session_manager):
        mgr = clean_session_manager
        session = mgr.create_session(export_format="pdf")
        closed = mgr.close_session(session.session_id)
        assert closed.status == SessionStatus.CLOSED
        assert closed.closed_at is not None

    def test_get_nonexistent_session(self, clean_session_manager):
        mgr = clean_session_manager
        assert mgr.get_session("nonexistent") is None

    def test_active_sessions(self, clean_session_manager):
        mgr = clean_session_manager
        s1 = mgr.create_session(export_format="pdf")
        s2 = mgr.create_session(export_format="csv")
        mgr.close_session(s1.session_id)
        active = mgr.active_sessions()
        assert len(active) == 1
        assert s2.session_id in active