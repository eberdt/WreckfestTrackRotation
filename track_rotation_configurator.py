import csv
from typing import TextIO


def main():

    track_rotation_output = "track_rotation.txt"
    valid_ids_file = "valid_track_ids.csv"
    user_tracks = "user_track_rotation.csv"
    valid_track_ids = populate_valid_tracks(valid_ids_file)

    # FOR TESTING PURPOSES ONLY
    # ids_file_checker = "double_check_ids.txt"
    # all_track_ids_list = []
    # ids_file = open(ids_file_checker, 'r')
    # for line in ids_file:
    #     curr_track_id = line.strip(' \n')
    #     all_track_ids_list.append(curr_track_id)
    # ids_file.close()
    # for key1 in valid_track_ids:
    #     for key2 in valid_track_ids[key1]:
    #         track_id = valid_track_ids[key1][key2]
    #         all_track_ids_list.pop(all_track_ids_list.index(track_id))
    # print(all_track_ids_list)

    populate_user_defined_tracks(valid_track_ids, user_tracks, track_rotation_output)


def populate_valid_tracks(valid_ids_file):
    all_track_ids_dict = {}
    with open(valid_ids_file) as valid_track_ids_file:
        valid_ids_csv_reader = csv.reader(valid_track_ids_file, delimiter=",")
        line_count = 0
        for row in valid_ids_csv_reader:
            if line_count > 0:
                location = row[0].strip(" \n").lower()
                track = row[1].strip(" \n").lower()
                track_id = row[2].strip(" \n").lower()
                if location in all_track_ids_dict:
                    all_track_ids_dict[location][track] = track_id
                else:
                    all_track_ids_dict[location] = {}
                    all_track_ids_dict[location][track] = track_id
            line_count = line_count + 1

        # FOR TESTING PURPOSES ONLY
        # for key in all_track_ids_dict:
        #     print(key)
        #     print(all_track_ids_dict[key])
        #
        # valid_track_ids_file.close()

    return all_track_ids_dict


def populate_user_defined_tracks(valid_track_ids, user_tracks, track_rotation_output):
    output_file: TextIO = open(track_rotation_output, 'w')
    output_file.write("")

    with open(user_tracks) as tracks_csv_file:
        tracks_csv_reader = csv.reader(tracks_csv_file, delimiter=',')
        # valid_laps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        valid_laps = list(range(1, 60))
        valid_teams = [2, 3, 4]
        # valid_minutes = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        valid_minutes = list(range(2, 20))
        valid_elimination = [0, 20, 30, 45, 60, 90, 120]
        line_count = 0
        for event in tracks_csv_reader:
            if line_count > 0:
                location = event[0].strip(" \n").lower()
                track_name = event[1].strip(" \n").lower()
                race_type = event[2].strip(" \n").lower()
                laps = event[3].strip(" \n")
                minutes = event[4].strip(" \n")
                num_teams = event[5].strip(" \n")
                elimination_interval = event[6].strip(" \n")
                try:
                    track_id = valid_track_ids[location][track_name]
                except KeyError as e:
                    print(e)
                    line_count = line_count + 1
                    print("ERROR: Invalid Track Location/Track: " + location + " / " + track_name + "  LineNum: " + str(
                        line_count))
                    continue

                if race_type == "banger race":
                    race_type = "racing"
                elif race_type == "team race":
                    race_type = "team race"
                elif race_type == "elimination race":
                    race_type = "elimination race"
                elif race_type == "deathmatch":
                    race_type = "derby deathmatch"
                elif race_type == "team deathmatch":
                    race_type = "team derby"
                elif race_type == "last man standing":
                    race_type = "derby"
                else:
                    line_count = line_count + 1
                    print("ERROR: race_type " + race_type + "  LineNum: " + str(line_count))
                    continue

                if race_type == "racing" and not laps.isnumeric():
                    print("ERROR: race without valid laps  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                elif race_type == "racing" and int(laps) not in valid_laps:
                    print("ERROR: race without valid laps  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                if race_type == "team race" and (not laps.isnumeric() or not num_teams.isnumeric()):
                    print("ERROR: team race without valid laps or number of teams  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                elif race_type == "team race" and (int(laps) not in valid_laps or int(num_teams) not in valid_teams):
                    print("ERROR: team race without valid laps or valid team number  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                if race_type == "derby deathmatch" and not minutes.isnumeric():
                    print("ERROR: deathmatch without time limit  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                elif race_type == "derby deathmatch" and int(minutes) not in valid_minutes:
                    print("ERROR: deathmatch without valid minutes  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                if race_type == "team derby" and (not minutes.isnumeric() or not num_teams.isnumeric()):
                    print("ERROR: team deathmatch without valid time limit or number of teams  LineNum: " + str(
                        line_count + 1))
                    line_count = line_count + 1
                    continue
                elif race_type == "team derby" and (int(minutes) not in valid_minutes or int(num_teams) not in valid_teams):
                    print("ERROR: team deathmatch without valid minutes or valid teams  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                if race_type == "elimination race" and not elimination_interval.isnumeric():
                    print("ERROR: elimination race without valid elimination interval  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue
                elif race_type == "elimination race" and int(elimination_interval) not in valid_elimination:
                    print("ERROR: elimination race without valid elimination interval  LineNum: " + str(line_count + 1))
                    line_count = line_count + 1
                    continue

                race_num = str(line_count-1)
                output_file.write("# Race " + race_num + "\n")
                output_file.write("# Location: " + location + "\n")
                output_file.write("# Track Name: " + track_name + "\n")
                output_file.write("el_add=" + track_id + "\n")
                output_file.write("el_gamemode=" + race_type + "\n")
                output_file.write("el_num_teams=" + num_teams + "\n")
                output_file.write("el_laps=" + laps + "\n")
                output_file.write("el_elimination_interval=0" + "\n")
                output_file.write("el_car_reset_disabled=0" + "\n")
                output_file.write("el_wrong_way_limiter_disabled=1" + "\n")
                output_file.write("#el_car_class_restriction=a" + "\n")
                output_file.write("el_car_restriction=" + "\n")
                output_file.write("el_weather=random" + "\n")
                output_file.write("\n")

            line_count = line_count + 1
    output_file.close()
    return


main()


#
#             output_file.write("# Race " + str(line_count-1) + "\n")
#             output_file.write("# Location: " + location + "\n")
#             output_file.write("# Track Name: " + track_name + "\n")
#             output_file.write("el_add=" + track_id + "\n")
#             output_file.write("el_gamemode=" + race_type + "\n")
#             output_file.write("el_num_teams=" + num_teams + "\n")
#             output_file.write("el_laps=" + laps + "\n")
#             output_file.write("el_elimination_interval=0" + "\n")
#             output_file.write("el_car_reset_disabled=0" + "\n")
#             output_file.write("el_wrong_way_limiter_disabled=1" + "\n")
#             output_file.write("#el_car_class_restriction=a" + "\n")
#             output_file.write("el_car_restriction=" + "\n")
#             output_file.write("el_weather=" + "\n")
#             output_file.write("\n")
#
#         line_count = line_count + 1
#
# output_file.close()
