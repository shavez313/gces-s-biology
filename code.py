import pyttsx3
import pygame
import time
import random

# --- Configuration ---
STAY_FOCUSED_INTERVAL = 3  # Remind Jackson to stay focused every X questions
SOUND_EFFECTS_ENABLED = True # Set to False if you don't have sound files

# --- Initialize Text-to-Speech ---
tts_engine = pyttsx3.init()
# You can adjust voice properties if needed
# voices = tts_engine.getProperty('voices')
# tts_engine.setProperty('voice', voices[1].id) # Example: use a female voice if available
tts_engine.setProperty('rate', 150) # Speed of speech

def speak(text):
    print(f"📢: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

# --- Initialize Pygame Mixer for Sound Effects ---
if SOUND_EFFECTS_ENABLED:
    try:
        pygame.mixer.init()
        correct_sound = pygame.mixer.Sound("correct.wav")
        incorrect_sound = pygame.mixer.Sound("incorrect.wav")
    except pygame.error as e:
        print(f"Warning: Could not load sound effects: {e}")
        print("Make sure 'correct.wav' and 'incorrect.wav' are in the same directory as the script.")
        print("Continuing without sound effects.")
        SOUND_EFFECTS_ENABLED = False

def play_sound(sound_type):
    if SOUND_EFFECTS_ENABLED:
        if sound_type == "correct" and 'correct_sound' in globals():
            correct_sound.play()
        elif sound_type == "incorrect" and 'incorrect_sound' in globals():
            incorrect_sound.play()

# --- Quiz Questions ---
# Extracted from the provided mark scheme
# Note: For "Any X from", the quiz will list options.
# For calculations, it will expect the final answer.
# For QWC, it will list indicative content.

questions_data = [
    {
        "id": "1a_i",
        "question": "1. (a) (i) Which mineral shows the greatest variation in content between the three types of slurry (Table 1 in your exam paper)?",
        "answer": "Nitrogen",
        "marks": 1
    },
    {
        "id": "1a_ii",
        "question": "1. (a) (ii) Suggest why there is a large variation in the content of this mineral (Nitrogen) in the three types of slurry.",
        "answer": "Different diet/different foods eaten", # Accepts either
        "marks": 1,
        "keywords": ["diet", "foods", "eaten"] # For more flexible checking
    },
    {
        "id": "1b",
        "question": "1. (b) Which type of slurry would be best for growing rice? Use evidence from both tables to support your answer (Tables 1 & 2 in your exam paper).",
        "answer": "Chicken; contains most nitrogen/rice needs most nitrogen", # Key points
        "marks": 2,
        "keywords": ["chicken", "most nitrogen", "rice needs nitrogen"]
    },
    {
        "id": "1c",
        "question": "1. (c) Give the function of nitrogen in the growth of plants.",
        "answer": "Needed to make amino acids/proteins",
        "marks": 1,
        "keywords": ["amino acids", "proteins"]
    },
    {
        "id": "2a",
        "question": "2. (a) Give the trophic level of the tadpoles (refer to food chain diagram in your exam paper).",
        "answer": "2",
        "marks": 1
    },
    {
        "id": "2b",
        "question": "2. (b) Name the secondary consumer in this food chain (refer to food chain diagram).",
        "answer": "Small fish",
        "marks": 1
    },
    {
        "id": "2c_i",
        "question": "2. (c) (i) Calculate the energy lost between the small fish (1600 kJ) and the large fish (75 kJ).",
        "answer": "1525", # 1600 - 75
        "marks": 2
    },
    {
        "id": "2c_ii",
        "question": "2. (c) (ii) Give two ways this energy is lost from the food chain. (List two)",
        "answer": ["excretion", "movement", "heat/respiration", "inedible parts"], # Any two from this list
        "marks": 2,
        "type": "any_x_from",
        "num_required": 2
    },
    {
        "id": "2d_i",
        "question": "2. (d) (i) Calculate the % efficiency of energy transfer from water weeds (90000 kJ) to tadpoles (15000 kJ). Give your answer to one decimal place. ((15000 / 90000) * 100)",
        "answer": "16.7", # or 16.66 - allow some flexibility
        "marks": 3,
        "allow_range": ["16.6", "16.7"] # Accept 16.6 or 16.7 due to rounding
    },
    {
        "id": "2d_ii",
        "question": "2. (d) (ii) Suggest why there is not another trophic level (5th) in this food chain.",
        "answer": "Not enough energy remaining to support a 5th trophic level",
        "marks": 1,
        "keywords": ["not enough energy", "support", "5th trophic level", "remaining"]
    },
    {
        "id": "3a",
        "question": "3. (a) Name the growing points of plants which contain stem cells.",
        "answer": "Meristems/apices",
        "marks": 1,
        "keywords": ["meristems", "apices"]
    },
    {
        "id": "3b_i",
        "question": "3. (b) (i) Give two sources of human stem cells. (List two)",
        "answer": ["Bone marrow", "umbilical cord", "embryo"],
        "marks": 2,
        "type": "any_x_from",
        "num_required": 2
    },
    {
        "id": "3b_ii_similarity",
        "question": "3. (b) (ii) Give one SIMILARITY between human and plant stem cells.",
        "answer": "cells divide/mitosis/differentiate",
        "marks": 1, # Part of a 2-mark question
        "keywords": ["divide", "mitosis", "differentiate"]
    },
    {
        "id": "3b_ii_difference",
        "question": "3. (b) (ii) Give one DIFFERENCE between human and plant stem cells.",
        "answer": "plant stem cells can redifferentiate; human stem cells cannot redifferentiate",
        "marks": 1, # Part of a 2-mark question
        "keywords": ["plant redifferentiate", "human cannot redifferentiate", "plant can", "human cannot"]
    },
    {
        "id": "4a",
        "question": "4. (a) Suggest why there are no chloroplasts visible in the electron microscope photograph of a plant cell (from the exam paper).",
        "answer": "It is a root cell/plane of section",
        "marks": 1,
        "keywords": ["root cell", "plane of section", "not a leaf cell", "underground"]
    },
    {
        "id": "4b",
        "question": "4. (b) Calculate the magnification of the photograph. Diameter of nucleus shown by arrow = 60 mm. Actual diameter of nucleus = 15 micrometres.",
        "answer": "x4000", # 60000 micrometres / 15 micrometres
        "marks": 3,
        "calculation_steps": "Convert 60 mm to micrometres: 60 * 1000 = 60000 µm. Magnification = Image / Actual = 60000 / 15 = 4000."
    },
    {
        "id": "4c",
        "question": "4. (c) What does the term resolution mean (in microscopy)?",
        "answer": "Ability to see fine detail/distinguish between two close points",
        "marks": 1,
        "keywords": ["fine detail", "distinguish", "two points", "clear"]
    },
    {
        "id": "5a",
        "question": "5. (a) Describe the direction of a nerve impulse across the gap (synapse) between two neurones (refer to diagram in exam paper - arrow from pre-synaptic to post-synaptic).",
        "answer": "Arrow pointing left to right/from pre-synaptic to post-synaptic", # Assuming standard diagram
        "marks": 1,
        "keywords": ["left to right", "pre-synaptic", "post-synaptic"]
    },
    {
        "id": "5b",
        "question": "5. (b) Complete the passage: A nerve impulse arrives. Vesicles release a (1)______ chemical into the gap. This gap is called a (2)______. The chemical (3)______ across the gap. If a high enough (4)______ of this chemical reaches the next neurone, an (5)______ impulse is generated. (Provide 5 words separated by commas)",
        "answer": "Transmitter, synapse, diffuses, concentration, electrical",
        "marks": 5,
        "type": "fill_blanks",
        "num_blanks": 5
    },
    # ... (Continue for all questions)
    # Example for QWC:
    {
        "id": "9a_i",
        "question": "9. (a) (i) Explain how changes in the level of carbon dioxide in the atmosphere can affect global temperatures. Your answer should:\n"
                    "• describe how the level of carbon dioxide is changing.\n"
                    "• explain how this change can affect global temperatures.\n"
                    "• give two causes of this change.\n"
                    "(This is a Quality of Written Communication question - aim for clear, structured answer using scientific terms)",
        "answer": "Indicative content:\n"
                  "Change: Increases/layer of gases becomes thicker.\n"
                  "How change affects global temperatures: Less heat energy can escape back into space/heat energy is reflected back to earth; Global temperature increases.\n"
                  "Causes: Deforestation; Combustion of fossil fuels.",
        "marks": 6,
        "type": "qwc" # Quality of Written Communication
    },
    {
        "id": "9a_ii",
        "question": "9. (a) (ii) Give two other problems associated with the change in global temperatures. (List two)",
        "answer": ["Ice caps melt", "rising sea levels", "flooding", "loss of habitats"],
        "marks": 2,
        "type": "any_x_from",
        "num_required": 2
    },
    {
        "id": "9b_i",
        "question": "9. (b) (i) In 2016, 20.6 million tonnes of greenhouse gases were emitted. In 2017, this decreased to 20 million tonnes. Calculate the percentage decrease. (Show 0.6; ÷ 20.6; 2.9%)",
        "answer": "2.9%",
        "marks": 3,
        "calculation_steps": "Decrease = 20.6 - 20 = 0.6 million tonnes. Percentage decrease = (0.6 / 20.6) * 100 = 2.912... % ≈ 2.9%"
    },
    {
        "id": "9b_ii",
        "question": "9. (b) (ii) Describe one initiative a government could take to reduce carbon dioxide levels in the atmosphere.",
        "answer": "Reforestation/international treaties/renewable energy (described)",
        "marks": 1,
        "keywords": ["reforestation", "treaties", "renewable energy", "planting trees", "solar", "wind"]
    }
]
# --- Quiz Logic ---
def run_quiz():
    speak("Hello Jackson! Let's start your Biology revision quiz.")
    time.sleep(1)
    score = 0
    total_marks_available = sum(q['marks'] for q in questions_data)
    question_count = 0

    random.shuffle(questions_data) # Shuffle questions for variety

    for q_data in questions_data:
        question_count += 1
        print("-" * 30)
        print(f"Question {question_count} ({q_data['marks']} mark{'s' if q_data['marks'] > 1 else ''}):")
        print(q_data["question"])

        user_answer = input("Your answer: ").strip()

        correct = False
        q_type = q_data.get("type")

        if q_type == "any_x_from":
            correct_options = [opt.lower() for opt in q_data["answer"]]
            user_answers_list = [ans.strip().lower() for ans in user_answer.split(',')]
            
            matches_found = 0
            valid_user_answers = []
            for ua in user_answers_list:
                if ua in correct_options and ua not in valid_user_answers: # ensure unique matches
                    valid_user_answers.append(ua)
                    matches_found +=1
            
            if matches_found >= q_data["num_required"]:
                correct = True
                # Award partial marks if needed, for simplicity full marks if num_required met
                score += q_data["marks"]
            else:
                print(f"You got {matches_found} out of {q_data['num_required']} correct parts.")


        elif q_type == "fill_blanks":
            correct_blanks = [b.strip().lower() for b in q_data["answer"].split(',')]
            user_blanks = [b.strip().lower() for b in user_answer.split(',')]
            if len(user_blanks) == q_data["num_blanks"]:
                correct_count = 0
                for i in range(q_data["num_blanks"]):
                    if user_blanks[i] == correct_blanks[i]:
                        correct_count +=1
                
                # Simple marking: all or nothing for the fill-in-the-blanks question as a whole
                # Or award marks per correct blank
                if correct_count == q_data["num_blanks"]:
                    correct = True
                    score += q_data["marks"]
                else:
                     print(f"You got {correct_count} out of {q_data['num_blanks']} blanks correct.")
            else:
                print(f"Please provide exactly {q_data['num_blanks']} answers separated by commas.")
        
        elif q_type == "qwc":
            print("\n--- For QWC questions, compare your answer to the indicative content below ---")
            print(f"Correct Answer/Indicative Content:\n{q_data['answer']}")
            print("--- Self-assess your answer based on the marking bands (A, B, C, D from scheme) ---")
            # For simplicity, we won't auto-grade QWC. We could ask user to self-award marks.
            try:
                awarded = int(input(f"How many marks (0-{q_data['marks']}) would you award yourself for this QWC? "))
                score += min(max(0, awarded), q_data['marks']) # ensure marks are within range
            except ValueError:
                print("Invalid input for marks. Skipping marks for this QWC.")
            # No 'correct' sound for QWC as it's self-assessed

        else: # Standard short answer or calculation
            # For calculation answers, allow some flexibility if 'allow_range' is defined
            if "allow_range" in q_data:
                if user_answer.lower() in q_data["allow_range"]:
                    correct = True
            elif "keywords" in q_data:
                found_keywords = 0
                for keyword in q_data["keywords"]:
                    if keyword.lower() in user_answer.lower():
                        found_keywords +=1
                # Heuristic: if most keywords are present, consider it correct for simple check
                # Or if the answer is one of the alternatives (e.g. "meristems/apices")
                if (found_keywords >= len(q_data["keywords"]) * 0.6) or \
                   any(alt.lower() == user_answer.lower() for alt in q_data["answer"].lower().split('/')):
                    correct = True
            
            # Fallback to exact match if no special handling
            if not correct and user_answer.lower() == str(q_data["answer"]).lower():
                 correct = True
            elif not correct and "/" in str(q_data["answer"]): # Handle alternatives like "A/B"
                if any(opt.strip().lower() == user_answer.lower() for opt in str(q_data["answer"]).split('/')):
                    correct = True


            if correct:
                score += q_data["marks"]

        # Feedback for non-QWC questions
        if q_type != "qwc":
            if correct:
                print("Correct!")
                play_sound("correct")
            else:
                print("Incorrect.")
                play_sound("incorrect")
                print(f"The correct answer is: {q_data['answer']}")
                if "calculation_steps" in q_data:
                    print(f"Calculation: {q_data['calculation_steps']}")
        
        print(f"Your current score: {score}")

        # "Stay focused" reminder
        if question_count % STAY_FOCUSED_INTERVAL == 0 and question_count < len(questions_data):
            time.sleep(1) # Pause before reminder
            speak("Jackson, stay focused!")
            time.sleep(0.5)

    print("-" * 30)
    speak(f"Quiz finished, Jackson! Your final score is {score} out of {total_marks_available}.")
    percentage = (score / total_marks_available) * 100 if total_marks_available > 0 else 0
    speak(f"That's {percentage:.2f} percent.")
    if percentage >= 80:
        speak("Excellent work, you're doing great!")
    elif percentage >= 60:
        speak("Good job! Keep practicing these topics.")
    else:
        speak("Keep revising, Jackson. You can improve!")

if __name__ == "__main__":
    run_quiz()