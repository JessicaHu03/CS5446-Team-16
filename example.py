import openai
import time
import json


dialogue_history_list = [{"role": "user", "content": "Hi, how can I assist you today?"}]
# messages role contains system, user, assistant. system == instruction, user == user, assistant == gpt


def simulate_patient(dialogue_history):
    instruction = """Task Description:
You are tasked with simulating a conversation between a patient and a doctor. Your role is to play the patient, who is experiencing anxiety due to symptoms or a recent diagnosis related to [**disease**]. You should start the conversation by expressing your concerns— either describing recent symptoms or seeking advice after being diagnosed with the disease. Feel free to use the provided knowledge about hypertension to inform your responses. The conversation should flow naturally, reflecting a typical patient-doctor interaction. You should reply no more than 30 words.

Response Format:
Please return your responses in the following JSON format: { "content": "Your simulated patient response here" }
content: The simulated patient's dialogue.
"""
    messages = [{
        "role": "system",
        "content": instruction
    }] + dialogue_history_list
    while True:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.7,
                timeout=30,
                messages=messages,
                response_format={ "type": "json_object" }
            )
            content = response.choices[0].message.content
            content = json.loads(content)
            return content
        except Exception as e:
            print(e)
            time.sleep(0.5)

