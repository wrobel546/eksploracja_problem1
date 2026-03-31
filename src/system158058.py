from collections import defaultdict
from RatingSystem import RatingSystem


class MySystem(RatingSystem):
    def __init__(self):
        super().__init__()
        self.movie_sum = defaultdict(float)
        self.movie_cnt = defaultdict(int)

        total_sum = 0.0
        total_cnt = 0

        for movie_id, ratings in self.movie_ratings.items():
            if not ratings:
                continue
            s = float(sum(ratings))
            c = len(ratings)
            self.movie_sum[int(movie_id)] = s
            self.movie_cnt[int(movie_id)] = c
            total_sum += s
            total_cnt += c

        self.global_mean = total_sum / total_cnt if total_cnt else 2.5

        self.movie_bias = {}
        MOVIE_REG = 20.0

        for movie_id, count in self.movie_cnt.items():
            s = self.movie_sum[movie_id]
            self.movie_bias[movie_id] = (s - count * self.global_mean) / (MOVIE_REG + count)

    USER_REG = 15.0
    def build_user_bias(self, user):
        if not user.ratings:
            return 0.0
        bias_sum = 0.0
        bias_cnt = 0
        for movie_id, rating in user.ratings.items():
            movie_id = int(movie_id)
            bias_sum += float(rating) - self.global_mean - self.movie_bias.get(movie_id, 0.0)
            bias_cnt += 1
        return bias_sum / (self.USER_REG + bias_cnt)

    @staticmethod
    def _clip(x):
        if x < 0.5:
            return 0.5
        if x > 5.0:
            return 5.0
        return x

    @staticmethod
    def _normalize_to_half_step(x):
        # 0.5, 1.0, 1.5, ..., 5.0
        x = MySystem._clip(float(x))
        return int(x * 2.0 + 0.5) / 2.0

    def rate(self, user, movie):
        movie_id = int(movie)
        n = self.movie_cnt.get(movie_id, 0)
        movie_bias = self.movie_bias.get(movie_id, 0.0)
        user_bias = self.build_user_bias(user)
        base = self.global_mean
        rate = base + movie_bias + user_bias
        return self._normalize_to_half_step(rate)

    def __str__(self):
        return "System created by 158058 and 155077"

