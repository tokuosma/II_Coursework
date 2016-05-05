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
    while True: 
        parts = question.partition('?') 
        part = (parts[0].strip() + parts[1].strip()).replace("\x00", "")
        question = parts[2]
        if part in questions: 
            a.append(questions[part]) 
        else:
            if part:
                raise QuestionNotFoundException("Question not found!")
        if not question: 
            break 
    return ' '.join(a) 

class QuestionNotFoundException(Exception):
    def __init__(self, message):
        self.message = message

