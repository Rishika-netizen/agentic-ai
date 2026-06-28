from session_manager import SessionManager

manager = SessionManager()

print(
    manager.get_session("C001")
)