import pytest


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # исправила - добавила фикстуру и изменила проверку, т.к. в примере используется несуществующий метод.
    def test_add_new_book_add_two_books(self, collector):
        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две книги
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_add_new_book_with_existing_name_not_added(self, collector):
        # добавляем книгу
        collector.add_new_book('Book 1')
        # добавляем книгу с тем же названием
        collector.add_new_book('Book 1')
        # проверяем, что книга с существующим названием не добавляется
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_with_new_name_default_genre_is_empty(self, collector):
        # добавляем книгу
        collector.add_new_book('Book 1')
        # проверяем, что по умолчанию у новой книги нет жанра
        assert collector.get_book_genre('Book 1') == ''

    @pytest.mark.parametrize('name', ['', 'A' * 41])
    def test_add_new_book_when_name_is_invalid_not_added(self, collector, name):
        # добавляем книгу с неправильным именем
        collector.add_new_book(name)
        # проверяем, что книга с неправильным именем не добавляется
        assert len(collector.get_books_genre()) == 0

    @pytest.mark.parametrize("name, genre, expected", [
        ['Book 1', 'Фантастика', 'Фантастика'],
        ['Book 1', 'Unknown genre', ''],
        ['Unknown book', 'Ужасы', None],
    ])
    def test_set_book_genre(self, collector, name, genre, expected):
        # добавляем книгу
        collector.add_new_book('Book 1')
        # добавляем жанр
        collector.set_book_genre(name, genre)
        # проверяем, что жанр правильный в зависимости от переданных параметров name и genre
        assert collector.get_book_genre(name) == expected

    @pytest.mark.parametrize("books, genre, expected_books", [
        [[('Book 1', 'Фантастика'), ('Book 2', 'Ужасы')], 'Фантастика', ['Book 1']],
        [[('Book 1', 'Фантастика'), ('Book 2', 'Фантастика')], 'Фантастика', ['Book 1', 'Book 2']],
        [[('Book 1', 'Фантастика')], 'Ужасы', []],
    ])
    def test_get_books_with_specific_genre(self, collector, books, genre, expected_books):
        # добавляем книги из списков с тестовыми данными и задаем их жанры
        for name, book_genre in books:
            collector.add_new_book(name)
            collector.set_book_genre(name, book_genre)
        # проверяем, что результирующий список содержит только книги соответствующего жанра
        assert collector.get_books_with_specific_genre(genre) == expected_books

    @pytest.mark.parametrize("books, expected_books", [
        [[('Book 1', 'Фантастика'), ('Book 2', 'Ужасы')], ['Book 1']],
        [[('Book 1', 'Комедии'), ('Book 2', 'Мультфильмы')], ['Book 1', 'Book 2']],
        [[('Book 1', 'Ужасы')], []],
    ])
    def test_get_books_for_children(self, collector, books, expected_books):
        # добавляем книги из списков с тестовыми данными и задаем их жанры
        for name, book_genre in books:
            collector.add_new_book(name)
            collector.set_book_genre(name, book_genre)
        # проверяем, что результирующий список содержит только книги для детей
        assert collector.get_books_for_children() == expected_books

    @pytest.mark.parametrize('in_favorites', [True, False])
    def test_add_book_in_favorites_new_book_added(self, collector, in_favorites):
        collector.add_new_book('Book 1')
        collector.add_book_in_favorites('Book 1')
        # проверка добавления одной и той же книги два раза
        if in_favorites:
            collector.add_book_in_favorites('Book 1')
        assert collector.get_list_of_favorites_books() == ['Book 1']

    def test_add_book_in_favorites_unknown_book_not_added(self, collector):
        collector.add_book_in_favorites('Book 1')
        assert 'Book 1' not in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("books, book_to_delete, expected_books", [
        [['Book 1', 'Book 2'], 'Book 2', ['Book 1']],
        [['Book 1', 'Book 2'], 'Book 3', ['Book 1', 'Book 2']],
        [[], 'Book 1', []],
    ])
    def test_delete_book_from_favorites(self, collector, books, book_to_delete, expected_books):
        # добавление книг из тестовых данных в избранное
        if books:
            for name in books:
                collector.add_new_book(name)
                collector.add_book_in_favorites(name)
        # удаление книги из избранного
        collector.delete_book_from_favorites(book_to_delete)
        assert collector.get_list_of_favorites_books() == expected_books
