import unittest
from cinema_system import CinemaManager, Movie, Screening

class TestCinemaSystem(unittest.TestCase):

    def setUp(self):
        self.manager = CinemaManager()

    def test_add_movie_success(self):
        self.assertTrue(self.manager.add_movie("Inception", 148))
        self.assertEqual(len(self.manager.movies), 1)

    def test_add_movie_duplicate(self):
        self.manager.add_movie("Inception", 148)
        self.assertFalse(self.manager.add_movie("Inception", 148))

    def test_add_movie_invalid_duration(self):
        self.assertFalse(self.manager.add_movie("Avatar", -5))

    def test_add_movie_empty_title(self):
        self.assertFalse(self.manager.add_movie("", 120))


    def test_create_screening_success(self):
        self.manager.add_movie("Inception", 148)
        screening = self.manager.create_screening("Inception", 100, 25.0)
        self.assertIsNotNone(screening)
        self.assertEqual(screening.movie.title, "Inception")

    def test_create_screening_movie_not_found(self):
        screening = self.manager.create_screening("NonExistent", 100, 25.0)
        self.assertIsNone(screening)  

    def test_create_screening_invalid_seats(self):
        self.manager.add_movie("Inception", 148)
        screening = self.manager.create_screening("Inception", -10, 25.0)
        self.assertIsNone(screening)  

    def test_create_screening_invalid_price(self):
        self.manager.add_movie("Inception", 148)
        screening = self.manager.create_screening("Inception", 100, -5.0)
        self.assertIsNone(screening)  


    def test_book_seats_success(self):
        self.manager.add_movie("Inception", 148)
        scr = self.manager.create_screening("Inception", 50, 20.0)
        self.assertTrue(self.manager.book_seats(scr, 5))
        self.assertEqual(scr.available_seats, 45)

    def test_book_seats_insufficient_space(self):
        self.manager.add_movie("Inception", 148)
        scr = self.manager.create_screening("Inception", 10, 20.0)
        self.assertFalse(self.manager.book_seats(scr, 15))

    def test_book_seats_invalid_number(self):
        self.manager.add_movie("Inception", 148)
        scr = self.manager.create_screening("Inception", 50, 20.0)
        self.assertFalse(self.manager.book_seats(scr, -2))

    def test_book_seats_unregistered_screening(self):
        standalone_scr = Screening(Movie("Test", 100), 50, 20.0)
        self.assertFalse(self.manager.book_seats(standalone_scr, 2))


    def test_price_regular(self):
        price = self.manager.calculate_total_price(30.0, 3, "REGULAR")
        self.assertEqual(price, 90.0)

    def test_price_student_discount(self):
        price = self.manager.calculate_total_price(30.0, 2, "STUDENT")
        self.assertEqual(price, 30.0) 

    def test_price_senior_discount(self):
        price = self.manager.calculate_total_price(20.0, 2, "SENIOR")
        self.assertEqual(price, 28.0) 

    def test_price_invalid_inputs(self):
        price = self.manager.calculate_total_price(-10.0, 2, "REGULAR")
        self.assertEqual(price, 0.0)


    def test_cancel_booking_success(self):
        self.manager.add_movie("Inception", 148)
        scr = self.manager.create_screening("Inception", 50, 20.0)
        self.manager.book_seats(scr, 10) 
        self.assertTrue(self.manager.cancel_booking(scr, 5))
        self.assertEqual(scr.available_seats, 45)

    def test_cancel_booking_exceed_total_capacity(self):
        self.manager.add_movie("Inception", 148)
        scr = self.manager.create_screening("Inception", 50, 20.0)
        self.assertFalse(self.manager.cancel_booking(scr, 5))

    def test_cancel_booking_invalid_seats(self):
        self.manager.add_movie("Inception", 148)
        scr = self.manager.create_screening("Inception", 50, 20.0)
        self.assertFalse(self.manager.cancel_booking(scr, -5))

    def test_cancel_booking_unregistered_screening(self):
        standalone_scr = Screening(Movie("Test", 100), 50, 20.0)
        self.assertFalse(self.manager.cancel_booking(standalone_scr, 2))

if __name__ == '__main__':
    unittest.main()