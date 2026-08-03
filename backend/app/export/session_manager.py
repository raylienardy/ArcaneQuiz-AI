"""
Pengelola sesi ekspor in-memory.
"""

import uuid
import logging
from typing import Dict, Optional
from datetime import datetime, timezone
from .session import ExportSession, SessionStatus
from .models import ExportFormat, ExportMetadata

logger = logging.getLogger(__name__)

class ExportSessionManager:
    """Menyimpan dan mengelola sesi ekspor di memori."""

    def __init__(self):
        self._sessions: Dict[str, ExportSession] = {}

    def create_session(self, **kwargs) -> ExportSession:
        """Buat sesi baru."""
        session_id = kwargs.pop("session_id", str(uuid.uuid4()))
        session = ExportSession(
            session_id=session_id,
            status=SessionStatus.CREATED,
            created_at=datetime.now(timezone.utc).isoformat(),
            **kwargs,
        )
        self._sessions[session_id] = session
        logger.info(f"Export session {session_id} created.")
        return session

    def update_session(self, session_id: str, **kwargs) -> Optional[ExportSession]:
        """Perbarui atribut sesi."""
        session = self._sessions.get(session_id)
        if not session:
            logger.warning(f"Session {session_id} not found.")
            return None
        for key, value in kwargs.items():
            setattr(session, key, value)
        session.updated_at = datetime.now(timezone.utc).isoformat()
        self._sessions[session_id] = session
        logger.info(f"Session {session_id} updated: {kwargs.keys()}")
        return session

    def get_session(self, session_id: str) -> Optional[ExportSession]:
        return self._sessions.get(session_id)

    def close_session(self, session_id: str) -> Optional[ExportSession]:
        """Tutup sesi (status CLOSED)."""
        return self.update_session(session_id, status=SessionStatus.CLOSED, closed_at=datetime.now(timezone.utc).isoformat())

    def remove_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def active_sessions(self) -> Dict[str, ExportSession]:
        """Kembalikan semua sesi yang belum ditutup."""
        return {k: v for k, v in self._sessions.items() if v.status != SessionStatus.CLOSED}

# Instans global (singleton)
_session_manager = None

def get_session_manager() -> ExportSessionManager:
    global _session_manager
    if _session_manager is None:
        _session_manager = ExportSessionManager()
    return _session_manager