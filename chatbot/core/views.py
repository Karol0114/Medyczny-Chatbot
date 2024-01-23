from spacy.lang.pl.stop_words import STOP_WORDS
from spacy.lang.pl import Polish
import spacy
from django.shortcuts import render
import openai
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)

nlp = spacy.load('pl_core_news_sm')

def lemmatize_text(text):
    
    doc = nlp(text.lower())
    
    return [token.lemma_ for token in doc if token.text not in STOP_WORDS]


def is_medical_query(user_input, medical_keywords):
    
    lemmatized_input = lemmatize_text(user_input)
    # Sprawdź, czy któryś z lematów słów kluczowych znajduje się w tekście
    for keyword in medical_keywords:
        if any(lemma.startswith(keyword) for lemma in lemmatized_input):
            return True
    return False

def chatbot(request):
    chatbot_response = None
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
        prompt = user_input

        medical_keywords = [
            'ból', 'temperatura', 'gorączka', 'zapalenie', 'antybiotyk', 'diagnoza',
            'terapia', 'leczenie', 'operacja', 'szpital', 'pacjent', 'zdrowie',
            'choroba', 'objawy', 'lekarz', 'pielęgniarka', 'medycyna', 'tabletki',
            'recepta', 'badanie', 'krwi', 'serce', 'ciśnienie', 'cukrzyca',
            'astma', 'alergia', 'wirus', 'infekcja', 'rak', 'nowotwór', 'badań',
            'szczepienie', 'immunizacja', 'grypa', 'covid', 'depresja', 'psychologia',
            'antydepresanty', 'analgezja', 'szczepionka', 'radiologia', 'onkologia',
            'kardiologia', 'neurologia', 'dermatologia', 'gastroenterologia',
            'hematologia', 'okulistyka', 'ortopedia', 'pediatria', 'psychiatria',
            'reumatologia', 'urologia', 'endokrynologia', 'narkoza', 'rehabilitacja',
            'morfina', 'ibuprofen', 'paracetamol', 'aspiryna', 'insulina', 'steroidy',
            'test', 'wymaz', 'tomografia', 'rezonans', 'magneticzny', 'ultrasonografia',
            'ekg', 'eeg', 'laboratorium', 'analiza', 'krew', 'mocz', 'genetyczne',
            'biopsja', 'transplantacja', 'dawca', 'przeszczep', 'dializa', 'opieka',
            'pierwsza pomoc', 'zawał', 'udar', 'złamanie', 'kontuzja', 'zwichnięcie',
            'zapalenie stawów', 'osteoporoza', 'epidemia', 'pandemia', 'profilaktyka',
            'witamin', 'suplement', 'dieta', 'odżywianie', 'fitness', 'ćwiczenia',
            'rekonwalescencja', 'zatrucie', 'toksyna', 'detoks', 'odtrucie',
            'higiena', 'sanitarny', 'dezynfekcja', 'sterylizacja', 'maseczka', 'rękawiczki',
            'immunologia', 'szpitalny', 'klinika', 'szczep', 'lekarski', 'medyczny',
            'konsultacja', 'terapeuta', 'farmacja', 'apteka', 'dawkowanie', 'przeciwbólowy',
            'przeciwzapalny', 'przeciwwirusowy', 'antyseptyczny', 'sztuczna inteligencja',
            'sztuczny', 'diagnozowanie', 'symulacja', 'symptomatyczny', 'terapeutyczny',
            'zabieg', 'procedura', 'farmakologia', 'anatomia', 'patologia', 'bakteryjny',
            'wirusowy', 'zakaźny', 'niezakaźny', 'chroniczny', 'ostry', 'łagodny',
            'pilny', 'awaryjny', 'profilaktyczny', 'diagnostyczny', 'chirurgiczny',
            'bezobjawowy', 'kwarantanna', 'izolacja', 'dezynfekcja', 'antybiogram',
            'steroid', 'szczepienia', 'próba kliniczna', 'badanie kliniczne',
            'karta pacjenta', 'historia choroby', 'elektroniczna dokumentacja medyczna',
            'zgoda na leczenie', 'etyka medyczna', 'prawo medyczne', 'ubezpieczenie zdrowotne',
            'opieka zdrowotna', 'zdrowie publiczne', 'zarządzanie w ochronie zdrowia',
            'polityka zdrowotna', 'badanie profilaktyczne', 'check-up', 'kontrola zdrowia',
            'świadomość zdrowotna', 'edukacja zdrowotna', 'wypalenie zawodowe',
            'dobrostan', 'samopoczucie', 'terapia zajęciowa', 'rehabilitacja neurologiczna',
            'rehabilitacja kardiologiczna', 'rehabilitacja ortopedyczna',
            'opieka długoterminowa', 'opieka paliatywna', 'opieka domowa', 'telemedycyna',
            'zdrowie cyfrowe', 'e-zdrowie', 'innowacje medyczne', 'startup medyczny',
            'technologia w medycynie', 'monitorowanie zdrowia', 'urządzenia medyczne',
            'narzędzia diagnostyczne', 'medycyna precyzyjna', 'personalizowana medycyna',
            
            'boli', 'bolało', 'boli mnie', 'ból głowy', 'ból brzucha', 'ból pleców',
            'wymiotuje', 'wymioty', 'nudności', 'mdłości', 'biegunka', 'biegnę do toalety',
            'opada mi z sił', 'czuję się słabo', 'kaszlę', 'kaszel', 'mam katar', 'katar',
            'gorączka', 'mam gorączkę', 'dreszcze', 'drgawki', 'cierpię', 'cierpienie',
            'osłabienie', 'zmęczenie', 'zawroty głowy', 'zawrót głowy', 'zemdlenia', 'omdlenia',
            'ręka', 'noga', 'głowa', 'serce', 'wątroba', 'nerki', 'płuca', 'żołądek',
            'mięśnie', 'stawy', 'kości', 'skóra', 'żyły', 'tętnice', 'ropień', 'wrzód',
            'siniak', 'krwiak', 'otarcie', 'rana', 'zranienie', 'pęknięcie', 'złamanie',
            'zwichnięcie', 'nadwyrężenie', 'kontuzja', 'oparzenie', 'uraz', 'blizna',
            'swędzenie', 'wysypka', 'trądzik', 'egzema', 'łuszczyca', 'uczulenie', 'alergia',
            'szum w uszach', 'utrata słuchu', 'krwotok', 'krwawienie', 'krwawię',
            'zakażenie', 'infekcja', 'gorączka', 'dreszcze', 'sztywność karku', 'sztywnienie',
            'drętwienie', 'mrowienie', 'spuchnięcie', 'obrzęk', 'zaburzenia snu', 'bezsenność',
            'migrena', 'ból zęba', 'zęby', 'chirurg', 'ortopeda', 'kardiolog', 'neurolog',
            'dermatolog', 'gastroenterolog', 'okulista', 'laryngolog', 'pediatra', 'ginekolog',
            'psycholog', 'psychiatra', 'anestezjolog', 'ratownik medyczny', 'pielęgniarka',
            'położna', 'fizjoterapeuta', 'dietetyk', 'higienistka stomatologiczna',
            'badanie krwi', 'morfologia', 'badanie moczu', 'USG', 'RTG', 'rezonans magnetyczny',
            'tomografia komputerowa', 'biopsja', 'endoskopia', 'kolonoskopia', 'mammografia',
            'angiografia', 'elektrokardiogram', 'EKG', 'EEG', 'spirometria', 'test wysiłkowy',
            'próba alergiczna', 'test skórny', 'próba czynnościowa', 'badanie słuchu',
            'badanie wzroku', 'laparoskopia', 'artroskopia', 'chemioterapia', 'radioterapia',
            'przeszczep', 'dializa', 'szew', 'zastrzyk', 'iniekcja', 'infuzja',
            'terapia manualna', 'masaż', 'krioterapia', 'termoterapia', 'elektroterapia',
            'hydroterapia', 'ćwiczenia rehabilitacyjne', 'trening funkcjonalny', 'rehabilitacja',
            'leki przeciwbólowe', 'leki przeciwzapalne', 'antybiotyki', 'sterydy',
            'leki przeciwhistaminowe', 'leki przeciwkoagulacyjne', 'witaminy', 'suplementy',
            'probiotyki', 'boli', 'bolało', 'boleć', 'ból głowy', 'bóle mięśniowe', 'bóle stawów',
            'wymiotować', 'wymioty', 'mdłości', 'nudności', 'biegunka', 'biegunkowy',
            'wysoka gorączka', 'gorączkować', 'kaszel', 'kaszleć', 'katar', 'kichać',
            'zatkany nos', 'czkawka', 'opadać z sił', 'osłabienie', 'zapalenie ucha',
            'zapalenie gardła', 'dreszcze', 'zimno', 'ciepłota', 'temperatura ciała',
            'szyja', 'ramię', 'noga', 'ręka', 'stopa', 'palec', 'kolano', 'łokieć',
            'nadgarstek', 'kręgosłup', 'serce', 'wątroba', 'płuca', 'nerki', 'mózg',
            'żołądek', 'jelita', 'trzustka', 'śledziona', 'mięsień', 'ścięgno',
            'cierpienie', 'cierpi', 'cierpiał', 'boleśnie', 'dyskomfort', 'swędzenie',
            'swędzi', 'wysypka', 'zakażenie', 'infekcja', 'stan zapalny', 'zapalenie',
            'uczulenie', 'alergia', 'reakcja alergiczna', 'pokrzywka', 'obrzęk',
            'duszności', 'trudności w oddychaniu', 'astma', 'krwiak', 'stłuczenie',
            'zranienie', 'rana', 'skaleczenie', 'uraz', 'kontuzja', 'złamanie',
            'zwichnięcie', 'naciągnięcie', 'skręcenie', 'zakrzep', 'krwotok',
            'hematoma', 'krwawienie', 'wylew', 'udar', 'atak serca', 'zawał',
            'niedrożność', 'zatkanie', 'zator', 'zakrzepica', 'sepsa', 'szok',
            'omdlenie', 'zemdlenie', 'utrata przytomności', 'zawroty głowy', 'szum w uszach',
            'ból zęba', 'dziąsło', 'cukrzyca', 'hipoglikemia', 'hiperglikemia',
            'nadciśnienie', 'niedociśnienie', 'cholesterol', 'tarczyca', 'hormony',
            'nerwica', 'depresja', 'lęk', 'bezsenność', 'zmęczenie', 'wyczerpanie',
            'stres', 'psychoterapia', 'leczenie', 'kuracja', 'terapia', 'rehabilitacja',
            'operacja', 'zabieg', 'narkoza', 'anestezja', 'sedacja', 'badanie',
            'diagnostyka', 'USG', 'RTG', 'MRI', 'CT', 'EKG', 'EEG', 'angiografia',
            'endoskopia', 'kolonoskopia', 'biopsja', 'mammografia', 'prześwietlenie',
            'poziom cukru', 'badanie krwi', 'badanie moczu', 'analiza', 'próba',
            'test', 'wynik', 'diagnoza', 'prognostyka', 'leczenie zachowawcze',
            'leczenie operacyjne', 'terapia', 'dawkowanie', 'przepis', 'recepta',
            'lekarstwo', 'medykament', 'lek', 'tabletka', 'kapsułka', 'syrop',
            'maść', 'żel',
            
            'wymiotować', 'wymiotuje', 'wymiotował', 'wymiotowała', 'wymiotowali', 'wymiotowały',
            'biegunka', 'biegnę', 'biegłem', 'biegła', 'biegło', 'biegły',
            'kaszleć', 'kaszlę', 'kaszlał', 'kaszłała', 'kaszlą',
            'kichać', 'kicha', 'kichnął', 'kichnęła', 'kichają',
            'pomagać', 'pomagam', 'pomógł', 'pomogła', 'pomogli', 'pomogły',

            
            'serce', 'wątroba', 'nerka', 'płuco', 'płuca', 'żołądek', 'mięsień', 'mięśnie',
            'skóra', 'kość', 'kości', 'staw', 'stawy', 'kręgosłup', 'mózg', 'jelito', 'jelita',
            'tętnica', 'żyła', 'żołądek', 'oczodół', 'szpik', 'naczynia', 'krwionośne',

            
            'ból', 'boli', 'bolało', 'boleć', 'bolał', 'bolała', 'bolały', 'bolących',

            
            'cierpienie', 'cierpi', 'cierpiał', 'cierpiała', 'cierpieli', 'cierpiały',
            'leczyć', 'leczę', 'leczono', 'leczył', 'leczyła', 'leczyli', 'leczyły',
            'operować', 'operuję', 'operował', 'operowała', 'operowali', 'operowały',

            
            'zdrowie', 'choroba', 'lekarstwo', 'szczepionka', 'terapia', 'diagnoza',
            'symptom', 'objawy', 'procedura', 'badanie', 'zakażenie', 'infekcja',
            'kontuzja', 'uraz', 'złamanie', 'rana', 'gojenie', 'rehabilitacja', 'kuracja',
            'antybiotyk', 'wirus', 'bakteria', 'grzybica', 'alergia', 'uczulenie',
            'opieka', 'wsparcie', 'ratunek', 'pierwsza pomoc', 'ratownik', 'sanitariusz',

            
            'pomoc', 'pomóc', 'pomaga', 'pomogę', 'pomagają', 'pomocy', 'pomagając', 'pomocna', 'pomocny',
            
            'zawroty głowy', 'osłabienie', 'zmęczenie', 'gorączka', 'dreszcze', 'wysypka',
            'obrzęk', 'krwotok', 'zakrztuszenie', 'bezdech', 'śpiączka', 'omdlenie',
            'utrata przytomności', 'zadyszka', 'kołatanie serca', 'bladość', 'żółtaczka',

            
            'punkcja', 'nacięcie', 'szycie', 'zastrzyk', 'transfuzja', 'pobranie krwi',

            
            'Jakie są objawy', 'Co oznacza', 'Jak leczyć', 'Czy to poważne', 'Kiedy iść do lekarza',
            'Domowe sposoby', 'Pierwsza pomoc przy', 'Jak długo trwa', 'Czy to zaraźliwe',

            
            'resuscytacja', 'defibrylator', 'wentylacja', 'tlenoterapia', 'sonda', 'drenaż',

            
            'maść', 'syrop', 'krople', 'tabletki', 'kapsułki', 'zastrzyki', 'inhalacje',

        
            'odporność', 'dobrostan', 'profilaktyka', 'odżywianie', 'dietetyka', 'suplementacja',

            
            'układ odpornościowy', 'układ krążenia', 'układ pokarmowy', 'układ nerwowy', 'układ oddechowy',

            
            'anemia', 'nadciśnienie', 'hipotonia', 'cukrzyca', 'epilepsja', 'osteoporoza', 'zawał',
            'udar mózgu', 'astma', 'choroba refluksowa', 'zespół jelita drażliwego',

            
            'higiena', 'sanitariat', 'dezynfekcja', 'izolatka', 'epidemiologia', 'profilaktyka',

            
            'konsultacja online', 'wizyta domowa', 'teleporada', 'e-recepta', 'zdrowotna aplikacja',

            
            'pacjent', 'lekarz rodzinny', 'specjalista', 'chirurg', 'pediatra', 'internista', 'ortopeda',
            'kardiolog', 'neurolog', 'dermatolog', 'psychiatra', 'psycholog', 'fizjoterapeuta',
            'rehabilitant', 'dietetyk', 'pielęgniarka', 'położna', 'farmaceuta', 'apteka',

            
            'przychodnia', 'szpital', 'ośrodek zdrowia', 'klinika', 'sanatorium', 'hospicjum', 'poradnia',
            'laboratorium', 'diagnostyka', 'badanie', 'wynik', 'terapia', 'leczenie', 'rehabilitacja',
            'szczepienie', 'immunizacja', 'profilaktyka', 'edukacja zdrowotna',
            'cierpienie', 'ból', 'dyskomfort', 'złamanie', 'uraz', 'kontuzja',
            'zadrapanie', 'skaleczenie', 'oparzenie', 'krwiak', 'naciągnięcie', 'nadwyrężenie',
            'stan zapalny', 'zapalenie', 'infekcja', 'gorączka', 'dreszcze', 'uczucie zmęczenia',
            'osłabienie', 'nudności', 'wymioty', 'biegunka', 'zaparcie', 'ból brzucha',
            'katar', 'kaszel', 'duszności', 'świszczący oddech', 'problemy z oddychaniem',
            'wysypka', 'świąd', 'pokrzywka', 'obrzęk', 'anafilaksja', 'reakcja alergiczna',
            'ból głowy', 'migrena', 'zawroty głowy', 'omdlenia', 'utrata przytomności',
            'drgawki', 'sztywność karku', 'ból pleców', 'ból stawów', 'ból mięśni',
            'zaburzenia snu', 'bezsenność', 'nadmierna senność', 'zmiany apetytu',
            'przyrost wagi', 'utrata wagi', 'zaburzenia odżywiania', 'pragnienie', 'wysokie ciśnienie krwi',
            'niskie ciśnienie krwi', 'zaburzenia rytmu serca', 'zawał mięśnia sercowego', 'udar mózgu',
            'zaburzenia mowy', 'zaburzenia połykania', 'zaburzenia chodu', 'zaburzenia równowagi',
            'zaburzenia koncentracji', 'zaburzenia pamięci', 'zaburzenia widzenia', 'zaburzenia słuchu',
            'krwawienie', 'krwotok', 'krwawienie z nosa', 'krwawienie z dziąseł', 'krwawienie z odbytu',
            'hematoma', 'żółtaczka', 'zaburzenia wątroby', 'zaburzenia nerek', 'kamienie nerkowe',
            'kamienie żółciowe', 'infekcje dróg moczowych', 'nietrzymanie moczu', 'trudności z oddawaniem moczu',
            'zaburzenia miesiączkowania', 'ból piersi', 'zaburzenia erekcji', 'bezpłodność',
            'zaburzenia libido', 'zmiany skórne', 'pieprzyki', 'zmiany barwnikowe', 'nowotwory skóry',
            'ropień', 'czyrak', 'grzybica', 'pasożyty', 'wszy', 'gnidy', 'tasiemiec',
            'zakażenie HIV', 'zapalenie wątroby', 'zakażenie wirusem HPV', 'ospa wietrzna',
            'odra', 'różyczka', 'szkarlatyna', 'gruźlica', 'borrelioza', 'zakażenie clostridium difficile',
            'sepsa', 'odwodnienie', 'zatrucie', 'przedawkowanie', 'zaburzenia elektrolitowe',
            'hipokalcemia', 'hipokaliemia', 'hipomagnezemia', 'hipernatremia', 'hiponatremia',
            'kwasica', 'zasadowica', 'zaburzenia metaboliczne', 'cukrzyca', 'hipoglikemia',
            'hiperglikemia', 'ketonuria', 'kwasica ketonowa', 'hipotermia', 'hipertermia',
            'udar cieplny', 'odmrożenie', 'zakrzepica', 'zatorowość płucna', 'niewydolność serca',
            'niewydolność oddechowa', 'niewydolność', 'cierpię', 'cierpisz', 'cierpi', 'cierpimy', 'cierpicie', 'cierpią',
            'duszę', 'duszysz', 'dusi', 'dusimy', 'dusicie', 'duszą',
            'migrena', 'migreny', 'migrenie', 'migrenom', 'migreną', 'migrenach',
            'wysypka', 'wysypki', 'wysypce', 'wysypką', 'wysypek', 'wysypkach',
            'pokrzywka', 'pokrzywki', 'pokrzywce', 'pokrzywką', 'pokrzywek', 'pokrzywkach',
            'szkarlatyna', 'szkarlatyny', 'szkarlatynie', 'szkarlatyną', 'szkarlatyno',
            
            'szkarlatyna', 'szkarlatyny', 'szkarlatynie', 'szkarlatynę', 'szkarlatyno', 'szkarlatyną', 'szkarlatynach', 'szkarlatynami',
            
            'pokrzywka', 'pokrzywki', 'pokrzywce', 'pokrzywkę', 'pokrzywko', 'pokrzywką', 'pokrzywkach', 'pokrzywkami',
            
            'wysypka', 'wysypki', 'wysypce', 'wysypkę', 'wysypko', 'wysypką', 'wysypkach', 'wysypkami',
            
            'migrena', 'migreny', 'migrenie', 'migrenę', 'migrene', 'migreno', 'migreną', 'migrenach', 'migrenami',
            
            'duszę', 'dusisz', 'dusi', 'dusimy', 'dusicie', 'duszą', 'dusił', 'dusiła', 'dusiło', 'dusili', 'dusiły',
            
            'cierpię', 'cierpisz', 'cierpi', 'cierpimy', 'cierpicie', 'cierpią', 'cierpiał', 'cierpiała', 'cierpiało', 'cierpieli', 'cierpiały',
            
            'gorączka', 'ból', 'krwawienie', 'mdłości', 'zawroty głowy', 'kaszel', 'katar', 'ból gardła', 'ból głowy', 'ból brzucha',
            'złamanie', 'zwichnięcie', 'oparzenie', 'ugryzienie', 'cięcie', 'rana', 'siniak', 'opuchlizna', 'zakrztuszenie', 'zatrucie',
            
        ]

        # Sprawdź, czy pytanie zawiera słowa kluczowe
        if is_medical_query(user_input, medical_keywords):
            response = openai.chat.completions.create(
                messages=[
                    {"role": "user", "content": user_input}
                ],
                model='gpt-3.5-turbo-1106',
            )
            chatbot_response = response.choices[0].message.content
        else:
            chatbot_response = "Jestem chatbotem medycznym i mogę odpowiedzieć tylko na pytania związane z medycyną."

        print(chatbot_response)

        return JsonResponse({'reply': chatbot_response})
    else:
        return render(request, 'main.html')
