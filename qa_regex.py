import re

QUESTIONS = ["Who is the president of (?p<country>\S+)?",
             "Who is the prime minister of (?p<country>\S+)?",
             "What is the population of (?p<country>\S+)?",
             "What is the area of (?p<country>\S+)?",
             "What is the form of government in (?p<country>\S+)?",
             "What is the capital of (?p<country>\S+)?",
             "When was the president of (?p<country>\S+) born?",
             "Where was the president of (?p<country>\S+) born?",
             "When was the prime minister of (?p<country>\S+) born?",
             "Where was the prime minister of (?p<country>\S+) born?",
             "Who is (?p<entity>\S+)?",
             "How many (?p<government_form1>\S+) are also (?p<government_form2>\S+)?",
             "List all countries whose capital name contains the string <str> (?p<str>\S+)",
             "How many presidents were born in (?p<country>\S+)?"]
