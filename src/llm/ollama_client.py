"""
Ollama LLM client for local language model inference
"""
from typing import Optional, List, Dict, Any, Generator
import requests
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """Client for interacting with Ollama LLM"""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral",
        temperature: float = 0.7,
        timeout: int = 60
    ):
        """
        Initialize Ollama client

        Args:
            base_url: Ollama API base URL
            model: Model name to use
            temperature: Sampling temperature (0.0 to 1.0)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
        self.timeout = timeout

        logger.info(f"Initialized Ollama client: {base_url}, model: {model}")

    def is_available(self) -> bool:
        """
        Check if Ollama service is available

        Returns:
            True if service is reachable
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama service not available: {e}")
            return False

    def list_models(self) -> List[str]:
        """
        List available models

        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            logger.info(f"Available models: {models}")
            return models
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> str:
        """
        Generate text from prompt

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt for context
            temperature: Override default temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            Generated text
        """
        if not self.is_available():
            raise ConnectionError("Ollama service is not available")

        # Build request payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature if temperature is not None else self.temperature
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        logger.info(f"Generating response for prompt (length: {len(prompt)} chars)")

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                stream=stream
            )
            response.raise_for_status()

            if stream:
                # Handle streaming response
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        import json
                        chunk = json.loads(line)
                        if "response" in chunk:
                            full_response += chunk["response"]
                return full_response
            else:
                # Handle non-streaming response
                data = response.json()
                generated_text = data.get("response", "")
                logger.info(f"Generated response (length: {len(generated_text)} chars)")
                return generated_text

        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise TimeoutError("Ollama request timed out")
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        stream: bool = False
    ) -> str:
        """
        Chat completion with conversation history

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            stream: Whether to stream the response

        Returns:
            Generated response
        """
        if not self.is_available():
            raise ConnectionError("Ollama service is not available")

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature if temperature is not None else self.temperature
            }
        }

        logger.info(f"Chat completion with {len(messages)} messages")

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout,
                stream=stream
            )
            response.raise_for_status()

            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        import json
                        chunk = json.loads(line)
                        if "message" in chunk and "content" in chunk["message"]:
                            full_response += chunk["message"]["content"]
                return full_response
            else:
                data = response.json()
                return data.get("message", {}).get("content", "")

        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise


# Global Ollama client instance
_ollama_client = None


def get_ollama_client(
    base_url: str = "http://localhost:11434",
    model: str = "mistral"
) -> OllamaClient:
    """
    Get or create global Ollama client instance

    Args:
        base_url: Ollama API base URL
        model: Model name to use

    Returns:
        OllamaClient instance
    """
    global _ollama_client

    if _ollama_client is None:
        _ollama_client = OllamaClient(base_url=base_url, model=model)

    return _ollama_client


__all__ = ["OllamaClient", "get_ollama_client"]
