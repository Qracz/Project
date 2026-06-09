class Movie:
    def __init__(self, title, duration_min):
        self.title = title
        self.duration_min = duration_min

class Screening:
    def __init__(self, movie, total_seats, base_price):
        self.movie = movie
        self.total_seats = total_seats
        self.base_price = base_price
        self.available_seats = total_seats
        self.reserved_seats = []

class CinemaManager:
    def __init__(self):
        self.movies = []
        self.screenings = []

    def add_movie(self, title, duration_min):
        if not title or duration_min <= 0:
            return False
        if any(m.title == title for m in self.movies):
            return False 
        new_movie = Movie(title, duration_min)
        self.movies.append(new_movie)
        return True

    def create_screening(self, movie_title, total_seats, base_price):
        movie = next((m for m in self.movies if m.title == movie_title), None)
        if not movie or total_seats <= 0 or base_price < 0:
            return None
        new_screening = Screening(movie, total_seats, base_price)
        self.screenings.append(new_screening)
        return new_screening

    def book_seats(self, screening, num_seats):
        if num_seats <= 0 or screening not in self.screenings:
            return False
        if screening.available_seats >= num_seats:
            screening.available_seats -= num_seats
            return True
        return False

    def calculate_total_price(self, base_price, num_seats, discount_type):
        if num_seats <= 0 or base_price < 0:
            return 0.0
        total = base_price * num_seats
        if discount_type == "STUDENT":
            return round(total * 0.5, 2) 
        elif discount_type == "SENIOR":
            return round(total * 0.7, 2) 
        return round(total, 2)

    def cancel_booking(self, screening, num_seats):
        if screening not in self.screenings or num_seats <= 0:
            return False
        if screening.available_seats + num_seats > screening.total_seats:
            return False
        screening.available_seats += num_seats
        return True