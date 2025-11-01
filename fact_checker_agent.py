import google.generativeai as genai
import os
# from dotenv import load_dotenv

# load_dotenv()

class FactCheckerAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not sey")
        
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            tools='google_search' 
        )

    async def check_fact(self, claim: str):
        prompt = f"""You are an expert fact-checker. Analyze this claim using web search:

            Claim: "{claim}"

            Please provide:

            1. **Verdict**: 
            - ✅ TRUE
            - ❌ FALSE  
            - ⚠️ PARTIALLY TRUE
            - ❓ UNVERIFIABLE

            2. **Confidence Level**: High / Medium / Low

            3. **Explanation** (2-4 sentences):
            - What does the evidence show?
            - Why is this the verdict?

            4. **Key Context** (if relevant):
                - Important nuances
            - Common misconceptions
            - Date/time relevance

            5. **Sources**: List credible sources you found

            Be objective, factual, and cite your sources."""
        
        try:
            response = self.model.generate_content(prompt)
            analysis = response.text
                
            final_response = f"## 🔍 Fact Check Results\n\n"
            final_response += f"**Claim:** _{claim}_\n\n"
            final_response += "---\n\n"
            final_response += analysis
            
            return final_response
        
        except Exception as e:
            return f"**Error during fact-checking:** {str(e)}\n\nPlease try again or rephrase your claim."
