from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from datetime import date

imdb_website = 'https://www.imdb.com/search/title/?sort=user_rating,desc'
start_index = 1
curr_date = date.today()
curr_year = curr_date.year

genre_list = [
	'Action',
	'Adventure',
	'Animation',
	'Biography',
	'Comedy',
	'Crime',
	'Documentary',
	'Drama',
	'Family',
	'Fantasy',
	'Film-Noir',
	'Game-Show',
	'History',
	'Horror',
	'Music',
	'Musical',
	'Mystery',
	'News',
	'Reality-TV',
	'Romance',
	'Sci-Fi',
	'Sport',
	'Talk-Show',
	'Thriller',
	'War',
	'Western',
]

class Error(Exception):
	'''Base class for other exceptions'''
	pass

class OutOfRangeTVError(Error):
	'''Raised when the year input is outside the TV series range'''
	pass

class OutOfRangeError(Error):
	'''Raised when the year input is outside the program range'''
	pass

# Determines if the user wants just movies or just tv-series or both included in the search.
def movie_or_tv():
	global imdb_website
	program_type = input('Would you like to include movies or tv shows or both? Enter "movie" or "tv" or "both" for your choice. ')
	print('\n')
	if program_type.lower() == 'movie':
		imdb_website += '&title_type=movie'
	elif program_type.lower() == 'tv':
		imdb_website += '&title_type=tv_series'
	elif program_type.lower() == 'both':
		pass
	else:
		print('There was an error with your input. Please try again.')
		print('\n')
		movie_or_tv()

# Determines which (if any) genres the user wants to include in the search.
def program_genres():
	global imdb_website, genre_list
	genres = input('Which genre(s) would you like to include?\n\nAction\nAdventure\nAnimation\nBiography\nComedy\n' +
				   'Crime\nDocumentary\nDrama\nFamily\nFantasy\nFilm-Noir\nGame-Show\nHistory\nHorror\nMusic\nMusical\nMystery\nNews\nReality-TV' +
				   '\nRomance\nSci-Fi\nSport\nTalk-Show\nThriller\nWar\nWestern\n\nChoose one of the following or enter "no" if you do not want to ' +
				   'include any genres. ')
	print('\n')
	genre_list_2 = []
	if genres.lower() == 'no':
		pass
	else:
		for item in genre_list:
			if genres.lower() == item.lower():
				imdb_website += '&genres=' + genres.lower()
				genre_list_2 = []
				program_genres()
			else:
				genre_list_2.append(item)
				if len(genre_list_2) == len(genre_list):
					print('There was an error with your input. Please try again.')
					program_genres()

# Determines if the user wants the search to only be within a certain year range.
def program_years():
	global imdb_website, curr_year
	try:
		min_year = int(input('What is the minimum year you want the programs to be of? Enter 0 if you do not want any such filter. '))
		print('\n')
		max_year = int(input('What is the maximum year you want the programs to be of? Enter 0 if you do not want any such filter. '))
		print('\n')
		if 'tv_series' in imdb_website:
			if min_year < 0 or 1 <= min_year <= 1897 or min_year > curr_year:
				raise OutOfRangeTVError
			if max_year < 0 or 1 <= max_year <= 1897 or max_year > curr_year:
				raise OutOfRangeTVError
		else:
			if min_year < 0 or 1 <= min_year <= 1894 or min_year > curr_year:
				raise OutOfRangeError
			if max_year < 0 or 1 <= max_year <= 1894 or max_year > curr_year:
				raise OutOfRangeError
		if min_year > max_year and max_year == 0:
			pass
		elif min_year > max_year and max_year != 0:
			raise ValueError
	except ValueError:
		print('There was an error with your input. Please try again.')
		print('\n')
		program_years()
	except OutOfRangeTVError:
		print('The earliest TV series on IMDb first aired in 1897. Please ensure your input is in between 1898 and the current year.')
		print('\n')
		program_years()
	except OutOfRangeError:
		print('The earliest program on IMDb first aired in 1894. Please ensure your input is in between 1895 and the current year.')
		print('\n')
		program_years()
	if min_year == max_year:
		if min_year == 0:
			pass
		else:
			imdb_website += '&release_date=' + str(min_year)
	elif min_year == 0 and max_year != 0:
		imdb_website += '&release_date=,' + str(max_year)
	elif min_year != 0 and max_year == 0:
		imdb_website += '&release_date=' + str(min_year) + ','
	else:
		imdb_website += '&release_date=' + str(min_year) + ',' + str(max_year)

# Determines if the user wants the search to only be within a certain rating range.
def program_rating():
	global imdb_website
	try:
		min_rating = float(input('What is the minimum rating you want the programs to be of? Enter 0 if you do not want any such filter. '))
		print('\n')
		min_rating =  round(min_rating, 1)
		max_rating = float(input('What is the maximum rating you want the programs to be of? Enter 0 if you do not want any such filter. '))
		print('\n')
		max_rating =  round(max_rating, 1)
		if min_rating < 0 or min_rating > 10:
			raise ValueError
		if max_rating < 0 or max_rating > 10:
			raise ValueError
		if min_rating > max_rating and max_rating == 0:
			pass
		elif min_rating > max_rating and max_rating != 0:
			raise ValueError
	except ValueError:
		print('There was an error with your input. Please try again.')
		print('\n')
		program_rating()
	if min_rating == max_rating:
		if min_rating == 0:
			pass
		else:
			imdb_website += '&user_rating=' + str(min_rating)
	elif min_rating == 0 and max_rating == 10:
		pass
	elif min_rating == 0 and 0 < max_rating < 10:
		imdb_website += '&user_rating=,' + str(max_rating)
	elif 0 < min_rating < 10 and max_rating == 0:
		imdb_website += '&user_rating=' + str(min_rating) + ','
	else:
		imdb_website += '&user_rating=' + str(min_rating) + ',' + str(max_rating)

# Determines if the user wants the search to only be within a certain number of votes range.
def program_votes():
	global imdb_website
	try:
		min_votes = int(input('What is the minimum amount of votes you want the programs to have? Enter 0 if you do not want any such filter. '))
		print('\n')
		max_votes = int(input('What is the maximum amount of votes you want the programs to have? Enter 0 if you do not want any such filter. '))
		print('\n')
		if min_votes < 0:
			raise ValueError
		if max_votes < 0:
			raise ValueError
		if min_votes > max_votes and max_votes == 0:
			pass
		elif min_votes > max_votes and max_votes != 0:
			raise ValueError
	except ValueError:
		print('There was an error with your input. Please try again.')
		print('\n')
		program_votes()
	if min_votes == max_votes:
		if min_votes == 0:
			pass
		else:
			imdb_website += '&num_votes=' + str(min_votes)
	elif min_votes == 0 and max_votes != 0:
		imdb_website += '&num_votes=,' + str(max_votes)
	elif min_votes != 0 and max_votes == 0:
		imdb_website += '&num_votes=' + str(min_votes) + ','
	else:
		imdb_website += '&num_votes=' + str(min_votes) + ',' + str(max_votes)

# Goes through all the movies on the webpage and adds their relevant information to the spreadsheet.
def program_sorter():
	global containers
	for container in containers:
		title = container.h3.a.text
		year_container = container.findAll('span', {'class':'lister-item-year text-muted unbold'})
		old_year_var = year_container[0].text
		new_year_var = ''
		for digit in old_year_var:
			if digit in '0123456789–':
				new_year_var += digit
		genre_container = container.findAll('span', {'class':'genre'})
		if genre_container == []:
			genres = 'Not found'
		else:
			genres = genre_container[0].text.strip()
		rating_container = container.findAll('div', {'class':'inline-block ratings-imdb-rating'})
		rating_var = rating_container[0].text.strip()
		votes_container = container.findAll('span', {'name':'nv'})
		votes = votes_container[0].text
		num_votes = ''
		for digit in votes:
			if digit in '0123456789':
				num_votes += digit
		f.write(title.replace(',', '') + ',' + new_year_var + ',' + genres.replace(', ', '|') + ',' 
				+ rating_var + ',' + num_votes + '\n')

# Starts the program
if __name__ == '__main__':

	print('Welcome to the IMDb Web Scraper. This script is designed to create a CSV dataset that contains movies and their relevant information ' + 
		  'for the purposes of data science and machine learning. Following this there will be a series of inputs for you to complete and upon ' +
		  'their completion, the file will be available in the same directory as where this script is located.\n')

	movie_or_tv()
	program_genres()
	program_years()
	program_rating()
	program_votes()

	# Opens a connection to the webpage, stores a local copy of the HTML code, and parses it
	connection = urlopen(imdb_website)
	page_html = connection.read()
	connection.close()
	parsed_html = soup(page_html, 'html.parser')

	# Searches for the blocks that contain the movies and their information and whether there is another page or not
	containers = parsed_html.findAll('div', {'class':'lister-item mode-advanced'})
	next_page = parsed_html.findAll('a', {'class':'lister-page-next next-page'})

	# Opens up a CSV file in 'Write' mode
	filename = 'program_list.csv'
	f = open(filename, 'w')

	# Creates headers under which movie information will fall under in the CSV file
	headers = 'title, year, genres, imdb_rating, number_of_votes\n'
	f.write(headers)

	# If the user's search yields no results, the program will essentially start over
	if containers == []:
		while containers == []:
			print('There were no results for your search. Please refine your criteria and try again.')
			print('\n')

			imdb_website = 'https://www.imdb.com/search/title/?sort=user_rating,desc'

			movie_or_tv()
			program_genres()
			program_years()
			program_rating()
			program_votes()

			connection = urlopen(imdb_website)
			page_html = connection.read()
			connection.close()
			parsed_html = soup(page_html, 'html.parser')

			containers = parsed_html.findAll('div', {'class':'lister-item mode-advanced'})
			next_page = parsed_html.findAll('a', {'class':'lister-page-next next-page'})

			filename = 'program_list.csv'
			f = open(filename, 'w')

			headers = 'title, year, genres, imdb_rating, number_of_votes\n'
			f.write(headers)

	print('Please be patient while the program creates your dataset. Once it is done, there will be another text pop-up in the console.')
	print('\n')

	program_sorter()

	# Recursively goes through the website and adds to the spreadsheet until there are no more pages left, or the spreadsheet contains 10,000 items
	if next_page != []:
		while next_page != []:
			start_index += 50
			if start_index == 10001:
				f.close()
				break
			else:
				imdb_website += '&start=' + str(start_index)
				connection = urlopen(imdb_website)
				page_html = connection.read()
				connection.close()
				parsed_html = soup(page_html, 'html.parser')
				containers = parsed_html.findAll('div', {'class':'lister-item mode-advanced'})
				next_page = parsed_html.findAll('a', {'class':'lister-page-next next-page'})
				program_sorter()
	f.close()
	print('The dataset has been created! Check the directory from where you ran this script and locate "program_list.csv" to access it.')