from collections import defaultdict

class Empire(object):
	""" all info to find best path for falcon millenium. """

	def __init__(self, routes_df, start, end, autonomy):
		self.empire = defaultdict(list)
		self.travel_time = {}
		self.current_time = {}
		self.autonomy = autonomy
		self.start_planet = start
		self.end_planet = end
		self.create_map(routes_df)
		
	def create_map(self, routes_df):
		""" Create map as a directed graph adjency list with wieght list"""
		for k in range(len(routes_df)):
			self.empire[routes_df.iloc[k].origin].append(routes_df.iloc[k].destination)
			if not routes_df.iloc[k].origin in self.current_time.keys():
				self.current_time[routes_df.iloc[k].origin] = 0
			if not routes_df.iloc[k].destination in self.current_time.keys():
				self.current_time[routes_df.iloc[k].destination] = 0
			self.travel_time[(routes_df.iloc[k].origin, routes_df.iloc[k].destination)] = routes_df.iloc[k].travel_time

	def find_all_path(self, current_planet, destination_planet, visited, path, all_path, max_time):
		""" find all paths from start point to end point """
		visited.append(current_planet)
		path.append(current_planet)

		if current_planet == destination_planet:
			all_path.append({"path":list(path), "travel_time": self.current_time[current_planet]})	
		for i in self.empire[current_planet]:
			if i not in visited:
				self.current_time[i] = self.travel_time[(current_planet, i)] + self.current_time[current_planet]
				if self.current_time[i] > max_time:
					continue
				self.find_all_path(i, destination_planet, visited, path, all_path, max_time)
		# continue finding paths by popping path and visited to get accurate paths
		path.pop()
		visited.pop()

		if not path:
			return all_path

	def find_best_path(self, all_path, hunters, max_time):
		""" Find path with best probabilties of success """
		best_prob = 0
		for k in range(len(all_path)):
			current_prob = 100
			h_counter = 0
			current_day = 0
			possible_days_for_waiting = max_time - (all_path[k]["travel_time"] + all_path[k]["refuel_time"])
			for j in range(1, len(all_path[k]["path"])):
				current_day += self.travel_time[(all_path[k]["path"][j -1], all_path[k]["path"][j])]
				#check hunters
				if any(h for h in hunters if (all_path[k]["path"][j] == h["planet"] and h["day"] == current_day)):
					current_prob -= (9**h_counter / 10 **(h_counter + 1))*100
					h_counter += 1
				#check fuel
				if current_day%self.autonomy == 0:
					current_day += 1
					#check hunters
					if any(h for h in hunters if (all_path[k]["path"][j] == h["planet"] and h["day"] == current_day)):
						current_prob -= (9**h_counter / 10 **(h_counter + 1)) * 100
						h_counter += 1

				if possible_days_for_waiting >= 1 and j+1 < len(all_path[k]["path"]):
					if any(h for h in hunters if (all_path[k]["path"][j + 1] == h["planet"] and h["day"] == current_day + self.travel_time[(all_path[k]["path"][j], all_path[k]["path"][j + 1])])):
						current_day += 1
						possible_days_for_waiting -= 1
			if current_prob > best_prob:
				best_prob = current_prob

		return best_prob

	def can_they_make_it_on_time(self, max_time, hunters):
		""" return probability of success given all info """
		all_path = self.find_all_path(self.start_planet, self.end_planet, [], [], [], max_time)
		if not all_path:
			return 0
		# #check if they have to refuel
		path_to_remove = []
		for k in range(len(all_path)):
			if all_path[k]["travel_time"] > self.autonomy:
				all_path[k]["refuel_time"] = int(all_path[k]["travel_time"]/self.autonomy)
			#check if time to get to destination is higher than max time
			if (all_path[k]["travel_time"] + all_path[k]["refuel_time"]) > max_time:
				path_to_remove.append(k)		
		for i in path_to_remove:
			all_path.pop(i)

		if not all_path:
			return 0

		#find path with less chance to be caught by hunters
		return self.find_best_path(all_path, hunters, max_time)