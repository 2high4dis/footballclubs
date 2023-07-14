from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.views.generic import DetailView, ListView
from .models import Player, Club, Game, Position, Country, City, League, GameLevel, EnemyTeam, GameAttend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, DeleteView
from django.db.models import Q
from django.shortcuts import render

models_list = {
    'players': Player,
    'clubs': Club,
    'games': Game,
    'positions': Position,
    'countries': Country,
    'cities': City,
    'leagues': League,
    'gamelevels': GameLevel,
    'enemy_teams': EnemyTeam,
    'game_attended': GameAttend
}


def players_list(request):
    template_name = 'footballclub/players.html'
    set = Player.objects.all()
    context = {
        'players': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


class PlayerInfo(DetailView):
    template_name = 'footballclub/player_info.html'
    model = Player

    def get_queryset(self):
        return Player.objects.all()


def clubs_list(request):
    template_name = 'footballclub/clubs.html'
    set = Club.objects.all()
    context = {
        'clubs': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def gameattended_list(request, **kwargs):
    template_name = 'footballclub/game_attended.html'
    set = GameAttend.objects.all()
    context = {
        'game_attended': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


class ClubInfo(DetailView):
    template_name = 'footballclub/club_info.html'
    model = Club

    def get_queryset(self):
        return Club.objects.all()


def games_list(request):
    template_name = 'footballclub/games.html'
    set = Game.objects.all()
    context = {
        'games': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


class GameInfo(DetailView):
    template_name = 'footballclub/game_info.html'
    model = Game

    def get_queryset(self):
        return Game.objects.all()


def positions_list(request, **kwargs):
    template_name = 'footballclub/positions.html'
    set = Position.objects.all()
    context = {
        'positions': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def countries_list(request, **kwargs):
    template_name = 'footballclub/countries.html'
    set = Country.objects.all()
    context = {
        'countries': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def cities_list(request, **kwargs):
    template_name = 'footballclub/cities.html'
    set = City.objects.all()
    context = {
        'cities': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def leagues_list(request, **kwargs):
    template_name = 'footballclub/leagues.html'
    set = League.objects.all()
    context = {
        'leagues': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def gamelevels_list(request, **kwargs):
    template_name = 'footballclub/gamelevels.html'
    set = GameLevel.objects.all()
    context = {
        'gamelevels': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def enemyteam_list(request, **kwargs):
    template_name = 'footballclub/enemy_teams.html'
    set = EnemyTeam.objects.all()
    context = {
        'enemy_teams': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


class Search(ListView):
    template_name = 'footballclub/search.html'

    def get_queryset(self):
        model_name = self.request.GET.get('model')
        model = models_list[model_name]
        filter = self.request.GET.get('q')
        match model_name:
            case 'players':
                objects = model.objects.filter(Q(pk=int(filter)) | Q(cost=int(filter)) | Q(year_fact=filter)
                                               if filter.isdigit() else
                                                (Q(position_id__position__icontains=filter) |
                                                 Q(club_id__club__icontains=filter) |
                                                 Q(last_name__icontains=filter) |
                                                 Q(first_name__icontains=filter) |
                                                 Q(birth_date__icontains=filter)))
                result = {
                    'player_info': objects
                }
            case 'clubs':
                objects = model.objects.filter(Q(pk=int(filter)) | Q(create_year=filter)
                                               if filter.isdigit() else
                                                (Q(city_id__city__icontains=filter) |
                                                 Q(club__icontains=filter) |
                                                 Q(base__icontains=filter) |
                                                 Q(manager_phone__icontains=filter) |
                                                 Q(league_id__league__icontains=filter) |
                                                 Q(manager_last_name__icontains=filter) |
                                                 Q(manager_first_name__icontains=filter)))
                result = {
                    'club_info': objects
                }
            case 'games':
                objects = model.objects.filter(Q(pk=int(filter)) | Q(goals_skipped=filter)
                                               if filter.isdigit() else
                                                (Q(gamelevel_id__game_level__icontains=filter) |
                                                 Q(club_id__club__icontains=filter) |
                                                 Q(enemyteam_id__team_name__icontains=filter) |
                                                 Q(country_id__country__icontains=filter) |
                                                 Q(game_date__icontains=filter)))
                result = {
                    'game_info': objects
                }
            case 'positions':
                objects = model.objects.filter(Q(pk=int(filter))
                                               if filter.isdigit() else
                                                (Q(position__icontains=filter)))
                result = {
                    'positions': objects
                }
            case 'countries':
                objects = model.objects.filter(Q(pk=int(filter))
                                               if filter.isdigit() else
                                                (Q(country__icontains=filter)))
                result = {
                    'countries': objects
                }
            case 'cities':
                objects = model.objects.filter(Q(pk=int(filter))
                                               if filter.isdigit() else
                                                (Q(city__icontains=filter)))
                result = {
                    'cities': objects
                }
            case 'leagues':
                objects = model.objects.filter(Q(pk=int(filter))
                                               if filter.isdigit() else
                                                (Q(league__icontains=filter)))
                result = {
                    'leagues': objects
                }
            case 'gamelevels':
                objects = model.objects.filter(Q(pk=int(filter))
                                               if filter.isdigit() else
                                                (Q(game_level__icontains=filter)))
                result = {
                    'gamelevels': objects
                }
            case 'enemy_teams':
                objects = model.objects.filter(Q(pk=int(filter))
                                               if filter.isdigit() else
                                                (Q(country_id__country__icontains=filter) |
                                                 Q(team_name__icontains=filter) |
                                                 Q(coach_last_name__icontains=filter) |
                                                 Q(coach_first_name__icontains=filter)))
                result = {
                    'enemy_teams': objects
                }
            case 'game_attended':
                objects = model.objects.filter(Q(pk=int(filter)) | Q(goals_scored=filter) | Q(salary=filter)
                                               if filter.isdigit() else
                                                (Q(player_id__first_name__icontains=filter) |
                                                 Q(player_id__last_name__icontains=filter) |
                                                 Q(game_id__club_id__club__icontains=filter) |
                                                 Q(game_id__enemyteam_id__team_name=filter) |
                                                 Q(game_id__country_id__country=filter)))
                result = {
                    'game_attended': objects
                }

        return result


class CreateListView(LoginRequiredMixin, ListView):
    template_name = 'footballclub/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return {
            'players_create': 'Player',
            'clubs_create': 'Club',
            'games_create': 'Game',
            'positions_create': 'Position',
            'countries_create': 'Country',
            'cities_create': 'City',
            'leagues_create': 'League',
            'gamelevels_create': 'Game Level',
            'enemy_teams_create': 'Enemy Team',
            'game_attended_create': 'Game Attend'
        }


class PlayerCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = Player
    fields = [
        'last_name', 'first_name', 'position_id',
        'birth_date', 'club_id', 'year_fact', 'photo', 'cost'
    ]


class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = Player
    fields = [
        'last_name', 'first_name', 'position_id',
        'birth_date', 'club_id', 'year_fact', 'photo', 'cost'
    ]


class PlayerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = Player


class ClubCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = Club
    fields = [
        'city_id', 'club', 'base', 'create_year',
        'manager_phone', 'league_id', 'manager_last_name', 'manager_first_name'
    ]


class ClubUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = Club
    fields = [
        'city_id', 'club', 'base', 'create_year',
        'manager_phone', 'league_id', 'manager_last_name', 'manager_first_name'
    ]


class ClubDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = Club


class GameCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = Game
    fields = [
        'gamelevel_id', 'goals_skipped', 'club_id', 'enemyteam_id',
        'country_id', 'game_date'
    ]


class GameUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = Game
    fields = [
        'gamelevel_id', 'goals_skipped', 'club_id', 'enemyteam_id',
        'country_id', 'game_date'
    ]


class GameDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = Game


class PositionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = Position
    fields = [
        'position'
    ]


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = Position
    fields = [
        'position'
    ]


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = Position


class CountryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = Country
    fields = [
        'country'
    ]


class CountryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = Country
    fields = [
        'country'
    ]


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = Country


class CityCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = City
    fields = [
        'city'
    ]


class CityUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = City
    fields = [
        'city'
    ]


class CityDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = City


class LeagueCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = League
    fields = [
        'league'
    ]


class LeagueUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = League
    fields = [
        'league'
    ]


class LeagueDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = League


class GameLevelCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = GameLevel
    fields = [
        'game_level'
    ]


class GameLevelUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = GameLevel
    fields = [
        'game_level'
    ]


class GameLevelDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = GameLevel


class EnemyTeamCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = EnemyTeam
    fields = [
        'country_id', 'team_name', 'coach_last_name', 'coach_first_name'
    ]


class EnemyTeamUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = EnemyTeam
    fields = [
        'country_id', 'team_name', 'coach_last_name', 'coach_first_name'
    ]


class EnemyTeamDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = EnemyTeam


class GameAttendCreateView(LoginRequiredMixin, CreateView):
    template_name = 'footballclub/item_form.html'
    model = GameAttend
    fields = [
        'player_id', 'game_id', 'goals_scored', 'attend',
        'salary'
    ]


class GameAttendUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'footballclub/item_form.html'
    model = GameAttend
    fields = [
        'player_id', 'game_id', 'goals_scored', 'attend',
        'salary'
    ]


class GameAttendDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'footballclub/delete_confirmation.html'
    success_url = '/'
    model = GameAttend


class ClubRatingView(ListView):
    template_name = 'footballclub/rating.html'
    context_object_name = 'clubs_rating'

    def get_queryset(self):
        name_map = {
            'SUM(goals_scored)': 'goals_sum'
        }
        set = Club.objects.raw("""
        SELECT club.id, club, SUM(goals_scored)
        FROM footballclub_club AS club
        INNER JOIN footballclub_game AS game ON game.club_id_id = club.id
        INNER JOIN footballclub_gameattend AS gameattend ON gameattend.game_id_id = game.id
        GROUP BY club.id, club
        ORDER BY SUM(goals_scored) DESC
        LIMIT 3
        """, translations=name_map)
        return set


def player_rating_view(request):
    template_name = 'footballclub/player_rating.html'
    club = 'FC Shakhtar'
    if request.method == 'POST':
        club = request.POST.get('club')

    name_map = {
        '(last_name || " " || first_name)': 'full_name',
        'SUM(goals_scored)': 'goals_sum'
    }
    set = Club.objects.raw("""
        SELECT club.id, club, player.id AS player_id, (last_name || " " || first_name), SUM(goals_scored)
        FROM footballclub_player AS player
        LEFT JOIN footballclub_club AS club ON player.club_id_id = club.id
        INNER JOIN footballclub_gameattend AS gameattend ON gameattend.player_id_id = player.id
        WHERE club == %s
        GROUP BY club.id, club, player_id, (last_name || " " || first_name)
        ORDER BY SUM(goals_scored) DESC
        LIMIT 3
        """, [club], translations=name_map)

    context = {
        'clubs_rating': set,
        'club': club
    }
    return render(request=request, template_name=template_name, context=context)


class PlayerRatingView(ListView):
    template_name = 'footballclub/player_rating.html'
    context_object_name = 'clubs_rating'

    def get_queryset(self):
        name_map = {
            '(last_name || " " || first_name)': 'full_name'
        }
        set = Club.objects.raw("""
        SELECT club, (last_name || " " || first_name), goals_scored
        FROM footballclub_player AS player
        LEFT JOIN footballclub_club AS club ON player.club_id_id = club.id
        INNER JOIN footballclub_gameattend AS gameattend ON gameattend.player_id_id = player.id
        WHERE club == %s
        ORDER BY goals_scored DESC
        LIMIT 3
        """, translations=name_map)
        return set


class ClubStatsView(ListView):
    template_name = 'footballclub/club_stats.html'
    context_object_name = 'clubs_stats'

    def get_queryset(self):
        name_map = {
            'CEIL(AVG(goals_scored))': 'avg_scored',
            'CEIL(AVG(goals_skipped))': 'avg_skipped',
        }
        set = Club.objects.raw("""
        SELECT club.id, club, CEIL(AVG(goals_scored)), CEIL(AVG(goals_skipped))
        FROM footballclub_club AS club
        INNER JOIN footballclub_game AS game ON game.club_id_id = club.id
        INNER JOIN footballclub_gameattend AS gameattend ON gameattend.game_id_id = game.id
        GROUP BY club
        ORDER BY club
        """, translations=name_map)
        return set


class PlayerStatsView(ListView):
    template_name = 'footballclub/player_stats.html'
    context_object_name = 'players_stats'

    def get_queryset(self):
        name_map = {
            'CEIL(AVG(goals_scored))': 'avg_scored',
            'CEIL(AVG(goals_skipped))': 'avg_skipped',
            '(last_name || " " || first_name)': 'full_name',
        }
        set = Club.objects.raw("""
        SELECT club.id, club, player.id AS player_id, (last_name || " " || first_name), CEIL(AVG(goals_scored)), CEIL(AVG(goals_skipped))
        FROM footballclub_club AS club
        INNER JOIN footballclub_game AS game ON game.club_id_id = club.id
        INNER JOIN footballclub_gameattend AS gameattend ON gameattend.game_id_id = game.id
        INNER JOIN footballclub_player AS player ON player.id = gameattend.player_id_id
        GROUP BY player.id, (last_name || " " || first_name)
        ORDER BY club
        """, translations=name_map)
        return set


def gamecount_view(request):
    template_name = 'footballclub/game_count.html'

    if request.method == 'GET':
        name_map = {
            'COUNT(*)': 'game_count',
        }
        set = Club.objects.raw("""
            SELECT club.id, club, COUNT(*)
            FROM footballclub_game AS game
            LEFT JOIN footballclub_club AS club ON club.id = game.club_id_id
            WHERE game_date BETWEEN "2021-01-01" AND "2021-12-31" AND club = "FC Shakhtar"
            GROUP BY club
            ORDER BY club
            """, translations=name_map)
        context = {
            'game_count': set,
        }
        return render(request=request, template_name=template_name, context=context)

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        club = request.POST.get('club')
        name_map = {
            'COUNT(*)': 'game_count',
        }
        set = Club.objects.raw("""
            SELECT club.id, club, COUNT(*)
            FROM footballclub_game AS game
            LEFT JOIN footballclub_club AS club ON club.id = game.club_id_id
            WHERE (game_date BETWEEN %s AND %s) AND club = %s
            GROUP BY club
            ORDER BY club
            """, [start, end, club], translations=name_map)

        context = {
            'game_count': set,
            'start': start,
            'end': end,
            'club': club
        }

        return render(request=request, template_name=template_name, context=context)


def finances_view(request):
    template_name = 'footballclub/finances.html'

    if request.method == 'GET':
        name_map = {
            'SUM(salary)': 'total_salary',
        }
        set = Club.objects.raw("""
        SELECT club.id, club, SUM(salary)
        FROM footballclub_game AS game
        LEFT JOIN footballclub_club AS club ON club.id = game.club_id_id
        INNER JOIN footballclub_gameattend AS gameattend ON game.id = gameattend.game_id_id
        WHERE game_date BETWEEN "2021-01-01" AND "2021-12-31" AND club = "FC Shakhtar"
        GROUP BY club.id, club
        ORDER BY club
        """, translations=name_map)

        context = {
            'clubs_finances': set,
        }
        return render(request=request, template_name=template_name, context=context)

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        club = request.POST.get('club')
        name_map = {
            'SUM(salary)': 'total_salary',
        }
        set = Club.objects.raw("""
        SELECT club.id, club, SUM(salary)
        FROM footballclub_game AS game
        LEFT JOIN footballclub_club AS club ON club.id = game.club_id_id
        INNER JOIN footballclub_gameattend AS gameattend ON game.id = gameattend.game_id_id
        WHERE (game_date BETWEEN %s AND %s) AND club = %s
        GROUP BY club.id, club
        ORDER BY club
        """, [start, end, club], translations=name_map)

        context = {
            'clubs_finances': set,
            'start': start,
            'end': end,
            'club': club
        }

        return render(request=request, template_name=template_name, context=context)


def clubs_by_cities(request):
    template_name = 'footballclub/clubs_by_cities.html'
    name_map = {
        'city.id': 'id',
    }
    set = City.objects.raw('''
        SELECT city.id, city, club.id AS club_id, club
        FROM footballclub_city AS city
        LEFT JOIN footballclub_club AS club ON city.id == club.city_id_id
        ORDER BY city
        ''', translations=name_map)

    context = {
        'cities': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def enemies_by_countries(request):
    template_name = 'footballclub/enemies_by_countries.html'
    name_map = {
        'country.id': 'id',
    }
    set = Country.objects.raw('''
        SELECT country.id, country, enemyteam.id AS enemyteam_id, team_name
        FROM footballclub_country AS country
        LEFT JOIN footballclub_enemyteam AS enemyteam ON country.id == enemyteam.country_id_id
        ORDER BY country
        ''', translations=name_map)

    context = {
        'countries': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def players_by_club(request):
    template_name = 'footballclub/players_by_club.html'
    name_map = {
        'player.id': 'id',
    }

    if request.method == 'GET':
        club = 'FC Shakhtar'
        set = Player.objects.raw('''
            SELECT player.id, last_name, first_name
            FROM footballclub_player AS player
            WHERE club_id_id == (SELECT id FROM footballclub_club AS club WHERE club.club == "FC Shakhtar")
            ''', translations=name_map)

    if request.method == 'POST':
        club = request.POST.get('club')
        set = Player.objects.raw('''
            SELECT player.id, last_name, first_name, birth_date
            FROM footballclub_player AS player
            WHERE club_id_id == (SELECT id FROM footballclub_club AS club WHERE club.club == %s)
            ''', [club], translations=name_map)

    context = {
        'players': set,
        'club': club,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def players_above_average(request):
    template_name = 'footballclub/players_above_average.html'
    name_map = {
        'player.id': 'id',
    }
    set = Player.objects.raw('''
        SELECT player.id, (last_name || " " || first_name) AS full_name, SUM(goals_scored) AS goals_sum
        FROM footballclub_player AS player
        INNER JOIN footballclub_gameattend AS gameattend ON gameattend.player_id_id == player.id
        GROUP BY player.id, full_name
        HAVING goals_sum > (SELECT CEIL(AVG(goals_scored)) FROM footballclub_gameattend)
        ORDER BY goals_sum DESC
        ''', translations=name_map)

    context = {
        'players': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def above_average_by_club(request):
    template_name = 'footballclub/above_average_by_club.html'
    name_map = {
        'player.id': 'id',
    }

    if request.method == 'GET':
        club = 'FC Shakhtar'

    if request.method == 'POST':
        club = request.POST.get('club')

    set = Player.objects.raw('''
        SELECT player.id, (last_name || " " || first_name) AS full_name, club, SUM(goals_scored) AS goals_sum
        FROM footballclub_player AS player
        INNER JOIN footballclub_gameattend AS gameattend ON gameattend.player_id_id == player.id
        INNER JOIN footballclub_club AS club ON club.id == player.club_id_id
        GROUP BY player.id, full_name, club
        HAVING goals_sum > (SELECT CEIL(AVG(goals_scored)) FROM footballclub_gameattend) AND club == %s
        ORDER BY goals_sum DESC
        ''', [club], translations=name_map)

    context = {
        'players': set,
        'club': club,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)


def club_games(request):
    template_name = 'footballclub/club_games.html'
    name_map = {
        'club.id': 'id',
    }
    set = Club.objects.raw('''
        SELECT club.id, club, (SELECT COUNT(*) FROM footballclub_game AS game 
                                WHERE game.club_id_id == club.id) AS game_count
        FROM footballclub_club AS club
        ORDER BY game_count DESC
        ''', translations=name_map)

    context = {
        'clubs': set,
        'count': len(set)
    }

    return render(request=request, template_name=template_name, context=context)
