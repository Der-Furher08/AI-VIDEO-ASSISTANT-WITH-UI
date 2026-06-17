from dotenv import load_dotenv
load_dotenv()
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize,generate_title
from core.extractor import extract_action_items,extract_key_decisions,extract_questions



source = "https://youtu.be/i9hf6frkd08?si=c5RHc3qqxDU2YjxK"
language = "english"

chunks = process_input(source)

transcript = transcribe_all(chunks,language=language)
print("\n"+ "="*60 )
print("\n==== TRANSCRIPT === \n")
print(transcript)
print("="*60)
print(transcript[:500] + "..." if len(transcript)>500 else transcript)

title = generate_title(transcript)
summary = summarize(transcript)

print("\n"+ "="*60 )
print(f" TITLE : {title}")
print("\n"+ "="*60 )
print("\n SUMMARY")
print("-"*60 )
print(summary)

action_items = extract_action_items(transcript)
decisions = extract_key_decisions(transcript)
questions = extract_questions(transcript)

print("\n"+ "="*60 )
print("\n ACTION ITEMS")
print("-"*60 )
print(action_items)

print("\n"+ "="*60 )
print("\n KEY DECISIONS")
print("-"*60 )
print(decisions)

print("\n"+ "="*60 )
print("\n OPEN QUESTIONS")
print("-"*60 )
print(questions)


