import pygame
from ship import Ship
class GameStats():
	'''Отслеживание статистики игры.'''
	def __init__(self,ai_settings):
		'''Инициализирует статистику.'''
		self.ai_settings = ai_settings
		self.reset_stats()
		# Игра запускается в False состоянии флага.
		self.game_active = False
		# Рекорд не должен сбрасываться.
		self.high_score = 0
		self.level = 1

	def reset_stats(self):
		'''Инициализирует статистику, изменяющуюся в ходе игры.'''
		self.ships_left = self.ai_settings.ship_limit
		# Количество очков.
		self.score = 0 
