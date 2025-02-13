import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class Character(BaseModel):
	question: str
	fact: str = Field(..., description="Give the answer to the question being asked")

def get_answer_groq(question):
	client = Groq(
		api_key=os.environ.get('GROQ_API_KEY'),
	)

	client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)
	
	resp = client.chat.completions.create(
		model="mixtral-8x7b-32768",
		messages=[
			{	"role": "user",
				"content": question,
			
			}
		],
		response_model=Character,
	)

	return resp

def main():
	while True:
		user_input = input("What do you want to know?: ")
	
		if user_input == "quit":
			return

		answer = get_answer_groq(user_input)
		
		if not answer.fact:
			print("Try to rephrase your question...")
		elif answer.fact:
			print(f"{answer.fact}\n")

if __name__ == "__main__":
	main()
	
