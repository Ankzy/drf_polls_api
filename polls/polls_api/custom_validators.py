from .models import Answer, Question, Option

def question_already_answered(data):
    if Answer.objects.filter(question__id=data['question'], user=data['user']):
            return (data['user'], data['question'])
    return False

def more_than_one_answer_to_same(data):
    questions_set = set()
    for answer in data:
        questions_set.add(answer['question'])
    if len(questions_set) < len(data):
        return True
    return False

def different_users(data):
    users_set = set()
    for answer in data:
        users_set.add(answer['user'])
    if len(users_set) > 1:
        return True
    return False

def choice_custom_validator(data):
    for answer in data:
        question = Question.objects.get(id=answer['question'])
        if question.type == "TEXT":
            if answer['text'] is None or answer['text']=='':
                return {
                    'error': 'Question {}. Text answer is required for the text type question.'.format(
                        question.id)}
        if question.type == "SNGL":
            if not isinstance(answer['choice_id'], int):
                return {
                    'error': 'Question {}. Answer to single-choice question (choice_id field) must be integer.'.format(
                        question.id)}
            if not Option.objects.filter(id=answer['choice_id'], question__id=question.id):
                return {
                    'error': 'There is no answer option with id {} in question with id {}'.format(
                        answer['choice_id'], question.id)}
        if question.type == "MULT":
            if not isinstance(answer['choice_id'], list):
                return {
                    'error': 'Question {}. Answer to multiple-choice question (choice_id field) must be list.'.format(
                        question.id)}
            for choice in answer['choice_id']:
                if not isinstance(choice, int):
                    return {
                        'error': 'Question {}. Answer to multiple-choice question must be list of integers.'.format(
                            question.id)}
                if not Option.objects.filter(id=choice, question__id=question.id):
                    return {
                        'error': 'There is no answer option with id {} in question with id {}'.format(
                            choice, question.id)}
    return False

def poll_question_conformity(data):
    for answer in data:
        if not Question.objects.filter(id=answer['question'], poll__id=answer['poll']):
            return {
                'error': 'There is no question with id {} in poll with id {}'.format(
                    answer['question'], answer['poll']
                )}
    return False