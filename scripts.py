from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation, Subject
from random import choice
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from commendation import commendation_texts

def get_schoolkid(full_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        return schoolkid
    except ObjectDoesNotExist:
        print('Имя введено не корректно')
    except MultipleObjectsReturned:
        print('Найдено более чем 1 ученик')


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
    if not schoolkid:
        raise ValueError("Ученик не найден")
    if subject:
        subjects = Subject.objects.filter(
                year_of_study=schoolkid.year_of_study,
                title__contains=subject
        )
    else:
        subjects = Subject.objects.filter(year_of_study=schoolkid.year_of_study)
    if not subjects:
        raise ValueError("Предмет не найден")
    subject = choice(subjects)
    lessons = Lesson.objects.filter(
        group_letter=schoolkid.group_letter,
        year_of_study=schoolkid.year_of_study,
        subject=subject
    )
    last_lesson=lessons.order_by('date').last()
    if not last_lesson:
        raise ValueError('Урок не найден')
    Commendation.objects.create(
        text=choice(commendation_texts),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )
