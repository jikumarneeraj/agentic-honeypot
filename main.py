from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime
import time, requests

from agent.scam_detector import detect_scam
from agent.persona_agent import generate_reply
from agent.memory import get_session
from agent.policy import should_stop
from extractor.intelligence import extract_intelligence
from config.settings import API_KEY, GUVI_CALLBACK_URL

app = FastAPI(title="Agentic HoneyPot (GUVI)")


class Message(BaseModel):
    sender: str
    text: str
    timestamp: str


class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: list = []
    metadata: dict = {}


@app.post("/honeypot/receive")
def honeypot(data: IncomingRequest, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    session = get_session(data.sessionId)

    if not session["start_time"]:
        session["start_time"] = time.time()

    session["turns"] += 1

    detection = detect_scam(data.message.text)
    scam_detected = detection["is_scam"]

    extracted = extract_intelligence(data.message.text)
    for k in extracted:
        session["extracted"][k].extend(extracted[k])

    stop = False
    agent_reply = None

    if scam_detected:
        stop = should_stop(session)
        if stop:
            agent_reply = "Thank you."
            session["completed"] = True
        else:
            agent_reply = generate_reply(
                data.message.text,
                session["history"]
            )
            session["history"].append(
                {"role": "user", "content": data.message.text}
            )
            session["history"].append(
                {"role": "assistant", "content": agent_reply}
            )

    duration = int(time.time() - session["start_time"])

    if stop:
        payload = {
            "sessionId": data.sessionId,
            "scamDetected": True,
            "totalMessagesExchanged": session["turns"],
            "extractedIntelligence": session["extracted"],
            "agentNotes": "Urgency-based financial scam with payment redirection"
        }
        try:
            requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
        except Exception:
            pass

    return {
        "status": "success",
        "scamDetected": scam_detected,
        "agentReply": agent_reply,
        "engagementMetrics": {
            "engagementDurationSeconds": duration,
            "totalMessagesExchanged": session["turns"]
        },
        "extractedIntelligence": session["extracted"],
        "agentNotes": "Scammer used urgency and redirection tactics"
    }
