async def calc_standard(
    gender: str, age: int, height: int, weight: int, lifestyle: str, goal: str
) -> dict:
    match lifestyle:
        case "Малоподвижный образ жизни":
            ARM = 1.2
        case "Тренировки 1-3 раза в неделю":
            ARM = 1.375
        case "Тренировки 3-5 раз в неделю":
            ARM = 1.55
        case "Высокие нагрузки каждый день":
            ARM = 1.725
        case "Экстрмеальные нагрузки":
            ARM = 1.9

    formule_mifflin = 10 * weight + 6.25 * height - 5 * age

    match gender:
        case "Мужчина":
            formule_mifflin += 5
            formule_harris = (
                88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            )
            quantity_calories = (height * 5) - (age * 6.8) + (weight * 13.7) + 66
        case "Женщина":
            formule_mifflin -= 161
            formule_harris = (
                447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            )
            quantity_calories = (height * 1.8) - (age * 4.7) + (weight * 9.6) + 655

    formule_mifflin *= ARM
    formule_harris *= ARM
    quantity_calories *= ARM

    formule_mean_harris_mifflin = int((formule_mifflin + formule_harris) / 2)

    match goal:
        case "Потеря жира":
            proteins_proc = 0.4
            fats_proc = 0.35
            carbohydrates_proc = 0.25
        case "Рекомпозиция":
            proteins_proc = 0.35
            fats_proc = 0.3
            carbohydrates_proc = 0.35
        case "Набор массы":
            proteins_proc = 0.3
            fats_proc = 0.3
            carbohydrates_proc = 0.4
        case "Поддержание веса":
            proteins_proc = 0.3
            fats_proc = 0.2
            carbohydrates_proc = 0.5

    proteins = int((quantity_calories * proteins_proc) / 4)
    fats = int((quantity_calories * fats_proc) / 9)
    carbohydrates = int((quantity_calories * carbohydrates_proc) / 4)

    return {
        "standard":
            {
                "calories": formule_mean_harris_mifflin,
                "proteins": proteins,
                "fats": fats,
                "carbohydrates": carbohydrates
            }
    }
