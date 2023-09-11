from __future__ import absolute_import, unicode_literals
import openai
import re
import nltk
nltk.download('punkt')
import os

# Function to process code files and generate secure code, descriptions, and keywords
def procesar_archivos(temperature):
    openai.api_key = "c85f5ba19e264974912657a10cb70c8d"
    openai.api_base = "https://cog-r64zdcyjshwjk.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    # Path to the "archivos" folder
    files_folder = './archivos'  # Make sure to use the correct path on your system

    # Iterate through files in the folder
    for file in os.listdir(files_folder):
        file_path = os.path.join(files_folder, file)

        # Check if it's a file
        if os.path.isfile(file_path):
            # Perform operations on the file here
            # You can open and read its content or do whatever you need
            with open(file_path, 'r') as file:
                code = file.read()

            #Verify that the the amount of tokens are valid for the actual license
            tokens = nltk.word_tokenize(code)
            if ((len(tokens) + 50) * 2.5) < 3900:
                print("Size of the file accepted")
            else:
                print("The size of the file is large")

            #Using the API
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo-mic",
                messages=[
                    {"role": "system", "content": "You are a professional in cybersecurity and you are an expert in amending code to eliminate vulnerabilities, returning the secure code."},
                    {"role": "user", "content": "Would you like to check my code?"},
                    {"role": "user", "content": "I'll pass you my code in the next input:"},
                    {"role": "user", "content": code},
                    {"role": "user", "content": "In the secure code that you created, return the code commented in the lines that you changed, excluding the words 'changes' and 'made'."},
                    {"role": "user", "content": "Answer me explicitly with this structure: 'Here is your secure code: THE CODE HERE.'"},
                    {"role": "user", "content": "And provide a description of the changes made with this structure: 'Changes made: LIST OF CHANGES'"},
                    {"role": "user", "content": "Finally, provide a list of 3 principal keywords (separated by line breaks) for the vulnerabilities found in the code, with this structure: 'List of keywords: KEYWORDS'"},
                    {"role": "user", "content": "If the code is not vulnerable, use the same structure with the same code, in the list of changes, explaining why it's not vulnerable, and in the list of keywords, add three relevant keywords related to the code."},
                ],
                temperature=float(temperature)
            )

            secure_code = response['choices'][0]['message']['content']

            #Regex for extract the respective text from the response
            regex = re.compile(r'Changes made:(.*)List of keywords', re.DOTALL)
            res = regex.search(secure_code)
            if res is not None:
                description = res.group(1)
            else:
                description = "No changes were made, maybe try again ;)"

            regex = re.compile(r'```(.*)```', re.DOTALL)
            res = regex.search(secure_code)
            secure_code_lines = res.group(1)

            regex = re.compile(r'List of keywords:(.*)', re.DOTALL)
            res = regex.search(secure_code)
            key_words = res.group(1)
            key_words = key_words.replace("-", "").replace(",", "\n").replace("```", "")
            url1 = ""
            url2 = ""
            url3 = ""
            keyword_list = ["", "", ""]
            if "None" not in key_words:
                keyword_list = [s for s in key_words.split("\n")]

                url1 = f" https://stackoverflow.com/search?q={keyword_list[0]}"
                url2 = f" https://stackoverflow.com/search?q={keyword_list[1]}"
                url3 = f" https://stackoverflow.com/search?q={keyword_list[2]}"

            #Overwrite the file with the secure lines
            with open(file_path, 'w') as file:
                file.write(secure_code_lines)

            return [description, url1, url2, url3, keyword_list[0], keyword_list[1], keyword_list[2]]

# Function to summarize code files
def resumir_archivos(temperature):
    openai.api_key = "c85f5ba19e264974912657a10cb70c8d"
    openai.api_base = "https://cog-r64zdcyjshwjk.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    # Path to the "archivos" folder
    files_folder = './archivos'  # Make sure to use the correct path on your system

    # Iterate through files in the folder
    for file in os.listdir(files_folder):
        file_path = os.path.join(files_folder, file)

        # Check if it's a file
        if os.path.isfile(file_path):
            # Perform operations on the file here
            # You can open and read its content or do whatever you need
            with open(file_path, 'r') as file:
                code = file.read()

            tokens = nltk.word_tokenize(code)
            if ((len(tokens) + 50) * 2.5) < 3900:
                print("Size of the file accepted")
            else:
                print("The size of the file is large")

            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo-mic",
                messages=[
                    {"role": "system", "content": "You are a professional programmer, and you are an expert at summarizing code."},
                    {"role": "user", "content": "Would you like to summarize my code?"},
                    {"role": "user", "content": "I'll pass you my code in the next input:"},
                    {"role": "user", "content": code},
                    {"role": "user", "content": "Provide a summary of the code using this structure: Summary of the code: THE SUMMARY"},
                ],
                temperature=float(temperature)
            )

            summary_code = response['choices'][0]['message']['content']

            return summary_code
