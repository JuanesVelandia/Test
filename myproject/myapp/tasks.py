from __future__ import absolute_import, unicode_literals
import openai
import re
import nltk
nltk.download('punkt')
import os

def procesar_archivos(temperatura):

    openai.api_key = "c85f5ba19e264974912657a10cb70c8d"
    openai.api_base = "https://cog-r64zdcyjshwjk.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    # Ruta a la carpeta "archivos"
    carpeta_archivos = './archivos'  # Asegúrate de usar la ruta correcta en tu sistema

    # Enumerar los archivos en la carpeta
    for archivo in os.listdir(carpeta_archivos):
        archivo_path = os.path.join(carpeta_archivos, archivo)

        # Verificar si es un archivo
        if os.path.isfile(archivo_path):
            # Realizar operaciones en el archivo aquí
            # Puedes abrirlo y leer su contenido o hacer lo que necesites
            with open(archivo_path, 'r') as file:
                code = file.read()
                
            tokens = nltk.word_tokenize(code)
            if ((len(tokens)+50)*2.5) < 3900:
                print("Size of the file accepted")
            else:
                print("The size of the file is large")


            response = openai.ChatCompletion.create(
            engine = "gpt-35-turbo-mic",
            messages=[
                {"role": "system", "content": "You are a professional in cybersecurity and you are an expert amending code, to eliminate all the vulnerabilities that the code present and returning the secure code"},
                {"role": "user", "content": "Would you like to check my code?"},
                {"role": "user", "content": "I pass you my code in the next input:"},
                {"role": "user", "content": code},
                {"role": "user", "content": "In the secure code that you created, return me the code commented in the lines that you changed, but this comments doesnt include the words 'changes' and 'made'"},
                {"role": "user", "content": "Answer me explicitly with this structure:' Here is your secure code: THE CODE HERE."},
                {"role": "user", "content": "And a description of what changes have you made with this structure: 'Changes made: LIST OF CHANGES'"},
                {"role": "user", "content": "At the end of everything, return me everytime a list of 3 and always 3 principal key words (separate into line breaks) of the vulnerabilites you find in the code, with this structure: 'List of keywords: KEYWORDS'"},
                {"role": "user", "content": "In case that the code is not vulnerable, use the same structure with the same code, in list of changes saying why is not vulnerable and in the list of the keyword add three keywords that have to be relasionated with the code"},
            ],
            temperature=float(temperatura)
            )

            secureCode = response['choices'][0]['message']['content']

            regex =  re.compile(r'Changes made:(.*)List of keywords', re.DOTALL)
            res = regex.search(secureCode)
            if res is not None:
                description = res.group(1)
            else:
                description = "No changes were made, maybe try again ;)"

            regex = re.compile(r'```(.*)```', re.DOTALL)
            res = regex.search(secureCode)
            secureCodeLines = res.group(1)

            regex =  re.compile(r'List of keywords:(.*)', re.DOTALL)
            res = regex.search(secureCode)
            key_words = res.group(1)
            key_words = key_words.replace("-", "").replace(",", "\n").replace("```","")
            url1 = ""
            url2 = ""
            url3 = ""
            lista_hecha = ["","",""]
            if "None" not in key_words:
                lista = key_words.split("\n")
                lista_hecha = [s for s in lista if s]

                url1 = f" https://stackoverflow.com/search?q={lista_hecha[0]}"
                url2 = f" https://stackoverflow.com/search?q={lista_hecha[1]}"
                url3 = f" https://stackoverflow.com/search?q={lista_hecha[2]}"

            with open(archivo_path, 'w') as file:
                file.write(secureCodeLines)



            return [description,url1,url2,url3,lista_hecha[0],lista_hecha[1],lista_hecha[2]]

def resumir_archivos(temperatura):
    openai.api_key = "c85f5ba19e264974912657a10cb70c8d"
    openai.api_base = "https://cog-r64zdcyjshwjk.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    # Ruta a la carpeta "archivos"
    carpeta_archivos = './archivos'  # Asegúrate de usar la ruta correcta en tu sistema

    # Enumerar los archivos en la carpeta
    for archivo in os.listdir(carpeta_archivos):
        archivo_path = os.path.join(carpeta_archivos, archivo)

        # Verificar si es un archivo
        if os.path.isfile(archivo_path):
            # Realizar operaciones en el archivo aquí
            # Puedes abrirlo y leer su contenido o hacer lo que necesites
            with open(archivo_path, 'r') as file:
                code = file.read()
                
            tokens = nltk.word_tokenize(code)
            if ((len(tokens)+50)*2.5) < 3900:
                print("Size of the file accepted")
            else:
                print("The size of the file is large")

            response = openai.ChatCompletion.create(
                engine = "gpt-35-turbo-mic",
                messages=[
                    {"role": "system", "content": "You are a professional programmer and you are an expert at summarizing codes."},
                    {"role": "user", "content": "Would you like to summarize my code?"},
                    {"role": "user", "content": "I pass you my code in the next input:"},
                    {"role": "user", "content": code},
                    {"role": "user", "content": "Answer me with this structure: Summary of the code: THE SUMMARY"},
                ],
                temperature=float(temperatura)
            )

            summaryCode = response['choices'][0]['message']['content']

            return summaryCode
