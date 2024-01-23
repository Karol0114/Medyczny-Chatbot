# Wirtualny Chatbot Medyczny 

## Opis projektu
Wirtualny Chatbot Medyczny to aplikacja webowa, która udziela informacji medycznych. Chatbot wykorzystuje API Open AI, aby udzielać odpowiedzi na pytania użytkowników. W projekcie używamy modelu 'gpt-3.5-turbo-1106', aby móc poprawnie używac chatbota, nalezy utworzyć plik .env i w nim podać klucz do naszego API. 
![image](https://github.com/Karol0114/Medyczny-Chatbot/assets/108083935/79cae0ff-cc0d-485a-8435-d58ab4142fbc)


## Technologie oraz biblioteki użyte w projekcie 
- Python
- Html
- Css
- JavaScript
- django
- spacy
- openai
- os
- dotenv


## Instalacja oraz uruchomienie

Aby uruchomić projekt należy:
1. Sklonowac repozytorium do swojego środowiska lokalnego
2. Uruchomić serwer lokalny za pomoca polecenia: python manage.py runserver ![image](https://github.com/Karol0114/Medyczny-Chatbot/assets/108083935/7deac812-a80e-496a-b602-5183f809cfda)
3. Następnie, po uruchomieniu aplikacji, należy otworzyć przeglądarkę i przejść do localhost: 'http://localhost:8000/' .
4. Po uruchomieniu strony, powinna ona wyglądać nadtępująco:
   ![image](https://github.com/Karol0114/Medyczny-Chatbot/assets/108083935/3f02358a-b4f9-484d-9d3d-f8bb5cd08662)
5. W prawym dolnym rogu, znajduje się ikonka chatu, po kliknięciu jej, pojawi nam się chat i możemy zadać pytanie. Model filtruje pytania i jeżeli pytanie nie dotyczy zagadnień medycyny to wysyła wiadomość: "Jestem chatbotem medycznym i mogę odpowiedzieć tylko na pytania związane z medycyną."
   
![image](https://github.com/Karol0114/Medyczny-Chatbot/assets/108083935/b4591730-f067-4f04-850f-59fd6dfdeccf)

