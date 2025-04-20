from agent_api.data.session_store import historial_responses
import agent_api.data.session_store as session_store

def olvidar_historial():
    """
    Olvida el historial de la conversación actual.
    """
    session_store.clear_responses()
    return "Historial olvidado."