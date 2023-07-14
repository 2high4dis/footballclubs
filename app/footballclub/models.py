from typing import Iterable, Optional
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
import datetime
import string

alphabet = string.ascii_letters


def calculate_age(born: datetime.date):
    today = timezone.now()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def validate_string(value):
    if set(value).intersection(string.digits):
        raise ValidationError(
            ('String %(value)s contains forbidden symbols.'),
            params={'value': value},
        )


def validate_phone(value):
    if set(value).intersection(alphabet):
        raise ValidationError(
            ('Phone number cannot contain letters.')
        )


def validate_birth_date(value: datetime.date):
    age = calculate_age(value)
    if age < 15:
        raise ValidationError(
            ('The player must be at least 15 years of age.')
        )
    if value > datetime.date.today():
        raise ValidationError(
            ('The player must be born before the current date.')
        )


def validate_year_fact(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Invalid value entered.'
        )


class Position(models.Model):
    position = models.CharField(max_length=15, verbose_name='Position')

    def __str__(self):
        return self.position

    get_info = __str__

    def get_absolute_url(self):
        return reverse('positions', kwargs={'id': self.pk})


class City(models.Model):
    city = models.CharField(
        max_length=10, verbose_name='City', validators=[validate_string])

    def __str__(self):
        return self.city

    get_info = __str__

    def get_absolute_url(self):
        return reverse('cities', kwargs={'id': self.pk})


class League(models.Model):
    league = models.CharField(max_length=20, verbose_name='League name')

    def __str__(self):
        return self.league

    get_info = __str__

    def get_absolute_url(self):
        return reverse('leagues', kwargs={'id': self.pk})


class GameLevel(models.Model):
    game_level = models.CharField(max_length=25, verbose_name='Game level')

    def __str__(self):
        return self.game_level

    get_info = __str__

    def get_absolute_url(self):
        return reverse('gamelevels', kwargs={'id': self.pk})


class Country(models.Model):
    country = models.CharField(
        max_length=10, verbose_name='Country', validators=[validate_string])

    def __str__(self):
        return self.country

    get_info = __str__

    def get_absolute_url(self):
        return reverse('countries', kwargs={'id': self.pk})


class Club(models.Model):
    city_id = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='City')
    club = models.CharField(max_length=15, verbose_name='Club name')
    base = models.CharField(max_length=20, verbose_name='Training base')
    create_year = models.PositiveIntegerField(verbose_name='Create year', validators=[
                                              MaxValueValidator(timezone.now().year)])
    manager_phone = models.CharField(
        max_length=15, verbose_name='Manager`s phone', validators=[validate_phone])
    league_id = models.ForeignKey(
        League, on_delete=models.CASCADE, verbose_name='Лига')
    manager_last_name = models.CharField(
        max_length=15, verbose_name='Manager`s last name', validators=[validate_string])
    manager_first_name = models.CharField(
        max_length=15, verbose_name='Manager`s first name', validators=[validate_string])

    def __str__(self):
        return self.club

    get_info = __str__

    def get_manager_info(self):
        return f'{self.manager_last_name} {self.manager_first_name}'

    def get_absolute_url(self):
        return reverse('club_info', kwargs={'pk': self.pk})


class Player(models.Model):
    last_name = models.CharField(
        max_length=15, verbose_name='Last name', validators=[validate_string])
    first_name = models.CharField(
        max_length=15, verbose_name='First name', validators=[validate_string])
    position_id = models.ForeignKey(
        Position, on_delete=models.CASCADE, verbose_name='Position')
    birth_date = models.DateField(
        default=timezone.now, verbose_name='Birth date', validators=[validate_birth_date])
    club_id = models.ForeignKey(
        Club, on_delete=models.CASCADE, verbose_name='Club')
    year_fact = models.PositiveIntegerField(
        verbose_name='Year of joining the club', validators=[validate_year_fact, MaxValueValidator(timezone.now().year)])
    photo = models.ImageField(upload_to='static/img',
                              verbose_name='Player`s photo', blank=True)
    cost = models.PositiveIntegerField(verbose_name='Contract cost ($)')

    def save(self, *pargs, **kwargs):
        if self.year_fact - self.birth_date.year < 15:
            raise ValidationError(
                ('At the time of joining the club, the player must be at least 15 years of age.')
            )
        if self.year_fact < self.club_id.create_year:
            raise ValidationError(
                ('The player must join the club after the founding of the club.')
            )
        else:
            super(Player, self).save(*pargs, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name} - {self.position_id.position}'

    get_info = __str__

    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('player_info', kwargs={'pk': self.pk})


class EnemyTeam(models.Model):
    country_id = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Country')
    team_name = models.CharField(
        max_length=15, verbose_name='Enemy team name', validators=[validate_string])
    coach_last_name = models.CharField(
        max_length=15, verbose_name='Coach last name', validators=[validate_string])
    coach_first_name = models.CharField(
        max_length=15, verbose_name='Coach first name', validators=[validate_string])

    def __str__(self):
        return self.team_name

    def get_coach(self):
        return f'{self.coach_last_name} {self.coach_first_name}'

    def get_info(self):
        return f'{self.team_name}. Coach: {self.get_coach()}'

    def get_absolute_url(self):
        return reverse('enemy_teams', kwargs={'id': self.pk})


class Game(models.Model):
    gamelevel_id = models.ForeignKey(
        GameLevel, on_delete=models.CASCADE, verbose_name='Game Level')
    goals_skipped = models.PositiveIntegerField(verbose_name='Goals skipped')
    club_id = models.ForeignKey(
        Club, on_delete=models.CASCADE, verbose_name='Club')
    enemyteam_id = models.ForeignKey(
        EnemyTeam, on_delete=models.CASCADE, verbose_name='Enemy team')
    country_id = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Country of the game')
    game_date = models.DateField(
        default=timezone.now, verbose_name='Date of the game', validators=[MaxValueValidator(datetime.date.today())])

    def save(self, *pargs, **kwargs):
        if self.game_date.year < self.club_id.create_year:
            raise ValidationError(
                'The game cannot be played before the foundation of the club.'
            )
        else:
            super(Game, self).save(*pargs, **kwargs)

    def get_all_goals(self):
        attended_players = self.gameattend_set.all()
        return sum(player.goals_scored for player in attended_players)

    def __str__(self):
        return f'{self.club_id.club} vs. {self.enemyteam_id.team_name}. {self.country_id.country} {self.game_date}. Result: {self.get_all_goals()} : {self.goals_skipped}'

    get_info = __str__

    def get_absolute_url(self):
        return reverse('game_info', kwargs={'pk': self.pk})


class GameAttend(models.Model):
    player_id = models.ForeignKey(
        Player, on_delete=models.CASCADE, verbose_name='Player')
    game_id = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name='Game')
    goals_scored = models.PositiveIntegerField(verbose_name='Goals scored')
    attend = models.BooleanField(verbose_name='Was there any participation')
    salary = models.PositiveIntegerField(verbose_name='Game award ($)')

    def __str__(self):
        return f'{self.player_id.get_info()} Attended in the game: {self.game_id.get_info()} Scored: {self.goals_scored}'

    def get_info(self):
        return f'{self.game_id.get_info()} Scored: {self.goals_scored} time(-s)'

    def get_absolute_url(self):
        return reverse('game_attended', kwargs={'id': self.pk})
