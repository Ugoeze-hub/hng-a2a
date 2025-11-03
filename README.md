 
# Fact Checker AI Agent

An intelligent fact-checking agent built for the HNG Stage 3 Backend Task. This agent verifies claims and statements using Google's Gemini AI and integrates seamlessly with Telex.im via the A2A (Agent-to-Agent) protocol.

## Features

- **Real-time Fact Checking**: Analyzes claims and provides verdicts (TRUE, FALSE, PARTIALLY TRUE, UNVERIFIABLE)
- **Confidence Scoring**: Includes confidence levels (High, Medium, Low) for each verdict
- **Source Citations**: Provides credible sources to support fact-check results
- **Context Awareness**: Highlights misconceptions, nuances, and time-sensitive information
- **A2A Protocol Integration**: Fully compatible with Telex.im messaging platform
- **Fast Response Times**: Powered by Gemini 2.5 Flash for quick analysis

## Live Demo

**Try it on Telex.im**: search for "Telex-gpt" (Although only available in the hng organization)

**API Endpoint**: `https://hng-a2a-ugoeze-hub7559-2ozzo1oj.leapcell.dev/a2a/factchecker`

**Health Check**: `https://hng-a2a-ugoeze-hub7559-2ozzo1oj.leapcell.dev/`

## Architecture
```
User → Telex.im → A2A Protocol (JSON-RPC 2.0) → FastAPI Agent → Gemini AI → Response
```

### Technology Stack

- **Backend**: FastAPI (Python 3.12+)
- **AI Model**: Google Gemini 2.5 Flash
- **Protocol**: A2A (Agent-to-Agent) via JSON-RPC 2.0
- **Deployment**: LeapCell

## Requirements

- Python 3.12+
- Gemini API Key

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ugoeze-hub/hng-a2a.git
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your Gemini API key from: https://ai.google.dev/gemini-api/docs/api-key

### 5. Run Locally
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at `http://localhost:8000`

## Testing

#### If using FastAPI, you can test with the docs
#### Testing with curl in your terminal also works
#### Postman can also be used when deployed


## How It Works

1. **User sends a claim** via Telex.im
2. **Telex forwards** the message to the agent using A2A protocol
3. **Agent extracts** the claim from the message
4. **Gemini AI analyzes** the claim with structured prompting
5. **Response includes**:
   - Verdict (TRUE/FALSE/PARTIALLY TRUE/UNVERIFIABLE)
   - Confidence level
   - Detailed explanation
   - Context and nuances
   - Credible sources
6. **Agent sends back** formatted response via A2A protocol
7. **User sees** the fact-check result on Telex


## Error Handling

The agent handles:
- ✅ Invalid JSON-RPC requests
- ✅ Missing or empty claims
- ✅ Gemini API failures
- ✅ Network timeouts
- ✅ Malformed A2A messages

All errors return proper JSON-RPC error responses with codes:
- `-32602`: Invalid params (no text content)
- `-32603`: Internal error (Gemini failure, etc.)

## Contributing

This is an HNG internship project. Contributions are welcome after the evaluation period.

## License

MIT License - see LICENSE file

## 👤 Author

**Your Name**
- GitHub: [Ugoeze-hub](https://github.com/ugoeze-hub)
- Twitter: [Ugoeze](https://x.com/ugo_the_xplorer)
- Email: eluchieugoeze@gmail.com

## Acknowledgments

- **HNG Internship** for the opportunity
- **Telex.im** for the A2A protocol platform
- **Google** for Gemini AI
- **FastAPI** community

## Resources

- [HNG Internship](https://hng.tech)
- [Telex.im](https://telex.im)
- [A2A Protocol Docs](https://docs.telex.im)
- [Gemini API Docs](https://ai.google.dev/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)

---

Built with ❤️ for HNG Stage 3 Backend Task
