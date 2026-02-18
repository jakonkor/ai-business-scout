"""
GitHub Models API integration for free LLM access
Uses GitHub's AI models marketplace with personal access token
"""

import os
from typing import Optional, List, Dict, Any
from openai import OpenAI


class GitHubLLM:
    """
    Wrapper for GitHub Models API.
    Provides access to various LLMs including GPT-4o, Claude, Llama, etc.
    
    Available models:
    - gpt-4o (OpenAI)
    - gpt-4o-mini (OpenAI)
    - claude-3.5-sonnet (Anthropic)
    - llama-3.1-405b (Meta)
    - mistral-large (Mistral)
    - phi-3 (Microsoft)
    """
    
    def __init__(self, token: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize GitHub Models API client.
        
        Args:
            token: GitHub personal access token
            model: Model to use (default: gpt-4o-mini for speed/cost)
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError(
                "GitHub token required. Set GITHUB_TOKEN environment variable or pass token parameter.\n"
                "Get a token at: https://github.com/settings/tokens"
            )
        
        self.model = model
        
        # Initialize OpenAI client pointing to GitHub
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=self.token,
        )
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate text using GitHub Models API.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"❌ Error calling GitHub Models API: {e}")
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate JSON response using GitHub Models API.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
        
        Returns:
            Parsed JSON response
        """
        import json
        
        if system_prompt:
            system_prompt += "\n\nRespond ONLY with valid JSON. No markdown, no explanations."
        else:
            system_prompt = "Respond ONLY with valid JSON. No markdown, no explanations."
        
        response_text = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=2000,
        )
        
        # Clean up response (remove markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            print(f"Response: {response_text[:200]}...")
            raise


async def main():
    """Test GitHub Models API"""
    import asyncio
    
    llm = GitHubLLM()
    
    print("Testing GitHub Models API...")
    print(f"Using model: {llm.model}\n")
    
    # Test simple generation
    response = await llm.generate(
        prompt="What are 3 trending technologies in 2024?",
        system_prompt="You are a tech trend analyst. Be concise.",
    )
    
    print("Response:")
    print(response)
    
    print("\n" + "="*60 + "\n")
    
    # Test JSON generation
    json_response = await llm.generate_json(
        prompt="Generate a business idea in the AI space",
        system_prompt="You are a business consultant. Return a JSON object with: title, description, target_market",
    )
    
    print("JSON Response:")
    import json
    print(json.dumps(json_response, indent=2))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
