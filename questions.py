questions = { 
  "What is your name?": 
  "It is Arthur, King of the Britons.", 
  "What is your quest?": 
  "To seek the Holy Grail.", 
  "What is your favourite colour?": 
  "Blue.", 
  "What is the capital of Assyria?": 
  "I don't know that.", 
  "What is the air-speed velocity of an unladen swallow?": 
  "What do you mean? An African or European swallow?", 
} 
 
 
def answer(question): 
    a = list() 
    print("input: " + question)
    while True: 
        parts = question.partition('?') 
        part = parts[0].lstrip() + parts[1]
        question = parts[2]
        if part in questions: 
            print("Part : " + part)
            a.append(questions[part]) 
        if not question: 
            break 
    return ' '.join(a) 
