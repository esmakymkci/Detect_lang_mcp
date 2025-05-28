import requests
import json
from typing import Dict, List, Optional

class DetectLanguageAPI:
    """DetectLanguage API client for language detection"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://ws.detectlanguage.com/0.2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def detect_language(self, text: str) -> Dict:
        """
        Detect language of given text using DetectLanguage API
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Detection results with language, confidence, and reliability
        """
        if not text or not text.strip():
            return {
                "error": "Text cannot be empty",
                "success": False
            }
        
        try:
            # Prepare the request data
            data = {"q": text}
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/detect",
                headers=self.headers,
                data=data,
                timeout=10
            )
            
            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                
                # Extract detection data
                if "data" in result and "detections" in result["data"]:
                    detections = result["data"]["detections"]
                    
                    if detections and len(detections) > 0:
                        # Get the most confident detection
                        best_detection = detections[0]
                        
                        return {
                            "success": True,
                            "language": best_detection.get("language", "unknown"),
                            "confidence": best_detection.get("confidence", 0),
                            "is_reliable": best_detection.get("isReliable", False),
                            "text": text,
                            "all_detections": detections
                        }
                    else:
                        return {
                            "success": False,
                            "error": "No language detected",
                            "text": text
                        }
                else:
                    return {
                        "success": False,
                        "error": "Invalid API response format",
                        "text": text
                    }
            
            elif response.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid API key",
                    "status_code": response.status_code
                }
            
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "API rate limit exceeded",
                    "status_code": response.status_code
                }
            
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "status_code": response.status_code,
                    "response": response.text
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "API request timeout"
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error to DetectLanguage API"
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid JSON response from API"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

def detect_language(text: str, api_key: str = "ba3b71e93a655b554f1df2f4b2b1e82b") -> Dict:
    """
    Convenience function to detect language of text
    
    Args:
        text (str): Text to analyze
        api_key (str): DetectLanguage API key
        
    Returns:
        Dict: Detection results
    """
    detector = DetectLanguageAPI(api_key)
    return detector.detect_language(text)

if __name__ == "__main__":
    # Test the function
    test_texts = [
        "Hello, how are you today?",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "Merhaba, nasılsın?",
        "Привет, как дела?"
    ]
    
    for text in test_texts:
        result = detect_language(text)
        print(f"Text: {text}")
        print(f"Result: {result}")
        print("-" * 50)
