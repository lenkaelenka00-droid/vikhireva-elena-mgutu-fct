import random
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class QuestionType(Enum):
    """Типы вопросов"""
    COMMUNICATION = "Коммуникация"
    TEAMWORK = "Командная работа"
    LEADERSHIP = "Лидерство"
    CONFLICT = "Разрешение конфликтов"
    FEEDBACK = "Работа с обратной связью"


@dataclass
class Answer:
    """Модель ответа"""
    text: str
    is_correct: bool
    explanation: str = ""


class SoftSkillQuestion:
    """Класс, представляющий вопрос по soft skills"""
    def __init__(self, question_text: str, answers: List[Answer],
                 question_type: QuestionType, difficulty: int = 1):
        self.question_text = question_text
        self.answers = answers
        self.question_type = question_type
        self.difficulty = difficulty
        self._validate_answers()

    def _validate_answers(self) -> None:
        """Проверяет, что есть хотя бы один правильный ответ"""
        if not any(answer.is_correct for answer in self.answers):
            raise ValueError("Должен быть хотя бы один правильный ответ")

    def get_correct_answers(self) -> List[Answer]:
        """Возвращает список правильных ответов"""
        return [answer for answer in self.answers if answer.is_correct]

    def check_answer(self, answer_index: int) -> bool:
        """Проверяет, правильный ли ответ по индексу"""
        if 0 <= answer_index < len(self.answers):
            return self.answers[answer_index].is_correct
        return False

    def __str__(self) -> str:
        return f"[{self.question_type.value}] {self.question_text}"


class QuestionFactory:
    """Фабрика для создания вопросов"""

    @staticmethod
    def create_communication_question() -> SoftSkillQuestion:
        return SoftSkillQuestion(
            question_text="Как вы поступите, если коллега постоянно срывает сроки сдачи общей работы?",
            answers=[
                Answer("Сделаю работу за него, чтобы не подвести команду", False,
                      "Это может привести к выгоранию и не решает корень проблемы"),
                Answer("Открыто обсужу проблему с коллегой и предложу помощь", True,
                      "Прямая коммуникация помогает найти причины проблемы и совместно решить ее"),
                Answer("Немедленно доложу руководителю о ситуации", False,
                      "Сначала стоит попытаться решить вопрос напрямую с коллегой")
            ],
            question_type=QuestionType.COMMUNICATION,
            difficulty=2
        )

    @staticmethod
    def create_teamwork_question() -> SoftSkillQuestion:
        return SoftSkillQuestion(
            question_text="Во время совещания возникает конфликт между двумя членами команды. Ваши действия?",
            answers=[
                Answer("Прерву дискуссию и перенесу обсуждение на другое время", False,
                      "Может отложить, но не решить проблему"),
                Answer("Выслушаю обе стороны и предложу компромиссное решение", True,
                      "Активное посредничество помогает найти взаимоприемлемое решение"),
                Answer("Предоставлю участникам самостоятельно разобраться в конфликте", False,
                      "Без посредничества конфликт может усугубиться")
            ],
            question_type=QuestionType.CONFLICT,
            difficulty=3
        )

    @staticmethod
    def create_random_question() -> SoftSkillQuestion:
        """Создает случайный вопрос"""
        creators = [
            QuestionFactory.create_communication_question,
            QuestionFactory.create_teamwork_question
        ]
        return random.choice(creators)()


class User:
    """Класс пользователя"""

    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.answered_questions = []

    def add_score(self, points: int) -> None:
        """Добавляет очки пользователю"""
        self.score += points

    def __str__(self) -> str:
        return f"Пользователь: {self.name}, Очки: {self.score}"


class Quiz(ABC):
    """Абстрактный класс для викторин"""

    @abstractmethod
    def ask_question(self) -> bool:
        """Задает вопрос и возвращает True если ответ правильный"""
        pass

    @abstractmethod
    def get_score(self) -> int:
        """Возвращает текущий счет"""
        pass


class SoftSkillsQuiz(Quiz):
    """Конкретная реализация викторины по soft skills"""

    def __init__(self, user: User, questions: Optional[List[SoftSkillQuestion]] = None):
        self.user = user
        self.questions = questions or self._load_default_questions()
        self.current_question_index = 0

    def _load_default_questions(self) -> List[SoftSkillQuestion]:
        """Загружает вопросы по умолчанию"""
        return [
            QuestionFactory.create_communication_question(),
            QuestionFactory.create_teamwork_question(),
            SoftSkillQuestion(
                question_text="Как вы будете действовать при получении негативной обратной связи о своей работе?",
                answers=[
                    Answer("Защищаю свою позицию и объясню, почему поступил именно так", False,
                          "Защита может восприниматься как неготовность к развитию"),
                    Answer("Выслушаю критику, задам уточняющие вопросы и разработаю план улучшений", True,
                          "Проактивный подход к обратной связи показывает зрелость и готовность развиваться"),
                    Answer("Поблагодарю за обратную связь, но не буду менять свой подход к работе", False,
                          "Игнорирование обратной связи мешает профессиональному росту")
                ],
                question_type=QuestionType.FEEDBACK,
                difficulty=2
            )
        ]

    def ask_question(self) -> bool:
        """Задает текущий вопрос"""
        if self.current_question_index >= len(self.questions):
            return False

        question = self.questions[self.current_question_index]
        print(f"\n{'='*60}")
        print(f"Вопрос {self.current_question_index + 1}: {question}")
        print(f"Сложность: {'★' * question.difficulty}")
        print('='*60)

        # Выводим варианты ответов
        for i, answer in enumerate(question.answers, 1):
            print(f"{i}. {answer.text}")

        # Получаем ответ пользователя
        while True:
            try:
                choice = int(input(f"\n{self.user.name}, выберите вариант (1-{len(question.answers)}): "))
                if 1 <= choice <= len(question.answers):
                    selected_answer = question.answers[choice - 1]

                    # Проверяем ответ
                    if selected_answer.is_correct:
                        points = question.difficulty * 10
                        self.user.add_score(points)
                        print(f"\n✅ Верно! +{points} очков")
                        print(f"Объяснение: {selected_answer.explanation}")
                    else:
                        print(f"\n❌ Неверно!")
                        print(f"Объяснение: {selected_answer.explanation}")

                        # Показываем правильный ответ
                        correct = question.get_correct_answers()
                        if correct:
                            print(f"Правильный ответ: {correct[0].text}")

                    self.current_question_index += 1
                    self.user.answered_questions.append(question)
                    return selected_answer.is_correct

                print(f"Пожалуйста, введите число от 1 до {len(question.answers)}")
            except ValueError:
                print("Пожалуйста, введите число")

    def get_score(self) -> int:
        """Возвращает текущий счет"""
        return self.user.score

    def run_quiz(self) -> None:
        """Запускает полную викторину"""
        print(f"\nДобро пожаловать в викторину по Soft Skills, {self.user.name}!")
        print("Ответьте на все вопросы для проверки ваших навыков.\n")

        while self.current_question_index < len(self.questions):
            self.ask_question()

        self._show_results()

    def _show_results(self) -> None:
        """Показывает результаты викторины"""
        print("\n" + "="*60)
        print("РЕЗУЛЬТАТЫ ВИКТОРИНЫ")
        print("="*60)
        print(f"Игрок: {self.user.name}")
        print(f"Итоговый счет: {self.user.score}")
        print(f"Пройдено вопросов: {len(self.user.answered_questions)}")

        # Анализ по категориям
        categories = {}
        for question in self.user.answered_questions:
            cat = question.question_type.value
            categories[cat] = categories.get(cat, 0) + 1

        print("\nКатегории вопросов:")
        for category, count in categories.items():
            print(f"  {category}: {count} вопросов")

        max_score = sum(q.difficulty * 10 for q in self.questions)
        percentage = (self.user.score / max_score * 100) if max_score > 0 else 0

        print(f"\nВы набрали {percentage:.1f}% от максимального результата!")

        if percentage >= 80:
            print("🎉 Отличный результат! Ваши soft skills на высоком уровне.")
        elif percentage >= 60:
            print("👍 Хороший результат! Есть куда развиваться.")
        else:
            print("📚 Есть над чем поработать. Рекомендуем уделить больше внимания soft skills.")


# Пример использования
if __name__ == "__main__":
    # Создаем пользователя
    user = User("Алексей")

    # Создаем и запускаем викторину
    quiz = SoftSkillsQuiz(user)
    quiz.run_quiz()

    # Дополнительный пример с фабрикой
    print("\n" + "="*60)
    print("ДОПОЛНИТЕЛЬНЫЙ ВОПРОС ОТ ФАБРИКИ")
    print("="*60)

    random_question = QuestionFactory.create_random_question()
    print(f"Вопрос: {random_question}")
    for i, answer in enumerate(random_question.answers, 1):
        print(f"{i}. {answer.text}")
