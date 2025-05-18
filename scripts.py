from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation, Subject
from random import choice
from django.core.exceptions import ObjectDoesNotExist

def get_schoolkid(full_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        return schoolkid
    except ObjectDoesNotExist:
        print('Имя введено не корректно')


def fix_marks(full_name):
    schoolkid = get_schoolkid(full_name)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    bad_marks.update(points=5)


def remove_chastisements(full_name):
    schoolkid = get_schoolkid(full_name)
    chastisements =  Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(full_name,subject=None):
    schoolkid = get_schoolkid(full_name)
    if subject:
        subjects = Subject.objects.filter(
                year_of_study=schoolkid.year_of_study,
                title__contains=subject
        )
        if not subjects:
            raise ValueError("Предмет не найден")
        else:
            subject=subjects[0]
    else:
        subjects = Subject.objects.filter(year_of_study=schoolkid.year_of_study)
        subject = choice(subjects)
    lessons = Lesson.objects.filter(
        group_letter=schoolkid.group_letter,
        year_of_study=schoolkid.year_of_study,
        subject=subject
    )
    lessons.order_by('date')
    last_lesson=lessons.last()
    commendation = ['Молодец!',
                    'Отлично!',
                    'Хорошо!',
                    'Великолепно!',
                    'Прекрасно!',
                    'Именно этого я давно ждал от тебя!',
                    'Сказано здорово – просто и ясно!',
                    'Ты, как всегда, точен!',
                    'Очень хороший ответ!',
                    'Талантливо!',
                    'Ты сегодня прыгнул выше головы!',
                    'Я поражен!',
                    'Уже существенно лучше!',
                    'Замечательно!',
                    'Прекрасное начало!',
                    'Так держать!',
                    'Ты на верном пути!',
                    'Здорово!',
                    'Это как раз то, что нужно!',
                    'Я тобой горжусь!',
                    'С каждым разом у тебя получается всё лучше!',
                    'Мы с тобой не зря поработали!',
                    'Я вижу, как ты стараешься!',
                    'Ты растешь над собой!',
                    'Ты многое сделал, я это вижу!',
                    'Теперь у тебя точно все получится!'
    ]
    Commendation.objects.create(
        text=choice(commendation),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )
