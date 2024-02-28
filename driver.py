import os
from docx import Document
from openai import OpenAI
client = OpenAI()
import model_config

def fetch_result(name, week):
    path = f'./week_{week}/{name}.docx'

    if not os.path.exists(path):
        print(f"No document found for {name} in week {week}.")
        return
    try:
        doc = Document(path)
        content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return content
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return 

def generate_feedback(content):
    if not content:
        print("No content found.")
        return
    
    
    response = client.chat.completions.create(model="gpt-4-0125-preview",
                                              messages=[
                                                        {"role": "system", "content": model_config.feedback_guide},
                                                        {"role": "system", "content": model_config.instructions},
                                                        {"role": "user", "content": f"Provide feedback for the student's performance in the quiz.\n{content}"}
                                                        ]
                                            )
    
    return response.choices[0].message.content
    


if __name__ == "__main__":
    student_name = input("Please enter the student's name: ")
    week_number = input("Please enter the week number you want insights from: ")
    print("Fetching results for " + student_name + " for week " + week_number + "...")
    content = fetch_result(student_name, week_number)
    print("Generating insights for " + student_name + " for week " + week_number + "...")
    feedback = generate_feedback(content)
    print(feedback)