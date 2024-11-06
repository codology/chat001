import anthropic


class ClaudeModels:
    # legacy models
    LEGACY_CLAUDE_2 = "claude-2.0"
    LEGACY_CLAUDE_2_1 = "claude-2.1"
    LEGACY_CLAUDE_INSTANT_1_2 = "claude-instant-1.2"

    # latest
    SONNET_35_LATEST = "claude-3-5-sonnet-latest"
    SONNET_35 = "claude-3-5-sonnet-20241022"
    SONNET_3 = "claude-3-sonnet-20240229"
    OPUS_3 = "claude-3-opus-20240229"
    HAIKU_3 = "claude-3-haiku-20240307"


class ClaudeApi:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.client = anthropic.Anthropic(api_key=api_key)
        self.response = []

    def _query(self, prompt, max_tokens=2000, temperature=0):
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            system="Respond only from the context given in the document. if you do not find the asnwer in the document keep quiet.",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": f"{prompt}"}],
                }
            ],
        )
        self.response = message
    
    def query_document(self, document: str, prompt:str, chunk=None):
        doc_prompt = f"Given this document, <document>{document}</document>."
        if chunk:
            doc_prompt += f" <chunk>{chunk}</chunk>"
        doc_prompt += prompt
        self._query(doc_prompt)

    def _parse_response(self):
        return "\n".join([k.text for k in self.response.content])

    def get_response(self):
        return self._parse_response()
