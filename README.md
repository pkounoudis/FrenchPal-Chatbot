# My-chatBot
Rasa project for Master's Course 

a. An experimental chatbot for educational purposes, and more specifically for language learning. I wanted to implement a "language helper" for people who are learning french, and provide
them with 3 tools. A grammar helper, a translator and an exercises' generator. The three main scenarios are described below.

b. First Tool, Grammar Helper. It is implemented with a json database with 4 options. The verbs etre, parler, apprendre and finir (one for each conjugation category). The user chooses a verb
and the bot answers with the verb's conjugation in the Present Tense. 
  Second tool, Translator. It is implemented with the help of ChatGPT 3.5 api. The user gives a text (up to 50 words) in french
and the bot gives the english translation. 
  Third tool, Exercises Generator. Again, this tools is implemented with the help of the ChatGPT 3.5 api. The user chooses the level of difficulty (A2 or B2) and the bot generates a small grammar
exercise.

c. More options regarding the exercises' dificulty level, their genre (either vocabulary or grammar), more verbs in various tenses, help with more grammar phenomena (plural, subjonctif etc) and maybe explore 
some more functionalities. For example, a chatbot could be made that generates history quizzez, answers math questions or even helps with university administration tasks (i.e. paying of tuition fees) and 
has answers for almost all course-related information, including fees, curriculum covered, completion date, etc. 

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Chatbot-Extended Version Assignment 3

a. Forms

I used Rasa Forms to properly change scenario 3, Exercises Generator. The form that was implemented ensures that entities A2 or B2 fill the required slot only when the relevant intent is formed, and not otherwise.
In the following example from Rasa interactive, I ask the bot to help me with grammar but I intentionally mention the A2 entity with the "Some grammar A2" string. The slot is not filled (None), even though the entity was recognized.

 3    utter_greet 1.00                                                             
      Hey! I am a french tutor! Do you need help with                              
      grammar, do you want me to translate something for                           
      you or would you like some exercises?!                                       
      action_listen 1.00                                                           
───────────────────────────────────────────────────────────────────────────────────
 4                                                                    Some grammar 
                                                                   [A2][{"entity": 
                                                                      "ex_level"}, 
                                                                        {"entity": 
                                                                      "ex_level"}] 
                                                              intent: grammar 0.99 
Current slots: 
        ex_level: None, requested_slot: None, session_started_metadata: None

I also added a story "unhappy language exercises A2/B2" to handle cases where the user chooses the wrong exercises level (wrong input) i.e. C2 level exercises instead of A2 or B2. To that end, a new intend "wrong_exercises_level" was added. For example:

Your input ->  hi!                                                                     
Hey! I am a french tutor! Do you need help with grammar, do you want me to translate something for you or would you like some exercises?!
Your input ->  exercises                                                               
Bien sure! Please choose the level of difficulty (A2 or B2)!
Your input ->  C2                                                                      
Please, enter again a valid exercises level (A2 or B2)

Finally, when the user engages in irrelevant conversation (chitchat) i.e. asks for the weather in the middle of an exercises intent, the bot answers and asks again for the exercises level. For example:

Your input ->  hi                                                                      
Hey! I am a french tutor! Do you need help with grammar, do you want me to translate something for you or would you like some exercises?!
Your input ->  exercises please                                                        
Bien sure! Please choose the level of difficulty (A2 or B2)!
Your input ->  What is the weather though?                                             
It's always sunny in Greece! Now, please choose the level of difficulty (A2 or B2)!
Your input ->  c2                                                                      
Please, enter again a valid exercises level (A2 or B2)
Your input ->  a2                                                                      
Here is some a2 exercises! Fill in the blanks with the appropriate form of the verb in parentheses.
1. Je (manger) du pain.
2. Tu (aller) à la plage.
3. Elle (regarder) la télévision.
4. Nous (parler) français.
5. Ils (jouer) au foot.
Answers:
1. mange
2. vas
3. regarde
4. parlons
5. jouent

b. Policies
