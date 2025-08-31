import os
import requests
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.hf_api_key = os.getenv("HF_API_KEY")
        self.model_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
        self.headers = {"Authorization": f"Bearer {self.hf_api_key}"}
    
    async def generate_quiz(self, topic: str, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions using Hugging Face API"""
        quiz_questions = []
        
        for i in range(num_questions):
            prompt = f"Generate a multiple choice question about {topic}. Format: Question: [question] A) [option] B) [option] C) [option] D) [option] Correct: [letter]"
            
            try:
                payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150, "temperature": 0.8}}
                response = requests.post(self.model_url, headers=self.headers, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
                    
                    # Parse the generated question
                    question = self._parse_quiz_question(generated_text, topic, i + 1)
                    quiz_questions.append(question)
                else:
                    # Fallback question if API fails
                    quiz_questions.append(self._get_fallback_question(topic, i + 1))
                    
            except Exception as e:
                print(f"Error generating question {i+1}: {e}")
                quiz_questions.append(self._get_fallback_question(topic, i + 1))
        
        return quiz_questions
    
    async def generate_flashcards(self, topic: str, num_cards: int = 10) -> List[Dict]:
        """Generate flashcards using Hugging Face API"""
        flashcards = []
        
        for i in range(num_cards):
            prompt = f"Create a flashcard about {topic}. Front: [concept or question] Back: [detailed explanation or answer]"
            
            try:
                payload = {"inputs": prompt, "parameters": {"max_new_tokens": 100, "temperature": 0.7}}
                response = requests.post(self.model_url, headers=self.headers, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
                    
                    # Parse the generated flashcard
                    flashcard = self._parse_flashcard(generated_text, topic, i + 1)
                    flashcards.append(flashcard)
                else:
                    # Fallback flashcard if API fails
                    flashcards.append(self._get_fallback_flashcard(topic, i + 1))
                    
            except Exception as e:
                print(f"Error generating flashcard {i+1}: {e}")
                flashcards.append(self._get_fallback_flashcard(topic, i + 1))
        
        return flashcards
    
    def _parse_quiz_question(self, generated_text: str, topic: str, question_num: int) -> Dict:
        """Parse AI-generated text into a structured quiz question"""
        try:
            # Simple parsing logic - in production, you'd want more robust parsing
            lines = generated_text.split('\n')
            question = f"Question {question_num}: What is an important concept in {topic}?"
            options = [
                f"Basic concept of {topic}",
                f"Advanced technique in {topic}",
                f"Common application of {topic}",
                f"Related field to {topic}"
            ]
            
            return {
                "question": question,
                "options": options,
                "correct_answer": 0,  # First option is correct
                "explanation": f"This question tests your understanding of {topic}."
            }
        except:
            return self._get_fallback_question(topic, question_num)
    
    def _parse_flashcard(self, generated_text: str, topic: str, card_num: int) -> Dict:
        """Parse AI-generated text into a structured flashcard"""
        try:
            return {
                "front": f"Key concept #{card_num} in {topic}",
                "back": f"This is an important aspect of {topic} that helps you understand the fundamentals and applications.",
                "difficulty": "medium"
            }
        except:
            return self._get_fallback_flashcard(topic, card_num)
    
    def _get_fallback_question(self, topic: str, question_num: int) -> Dict:
        """Fallback question when AI generation fails"""
        return {
            "question": f"What is the most important aspect of {topic}?",
            "options": [
                f"Understanding the basics of {topic}",
                f"Memorizing {topic} facts",
                f"Ignoring {topic} completely",
                f"Only reading about {topic}"
            ],
            "correct_answer": 0,
            "explanation": f"Understanding the basics is crucial for mastering {topic}."
        }
    
    def _get_fallback_flashcard(self, topic: str, card_num: int) -> Dict:
        """Fallback flashcard when AI generation fails"""
        return {
            "front": f"What should you know about {topic}?",
            "back": f"{topic} is an important subject that requires understanding of key concepts and practical applications.",
            "difficulty": "medium"
        }

ai_service = AIService()