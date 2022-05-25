import subprocess

Qs = ["Who is the president of China?", "Who is the president of Portugal?", "Who is the president of Guam?", "Who is the prime minister of Eswatini?", "Who is the prime minister of Tonga?", "What is the population of Isle of Man?", "What is the population of Tokelau?", "What is the population of Djibouti?", "What is the area of Mauritius?", "What is the area of Luxembourg?", "What is the area of Guadeloupe?", "What is the form of government in Argentina?", "What is the form of government in Sweden?", "What is the form of government in Bahrain?", "What is the form of government in North Macedonia?", "What is the capital of Burundi?", "What is the capital of Mongolia?", "What is the capital of Andorra?", "What is the capital of Saint Helena, Ascension and Tristan da Cunha?", "What is the capital of Greenland?", "List all countries whose capital name contains the string hi", "List all countries whose capital name contains the string free", "List all countries whose capital name contains the string alo", "List all countries whose capital name contains the string baba", "How many  Absolute monarchy are also Unitary state?", "How many Dictatorship are also Presidential system?", "How many Dictatorship are also Authoritarian?", "How many presidents were born in Iceland? ", "How many presidents were born in Republic of Ireland? ", "When was the president of Fiji born?", "When was the president of United States born?", "Where was the president of Indonesia born?", "Where was the president of Uruguay born?", "Where was the prime minister of Solomon Islands born?", "When was the prime minister of Lesotho born?", "Who is Denis Sassou Nguesso?","Who is David Kabua?"]

Answers = ["Xi Jinping", "Marcelo Rebelo de Sousa", "Joe Biden", "Cleopas Dlamini", "Siaosi Sovaleni", "84,069", "1,499", "921,804", "2,040 km squared", "2,586.4 km squared", "1,628 km squared", "Federal republic, Presidential system, Republic", 
"Constitutional monarchy, Parliamentary system, Unitary state", "Parliamentary, Semi-constitutional monarchy, Unitary state", "Parliamentary republic, Unitary state", "Gitega", "Ulaanbaatar", "Andorra la Vella", "Jamestown, Saint Helena", "Nuuk", "Bhutan, India, Moldova, Sint Maarten, United States", "Sierra Leone", "Niue, Tonga", "Eswatini, Ethiopia", "5", "5", "3", "1", "0", "1964-04-20", "1942-11-20", "Indonesia", "Uruguay", "Papua New Guinea", "1961-11-03", "President of Republic of the Congo", "President of Marshall Islands"]



i = 1
for q,ans in zip(Qs, Answers):
    cmd = ["python3", "geo_qa.py", "question", q]
    output = subprocess.run(cmd, encoding="UTF-8", capture_output=True)
    stdout_output = str(output.stdout).strip("\n")

    if (stdout_output != ans):
        print()
        print("Test Failed")
        print("Q: " + q)
        print("Output: " + stdout_output)
        print("Answer: " + ans)
        print()
    else: 
        print("test " + str(i) + " passed" )

    i += 1

    
        
        
