import os
import re

import asyncio
import aiohttp

from dotenv import load_dotenv


# Функция теста на адекватность
async def normal_request_test(text: str, prompt: dict, url: str, headers: dict) -> bool: 
    global usedTokens 
    global usedRequests 
    confirm_messages = [] 
    system_text = "Ты ассистент, который отвечает на вопросы только одним словом: да или нет." 
    request_text = f"Является ли блюдо {text} съедобным?" 
    prompt['messages'] = [ 
                    { 
                        "role": "system", 
                        "text": system_text 
                    }, 
                    { 
                        "role": "user", 
                        "text": request_text 
                    } 
                ] 
    prompt['completionOptions']['maxTokens'] = 150 
    for i in range(3): 
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, headers=headers, json=prompt) as response:
                await asyncio.sleep(1)
                if response.status == 200:
                    result = await response.json()
                    message = result['result']['alternatives'][0]['message']['text'] 
                    usedTokens += int(result['result']['usage']['totalTokens']) 
                    usedRequests += 1 
                    confirm_messages.append(message) 

                    if i == 2 and list(map(lambda x: x.lower(), confirm_messages)).count('да') == 2: 
                        return True 
                    elif i == 2 and list(map(lambda x: x.lower(), confirm_messages)).count('нет') == 2: 
                        return False 
                else:
                    print(f"Ошибка запроса: {response.status}")
                    return False

    confirm_messages = list(map(lambda x: x.lower(), confirm_messages)) 
    yes_answers = confirm_messages.count('да') 
    no_answers = confirm_messages.count('нет') 
 
    return yes_answers > no_answers


# Основная функция для вывода инфы о блюде
async def send_meal_info(text: str, prompt: dict, url: str, headers: dict) -> str:
    global usedTokens
    global usedRequests
    system_text = "Ты диетолог, способный помочь в правильном питании и подсчете калорий, белков, жиров и углеводов. Все ответ подсчета должен выглядеть как примерный расчет КБЖУ для описанного блюда."
    request_text = f"Рассчитай КБЖУ для блюда - {text}. \
                    Шаблон ответа: \n1. Расчет КБЖУ для каждого ингридиента \n2. Совет по следующему приему пищи **предложи блюда. \n3. Общее количество белков, жиров, углеводов, калорий **только числа\
                    **Строго пользуйся шаблоном вывода, говори от 1-го лица, никогда не меняй шаблон вывода. Не используй стоп-слов, типа: примерно, около, приблизительно"
    prompt['messages'] = [
                {
                    "role": "system",
                    "text": system_text
                },
                {
                    "role": "user",
                    "text": request_text
                }
            ]
    prompt['completionOptions']['maxTokens'] = 1000
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, headers=headers, json=prompt) as response:
                await asyncio.sleep(1)
                if response.status == 200:
                    result = await response.json()

                    message = result['result']['alternatives'][0]['message']['text']
                    usedTokens += int(result['result']['usage']['totalTokens'])
                    usedRequests += 1

                    return message
                else:
                    print(f"Ошибка запроса: {response.status}")
                    return False

# Функция получения основных параметров в текстовом виде: жиры, белки, углеводы, калории
async def get_params_CPFC(text: str, prompt: dict, url: str, headers: dict) -> str:
    global usedTokens
    global usedRequests
    system_text = "Следуй строго шаблонам и правилам."
    request_test = "Выведи данные по шаблону. Шаблон: ВсегоУглеводов_число, ВсегоБелка_число, ВсегоЖиров_число, ВсегоКалорий_число. Соблюдай шаблон, не пиши другой информации, помимо заданых параметров"
    prompt['messages'] = [
            {
                "role": "system",
                "text": system_text
            },
            {
                "role": "assistant",
                "text": text
            },
            {
                "role": "user",
                "text": request_test
            }
        ]
    prompt['completionOptions']['maxTokens'] = 1000
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, headers=headers, json=prompt) as response:
                await asyncio.sleep(1)
                if response.status == 200:
                    result = await response.json()
        
                    message = result['result']['alternatives'][0]['message']['text']
                    usedTokens += int(result['result']['usage']['totalTokens'])
                    usedRequests += 1

                    return message 
                else:
                    print(f"Ошибка запроса: {response.status}")
                    return False
            

# Функция проверки адекватности ответа
async def normal_request_test_2(text: str, params: dict, prompt: dict, url: str, headers: dict) -> bool:
    global usedTokens
    global usedRequests
    CPFC = ''
    for key, value in params.items():
        CPFC += f'{key}: {str(value)}\n'
    confirm_messages = []
    system_text = "Ты ассистент, который отвечает на вопросы только одним словом: да или нет."
    request_text = f"Является данные значения КБЖУ адекватными - {CPFC} для блюда {text}"
    prompt['messages'] = [
                    {
                        "role": "system",
                        "text": system_text
                    },
                    {
                        "role": "user",
                        "text": request_text
                    }
                ]
    prompt['completionOptions']['maxTokens'] = 150
    for i in range(3):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(url, headers=headers, json=prompt) as response:
                await asyncio.sleep(1)
                if response.status == 200:
                    result = await response.json()
                    message = result['result']['alternatives'][0]['message']['text']
                    usedTokens += int(result['result']['usage']['totalTokens'])
                    usedRequests += 1
                    confirm_messages.append(message)

                    if i == 1 and list(map(lambda x: x.lower(), confirm_messages)).count('да') == 2:
                        return True
                    elif i == 1 and list(map(lambda x: x.lower(), confirm_messages)).count('нет') == 2:
                        return False  
                else:
                    print(f"Ошибка запроса: {response.status}")
                    return False
        

    confirm_messages = list(map(lambda x: x.lower(), confirm_messages))
    yes_answers = confirm_messages.count('да')
    no_answers = confirm_messages.count('нет')

    return yes_answers > no_answers

# Функция получения числового количества жирова, белков, углеводов, калорий
async def extract_nutritional_info(text: str) -> str:
    nutritional_info = {'calories': None, 'proteins': None, 'fats': None, 'carbohydrates': None}

    patterns = {
        'calories': re.compile(r'\b(?:калорий|ккал|кал)\b[^0-9]*([\d,\.]+)\s*(?:ккал|калорий)?', re.IGNORECASE),
        'proteins': re.compile(r'\b(?:белков|белка|белок)\b[^0-9]*([\d,\.]+)\s*(?:г|грамма)?', re.IGNORECASE),
        'fats': re.compile(r'\b(?:жиров|жир)\b[^0-9]*([\d,\.]+)\s*(?:г|грамма)?', re.IGNORECASE),
        'carbohydrates': re.compile(r'\b(?:углеводов|углеводы)\b[^0-9]*([\d,\.]+)\s*(?:г|грамма)?', re.IGNORECASE)
    }

    for nutrient, pattern in patterns.items():
        matches = pattern.findall(text)
        if matches:
            for match in matches:
                value_str = match
                value_str = value_str.replace(',', '.').strip()
                if value_str[-1] == '.':
                    value_str = value_str[:-1]
                # Пытаемся преобразовать данные к float, чтобы после записать в словарь
                try:
                    value = float(value_str)
                    nutritional_info[nutrient] = value
                # Если не получается, появляется варнинг, что не получилось и подаем модели новый запрос на получение нового текста
                except ValueError:
                    warning = '1'

    return nutritional_info


async def calc_calories(meal: str) -> dict:
    load_dotenv()
    # Ключ папки 
    id_folder = os.getenv("FOLDER_ID")
    # Апи ключ
    apiKey = os.getenv("API_KEY")

    # Ссылка на модель
    model_uri = f'gpt://{id_folder}/yandexgpt-lite'

    # URL подачи запроса
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    # Хедеры для запроса
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {apiKey}"
    }

    # Основной промпт 
    prompt_main = {
                    "modelUri": model_uri,
                    "completionOptions": {
                        "stream": False,
                        "temperature": 0.6,
                        "maxTokens": None
                    },
                    "messages": None 
                }

    # Переменная, храянящая за один пользовательский запрос
    global usedTokens
    usedTokens = 0 

    # Переменная, хранящая количество запросов за один цикл пользователького запроса
    global usedRequests
    usedRequests = 0 

    # main код
    if len(meal) <= 100:
        await asyncio.sleep(1)
        isnormal_request = await normal_request_test(meal, prompt_main, url=url, headers=headers)
        if isnormal_request:
            flag = False
            for _ in range(10):
                # Ответ по пунктам для блюда
                nn_answer_for_meal = await send_meal_info(meal, prompt_main, url=url, headers=headers)
                # Грязный вывод КБЖУ(с текстом, в формате: "белки: 3г")
                dirty_CPFC = await get_params_CPFC(nn_answer_for_meal, prompt_main, url=url, headers=headers)
                # Чистый вывод КБЖУ в формате словаря
                clear_CPFC = await extract_nutritional_info(dirty_CPFC)
                if None not in clear_CPFC.values():
                    isnormal_request_2 = await normal_request_test_2(meal, clear_CPFC, prompt_main, url=url, headers=headers)
                    if isnormal_request_2:
                        flag = True
                        return {
                            'nn_answer': nn_answer_for_meal,
                            'CPFC': clear_CPFC,
                            'warning': None,
                            'usedTokens': usedTokens,
                            'usedRequests': usedRequests
                        }
                
            if not flag:
                # Варнинг, если прошло 5 иттераций и при этом результат не успешен, в таком случае не списываем у пользователя запрос
                warning = 'Не удалось сделать описание для заданого блюда, проверьте правильность написания и повторите попытку позже.'
        else:
            # Варнинг, если написали полную дичь в блюдо
            warning = 'Данное блюдо является не адекватным, избегайте зловредства, иначе вы будете забанены. Если произошла ошибка, сообщите в поддержку.'
    else:
        # Ошибка привышения количества символов
        warning = 'Вы привысили допустимое число символов для одного запроса - 100 символов.'

    return {
        'nn_answer': None, # Ответ от модели - строка
        'CPFC': None, # КБЖУ - словарь
        'warning': warning, # Предупреждения - строка
        'usedTokens': usedTokens, # Использованные токены - целое число
        'usedRequests': usedRequests # Использованные запросы - целое число
    }
