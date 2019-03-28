import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	# Инициализирует pygame, settings и объект экрана. 
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')
	# Создание корабля.
	ship = Ship(ai_settings,screen)
	# Создание группы для хранения пуль.
	bullets = Group()
	aliens = Group()
	# Создание пришельца.
	alien = Alien(ai_settings,screen)
	# Создание экземпляра статистики.
	stats = GameStats(ai_settings)
	# Создание экземпляра кнопки и таблицы счета.
	play_button = Button(ai_settings,screen,'Play')
	sb = Scoreboard(ai_settings,screen,stats)
	gf.create_fleet(ai_settings,screen,ship,aliens)
	# Запуск основного цикла игры.
	while True:
		# Отслеживание событий клавиатуры и мыши.
		gf.check_events(ai_settings,screen,aliens,stats,play_button,
														ship,bullets,sb)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,ship,aliens,bullets,sb,stats)
			gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets,sb)
		gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,
															  play_button,sb)
run_game()