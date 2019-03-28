import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from gamestats import GameStats


def check_keydown_events(event,ai_settings,screen,ship,bullets):
	'''Реагирует на нажатие клавиш.'''
	if event.key == pygame.K_RIGHT:
		# Переместить корабль вправо.
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullets(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()


def check_keyup_events(event,ship):
	'''Реагирует на отпускание клавиш.'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False


def check_events(ai_settings,screen,aliens,stats,
									play_button,ship,bullets,sb):
	'''Обрабатывает нажатия клавиш и события мыши.'''
	# Отслеживание событий клавиатуры и мыши.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,ship,aliens,stats,
										play_button,sb,bullets,mouse_x,mouse_y)
def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb):
	'''Обновляет изображения на экране и отображает новый экран.'''
	# При каждом проходе цикла перерисовывается экран.
	screen.fill(ai_settings.bg_color)
	# Все пули выводятся позади корабля и прищельцев.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.bltime()
	aliens.draw(screen)
	# Вывод счета.
	sb.show_score()
	# Кнопка отображается только в неактивном состоянии флага.
	if not stats.game_active:
		play_button.draw_button()
	# Отображение последнего прорисованного экрана.
	pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets,sb,stats):
	'''Обновляет позиции пуль и удаляет старые пули.'''
	# Обновляет позиции пуль.
	bullets.update()
	# Удаление пуль, вышедших за экран.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet) 
	check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets,sb,stats)

def fire_bullets(ai_settings,screen,ship,bullets):
	'''Выпускает пулю, если максимум еще не достигнут.'''
	if len(bullets) < ai_settings.bullets_allowed:
	# Создание новой пули и включение ее в групу.
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def create_fleet(ai_settings,screen,ship,aliens):
	'''Создает флот пришельцев.'''
	# Создание пришельцев и вычисление количества пришельцев в ряду.
	# Интервал между соседними пришельцами равен одному пришельцу.

	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

	# Создание (флота) пришельцев.
	for row_number in range(number_rows):
	 	# Создание одного ряда пришельцев.
		for alien_number in range(number_aliens_x):
			# Создание пришельца и размещение его в ряду.
			create_alien(ai_settings,screen,aliens,alien_number,row_number)


def get_number_aliens_x(ai_settings,alien_width):
	'''Вычисляет количество пришельцев в ряду.'''
	available_space_x = ai_settings.screen_width - (2 * alien_width)
	number_aliens_x = int(available_space_x/(2 * alien_width))
	return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	'''Создает пришельца и добавляет его в ряд.'''
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
	'''Определяет количество рядов, помещающихся на экране.'''
	available_space_y = (ai_settings.screen_height - 
													(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,sb):
	'''Проверяет, достиг ли флот экрана,
	после чего обновляет позиции всех пришельцев во флоте.'''
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	# Проверка коллизий между кораблем и пришельцем.
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
	# Проверка пришельцев, добравшихся до низа.
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb)


def check_fleet_edges(ai_settings,aliens):
	'''Реагирует на достижение пришельцем экрана.'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	'''Опускает весь флот и меняет направление движения.'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets,sb,stats):
	# Проверка попадания в пришельцев.
	# При обнаружении попадание просиходит удаление пришельца.
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points
		sb.prep_score()
		check_high_score(stats,sb)
	if len(aliens) == 0:
		# Если весь флот уничтожен, начинает новый уровень.
		# Уничтожение существующих пуль и создание нового флота, увеличение скорости.
		ai_settings.increase_speed()
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		# Увеличивает уровень.
		stats.level += 1
		sb.prep_level()

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
	'''Обрабатывает столкновение корабля и пришельца.'''
	if stats.ships_left > 0:
		# Уменьшение ships_left.
		stats.ships_left -= 1
		# Обновление игровой информации.
		sb.prep_ships()
		# Очистка списка пришельцев и пуль.
		aliens.empty()
		bullets.empty()
		# Создание нового флота и размещение корабля в центре.
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		# Пауза.
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(False)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
	'''Проверяет, добрались ли пришельцы до нижнего края.'''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Происходит то же, что и при коллизии.
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
			break

def check_play_button(ai_settings,screen,ship,aliens,stats,play_button,
											sb,bullets,mouse_x,mouse_y):
	'''Запускает новую игру при нажатии кнопки.'''
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		# Сброс игровых настроек.
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		# Сброс игровой статистики.
		stats.reset_stats()
		stats.game_active = True
		# Сброс изображений счета и уровня.
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		# Очистка списка пришельцев и пуль.
		aliens.empty()
		bullets.empty()
		# Создание нового флота и размещение корабля в центре.
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

def check_high_score(stats,sb):
	'''Проверяет, появился ли новый рекорд.'''
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()














