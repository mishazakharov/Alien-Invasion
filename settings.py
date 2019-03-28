class Settings():
	'''Класс для хранения всех настроек игры Alien Invasion'''
	def __init__(self):
		'''Инициализирует статические настройки игры.'''
		# Параметры экрана
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		# Настройка скорости корабля. 
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 10
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 3
		# Скорость пришельца. 
		self.alien_speed_factor = 3
		self.fleet_drop_speed = 10
		# fleet_direction = 1 вправо, а -1 влево. 
		self.fleet_direction = 1
		self.ship_limit = 3

		# Изменение темпа игры.
		self.speedup_scale = 1.1
		# Изменение количества очков за пришельца.
		self.score_scale = 1.5
		self.initialize_dynamic_settings()


	def initialize_dynamic_settings(self):
		'''Инициализируются динамические настройки игры.'''
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1

		# fleet_direction - направление!
		self.fleet_direction = 1
		# Количество очков с пришельца.
		self.alien_points = 50

	def increase_speed(self):
		'''Увеличивает настройки скорости и изменяет начисление очков.'''
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
