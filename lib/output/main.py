## File to manage outputs
 

# Library to get date and calcutiontime for program
import datetime

import lib.output.highcharts
import lib.output.json
import settings


##
## @brief      Creates a filename with current date.
##
## @param      simc_settings  The simc options dictionary {iterations s, target
##                            error s, fight style s, class s, spec s, tier s
##                            "T19M_NH"}
##
## @return     Returns a filename which contains the current date
##
def create_filename(simc_settings):
  filename = ""
  filename += "{:%Y_%m_%d__%H_%M}".format(datetime.datetime.now())
  filename += "_" + simc_settings["fight_style"]
  filename += "_" + simc_settings["class"]
  filename += "_" + simc_settings["spec"]
  filename += "_" + simc_settings["tier"]
  return filename


##
## @brief      Reduces trinket dps to the actual gain those trinkets provide in
##             comparison to the baseline dps.
##
## @param      sim_results  Dictionary of all simmed trinkets with all their dps
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      base_dps     Dictionary of the base-profile without trinkets
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      base_ilevel  The base ilevel
##
## @return     Dictionary of all simmed trinkets with all their normalised dps
##             values as strings {trinket_name s:{ilevel s:{dps s}}}. dps is "0"
##             if to be simmed itemlevel don't match available trinket itemlevel
##
def normalise_trinkets(sim_results, base_dps, base_ilevel):
  for trinket in sim_results:
    for ilevel in sim_results[trinket]:
      if not sim_results[trinket][ilevel] == "0":
        sim_results[trinket][ilevel] = str(int(sim_results[trinket][ilevel]) - int(base_dps["none"][base_ilevel]))
  return sim_results


##
## @brief      Generates a list ordered by max dps value of highest itemlevel
##             trinkets [trinket_name s]
##
## @param      sim_results  Dictionary of all simmed trinkets with all their dps
##                          values as strings {trinket_name s:{ilevel s:{dps
##                          s}}}.
## @param      ilevels      The ilevels list
##
## @return     Trinket list ordered ascending from lowest to highest dps for
##             highest available itemlevel
##
def order_results(sim_results, ilevels):
  highest_ilevel = ilevels[0]
  current_best_dps = "-1"
  last_best_dps = "-1"
  name = ""
  trinket_list = []
  # gets highest dps value of all trinkets
  for trinket in sim_results:
    if int(last_best_dps) < int(sim_results[trinket][highest_ilevel]) :
      last_best_dps = sim_results[trinket][highest_ilevel]
      name = trinket
  trinket_list.append(name)
  for outerline in sim_results:
    name = "error"
    current_best_dps = "-1"
    for trinket in sim_results:
      if int(current_best_dps) < int(sim_results[trinket][highest_ilevel]) and int(last_best_dps) > int(sim_results[trinket][highest_ilevel]):
        current_best_dps = sim_results[trinket][highest_ilevel]
        name = trinket
    if not name == "error": 
      trinket_list.append(name)
      last_best_dps = current_best_dps
  return trinket_list


def print_manager(print_types, base_dps_dic, trinket_dic, ilevels, graph_colours, graph_name, simc_settings, output_screen):
  filename = create_filename(simc_settings)
  for print_type in print_types:

    if print_type is "json":
      print("Initiating json output.")
      if json.print_json(trinket_dic, ilevels, graph_name, simc_settings, filename):
        print("Generating json file: Done")
      else:
        print("Generating json file: Failed")

    elif print_type is "highchart":
      print("Initiating highchart output")
      print("Ordering trinkets by dps.")
      ordered_trinket_names = order_results(sim_results, ilevels)
      if output_screen:
        print(ordered_trinket_names)
      print("Normalising dps values.")
      sim_results = normalise_trinkets(sim_results, base_dps_dic, ilevels[-1])
      if output_screen:
        print(sim_results)
      if lib.output.highcharts.print_highchart(sim_results, ordered_trinket_names, ilevels, graph_colours, graph_name, simc_settings, filename):
        print("Generating highchart file: Done")
      else:
        print("Generating highchart file: Failed")