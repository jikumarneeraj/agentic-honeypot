from fastapi import FastAPI, Header, HTTPException, Request
import time
import requests

from agent.scam_detector import detect_scam
from agent.persona_agent import generate_reply
from agent.memory import get_session
from agent.policy import should_stop
from extractor.intelligence import extract_intelligence
from config.settings import API_KEY, GUVI_CALLBACK_URL

app = FastAPI(title="Agentic HoneyPot (GUVI)")


@app.api_route("/honeypot/receive", methods=["GET", "POST"])
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # -------------------------------------------------
    # 1️⃣ API KEY AUTH (MANDATORY)
    # -------------------------------------------------
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # -------------------------------------------------
    # 2️⃣ SAFE BODY PARSING (GUVI TESTER SAFE)
    # -------------------------------------------------
    body = {}

    if request.method == "POST":
        try:
            parsed = await request.json()
            if isinstance(parsed, dict):
                body = parsed
        except Exception:
            body = {}

    # -------------------------------------------------
    # 3️⃣ SAFE DEFAULT VALUES
    # -------------------------------------------------
    session_id = body.get("sessionId", "guvi-test-session")

    message_text = ""
    if isinstance(body.get("message"), dict):
        message_text = body["message"].get("text", "")

    # -------------------------------------------------
    # 4️⃣ SESSION MANAGEMENT
    # -------------------------------------------------
    session = get_session(session_id)

    if not session["start_time"]:
        session["start_time"] = time.time()

    session["turns"] += 1

    # -------------------------------------------------
    # 5️⃣ SCAM DETECTION
    # -------------------------------------------------
    detection = detect_scam(message_text)
    scam_detected = detection.get("is_scam", False)

    # -------------------------------------------------
    # 6️⃣ INTELLIGENCE EXTRACTION
    # -------------------------------------------------
    extracted = extract_intelligence(message_text)
    for k in extracted:
        session["extracted"][k].extend(extracted[k])

    # -------------------------------------------------
    # 7️⃣ AGENTIC ENGAGEMENT
    # -------------------------------------------------
    agent_reply = "Thank you."
    stop = False

    if scam_detected:
        stop = should_stop(session)

        if not stop:
            agent_reply = generate_reply(
                message_text,
                session["history"]
            )

            session["history"].append(
                {"role": "user", "content": message_text}
            )
            session["history"].append(
                {"role": "assistant", "content": agent_reply}
            )
        else:
            session["completed"] = True

    # -------------------------------------------------
    # 8️⃣ METRICS
    # -------------------------------------------------
    duration = int(time.time() - session["start_time"])

    # -------------------------------------------------
    # 9️⃣ GUVI FINAL CALLBACK (ONLY WHEN STOPPED)
    # -------------------------------------------------
    if stop:
        payload = {
            "sessionId": session_id,
            "scamDetected": True,
            "totalMessagesExchanged": session["turns"],
            "extractedIntelligence": session["extracted"],
            "agentNotes": "Urgency-based financial scam with payment redirection"
        }

        try:
            requests.post(
                GUVI_CALLBACK_URL,
                json=payload,
                timeout=5
            )
        except Exception:
            pass

    # -------------------------------------------------
    # 🔟 FINAL RESPONSE (GUVI VALID)
    # -------------------------------------------------
    return {
        "status": "success",
        "scamDetected": scam_detected,
        "agentReply": agent_reply,
        "engagementMetrics": {
            "engagementDurationSeconds": duration,
            "totalMessagesExchanged": session["turns"]
        },
        "extractedIntelligence": session["extracted"],
        "agentNotes": "GUVI endpoint tester validation response"
    }
