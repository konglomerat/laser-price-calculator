from matplotlib import pyplot as plt
from matplotlib import gridspec as gridspec 
import numpy as np
import pandas as pd

def price_per_minute(t, a, b, c):
   return a*np.exp(-b*t) + c

def total_price(t, a, b, c):
	"""
	Integral of the price_per_minute function
	"""
	return a/b * (1 - np.exp(-b*t)) + c * t 

def slub_makerspace_pricing(t, m, n):
	"""
	Pricing in the SLUB Makerspace in Dresden for Lasercutting
	"""
	return m * t + n

def plot_diagramms():
	# load old price table
	df = pd.read_csv("laser-price-plotter.csv", sep=";")


	# set time values
	t_min = 0  # in min
	step = 15  # in min
	num = 9
	t_max = num * step  # in min
	t = np.linspace(0, t_max, t_max + 1)
	xticks = np.arange(0, num + 1) * step + t_min   # set x ticks in 15min steps

	show_old_price_model = False

	# prepare figure
	fig = plt.figure(figsize=(11.69, 8.27), tight_layout=True)  # DIN A4 landscape
	gs = gridspec.GridSpec(2,1)

	# prepare plot price per minute
	ax_price_per_minute = fig.add_subplot(gs[0,0])
	ax_price_per_minute.set_title("Preisentwicklung")
	ax_price_per_minute.set_xlabel("Zeit in min")
	ax_price_per_minute.set_ylabel("Preis in EUR/min")
	plt.xticks(xticks)
	plt.ylim(0, 1.25)

	# prepare plot total price
	ax_total_price = fig.add_subplot(gs[1,0])
	ax_total_price.set_title("Kostenentwicklung")
	ax_total_price.set_xlabel("Zeit in min")
	ax_total_price.set_ylabel("Preis in EUR")
	plt.xticks(xticks)

	# define colors
	members_color_old = "#A7C4E7"
	members_color_new = "#0074B2"
	non_members_color_old = "#FFB978"
	non_members_color_new = "#FF7B0E"
	slub_color = "#00A435"

	# Members
	members_price_at_t_0 = 0.8
	members_slope_at_t_0 = 0.01
	members_price_convergence = 0.3

	members_a = members_price_at_t_0 - members_price_convergence
	members_b = members_slope_at_t_0 / members_a
	members_c = members_price_convergence

	print("members_a:", members_a)
	print("members_b:", members_b)
	print("members_c:", members_c)

	if show_old_price_model:
		ax_price_per_minute.plot(df["time in min"], df["member price in euro"], label="Mitglied alt", color=members_color_old)

	ax_price_per_minute.plot(t, price_per_minute(t=t, a=members_a, b=members_b, c=members_c), label="Mitglied", color=members_color_new)
	ax_total_price.plot(t, total_price(t=t, a=members_a, b=members_b, c=members_c), label="Mitglied", color=members_color_new)

	# Non-Members
	non_members_price_at_t_0 = 1.2
	non_members_slope_at_t_0 = 0.01
	non_members_price_convergence = 0.5

	non_members_a = non_members_price_at_t_0 - non_members_price_convergence
	non_members_b = non_members_slope_at_t_0 / non_members_a
	non_members_c = non_members_price_convergence

	print("non_members_a:", non_members_a)
	print("non_members_b:", non_members_b)
	print("non_members_c:", non_members_c)

	if show_old_price_model:
		ax_price_per_minute.plot(df["time in min"], df["non-member price in euro"], label="Nichtmitglied alt", color=non_members_color_old)

	ax_price_per_minute.plot(t, price_per_minute(t=t, a=non_members_a, b=non_members_b, c=non_members_c), label="Nichtmitglied", color=non_members_color_new)
	ax_total_price.plot(t, total_price(t=t, a=non_members_a, b=non_members_b, c=non_members_c), label="Nichtmitglied", color=non_members_color_new)

	# SLUB Makerspace pricing
	slub_time_steps_range = np.linspace(0, t_max/10, t_max/10 + 1)

	slub_time_steps = [10*val for val in slub_time_steps_range for _ in (0, 1)]
	slub_time_steps = slub_time_steps[1:]

	slub_prices = [10*val for val in slub_time_steps_range for _ in (0, 1)]
	slub_prices = slub_prices[:-1]

	ax_total_price.plot(slub_time_steps, slub_prices, label="SLUB Makerspace", color=slub_color)

	# show legends
	ax_price_per_minute.legend()
	ax_total_price.legend()

	# calculate prices for special times durations
	time_steps_for_price = 5  # in min
	delta_t = t_max - t_min
	amount_of_steps = delta_t/time_steps_for_price 
	special_times =  [5, 10, 20, 30, 60, 90, 120] # np.linspace(t_min, t_max, amount_of_steps + 1)
	member_prices_for_special_times = []
	non_member_prices_for_special_times = []

	for time in special_times:
		member_prices_for_special_time     = round(total_price(t=time, a=members_a, b=members_b, c=members_c), 2)
		member_prices_for_special_times.append(member_prices_for_special_time)
		non_member_prices_for_special_time = round(total_price(t=time, a=non_members_a, b=non_members_b, c=non_members_c), 2)
		non_member_prices_for_special_times.append(non_member_prices_for_special_time)

	print(member_prices_for_special_times)
	print(non_member_prices_for_special_times)

	markersize = 5
	ax_total_price.plot(special_times, member_prices_for_special_times,
						'o', markersize=markersize, color=members_color_new)
	ax_total_price.plot(special_times, non_member_prices_for_special_times,
						'o', markersize=markersize, color=non_members_color_new)

	annotation_distance = 20
	arrow_distance_from_data_point = 3
	rotation_angle = 90
	bbox_args = dict(boxstyle="round", fc=members_color_new)
	arrow_args = dict(arrowstyle="-")





	annotation_member_dic = {}
	annotation_non_member_dic = {}

	for i in range(0, len(special_times)):
		x = special_times[i]
		y_member = member_prices_for_special_times[i]
		y_non_member = non_member_prices_for_special_times[i]

		# annotation_member_dic[i] = ax_total_price.annotate(str(y_member)+"€", 
		# 				xy=(x, y_member - arrow_distance_from_data_point), xycoords='data',
		# 				xytext=(x, y_member - annotation_distance), textcoords='data',
		# 				ha="center", va="center",
		# 				# bbox=bbox_args,
		# 				arrowprops=arrow_args,
		# 				rotation=rotation_angle,
		# 				color=members_color_new,
		# 				)
		# annotation_member_dic[i].draggable()
		text = str(x) + "min" + str(y_member)+"€ / " + str(y_non_member) + "€"

		# annotation_non_member_dic[i] = ax_total_price.annotate(str(y_non_member)+"€", 
		# annotation_non_member_dic[i] = ax_total_price.annotate(text, 
		# 				xy=(x, y_non_member + arrow_distance_from_data_point), xycoords='data',
		# 				xytext=(x, y_non_member + annotation_distance), textcoords='data',
		# 				ha="center", va="center",
		# 				#bbox=bbox_args,
		# 				# arrowprops=arrow_args,
		# 				rotation=rotation_angle,
		# 				color=non_members_color_new,
		# 				)
		# annotation_non_member_dic[i].draggable()
		# ax_total_price.vlines(x=x,ymin=y_non_member+5, ymax=y_non_member + annotation_distance,
		# 						linestyles='dashed',
		# 						color="grey")
		# ax_total_price.vlines(x=x,ymin=0, ymax=30, linestyles='dashed')

	# an1 = ax_total_price.annotate(str(member_prices_for_special_times[2])+"€", 
	# 					xy=(special_times[2], member_prices_for_special_times[2]), xycoords='data',
	#                 	xytext=(special_times[2], member_prices_for_special_times[2] + annotation_distance), textcoords='data',
	#                 	ha="center", va="center",
	#                 	#bbox=bbox_args,
	#                 	#arrowprops=arrow_args
	#                 	rotation=90,
	#                 	color=non_members_color_new,
	#                 	)
	# an1.draggable()
	plt.show()



plot_diagramms()

with plt.xkcd():
	plot_diagramms()


