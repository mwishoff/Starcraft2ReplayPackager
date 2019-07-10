"""
__Author__ = Matthew Wishoff
Maintained with PEP8 standards

This program will take the starcraft2 replays in the folder given by the user,
and sort them into their match ups and by patch for easy browsing and viewing
through the StarCraft2 Client.
"""

import os
import mpyq
from s2protocol import versions


def grab_files():
    """
    This function iterates over the files in the location given by the user,
    calling the function extract_replay_info(loc) which returns a dictionary.

    :rtype: dictionary
    :return: Returns all the data from all the replays in the given directory.
    """
    rep_info_data = []

    for file in os.listdir("."):
        if os.path.isfile(file):
            loc = os.path.join(file)
            rep_info = extract_replay_info(loc)
            if rep_info != {}:
                rep_info['file_name'] = file
                rep_info_data.append(rep_info)

    return rep_info_data


def extract_replay_info(loc):
    """
    Replays are stored as MPQArchives and need to be extracted using the scprotocol
    provided by blizzard. This function takes that protocol and uses it to extract
    the data inside the replay. Items returned are player names, map name, player races,
    official blizzard map, the patch version, and the location of the starcraft2 replay.

    :param loc: File path location where a single StarCraft2 replay is
    :rtype: Dictionary
    :return: Returns data from the replay
    """

    if os.path.isfile(loc):
        archive = mpyq.MPQArchive(loc)
        contents = archive.header['user_data_header']['content']
        header = versions.latest().decode_replay_header(contents)
        base_build = header['m_version']['m_baseBuild']
        try:
            protocol = versions.build(base_build)
        except ImportError:
            print("Replay too old, protocol does not exist: " + loc)
            return {}

        # Get patch version from replay header
        patch = str(header['m_version']['m_major']) + "." + \
                str(header['m_version']['m_minor']) + "." + \
                str(header['m_version']['m_revision'])

        contents = archive.read_file('replay.details')

        details = protocol.decode_replay_details(contents)

        try:
            map_name = details['m_title']
            player1_name = details['m_playerList'][0]['m_name'].decode('utf-8')
            player1_race = details['m_playerList'][0]['m_race'].decode('utf-8')
            player2_name = details['m_playerList'][1]['m_name'].decode('utf-8')
            player2_race = details['m_playerList'][1]['m_race'].decode('utf-8')
            blizz_map = details['m_isBlizzardMap']

            # Removes clan tag of the player
            if r"&gt;<sp/>" in player1_name:
                player1_name = player1_name.split("&gt;<sp/>")[1]
            if r"&gt;<sp/>" in player2_name:
                player2_name = player2_name.split("&gt;<sp/>")[1]

            return {"map": map_name,
                    "blizz_map": blizz_map,
                    "player1_name": str(player1_name),
                    "player1_race": str(player1_race),
                    "player2_name": str(player2_name),
                    "player2_race": str(player2_race),
                    "patch": patch,
                    "file": loc}
        except:
            return {}


def sort_replays_into_folders(starcraft_handle, data, replay_location):
    """
    This function iterates over the data, and creates directories for each patch
    in the data so that the files can be sorted into their respective folders.
    for easy browsing in the starcraft2 client.

    :param starcraft_handle: Starcraft2 handle given by the user
    :param data: A list of dictionaries that contain data about the replays
    :param replay_location: the top level directory where the replays currently are
    :return: None
    """
    patches = set()

    for replay_info in data:
        player_1 = replay_info['player1_name']
        player_2 = replay_info['player2_name']
        patch = replay_info['patch']
        matchup = ""

        if patch not in patches and "Patch " + patch not in os.listdir(os.getcwd()):
            os.mkdir("Patch " + patch, mode=777)
            os.chdir("Patch " + patch)

            os.mkdir("Terran Vs Terran", mode=777)
            os.mkdir("Terran Vs Zerg", mode=777)
            os.mkdir("Terran Vs Protoss", mode=777)

            os.mkdir("Protoss Vs Protoss", mode=777)
            os.mkdir("Protoss Vs Zerg", mode=777)
            os.mkdir("Protoss Vs Terran", mode=777)

            os.mkdir("Zerg Vs Zerg", mode=777)
            os.mkdir("Zerg Vs Protoss", mode=777)
            os.mkdir("Zerg vs Terran", mode=777)

            os.mkdir("Custom Maps", mode=777)

            patches.add(patch)

        if player_1 == starcraft_handle:
            matchup = replay_info['player1_race'] + " Vs " + replay_info['player2_race']
        elif player_2 == starcraft_handle:
            matchup = replay_info['player2_race'] + " Vs " + replay_info['player1_race']

        # if a map isn't a blizzard map it's a community made custom map.
        if not replay_info['blizz_map']:
            matchup = "Custom Maps"

        os.chdir(replay_location)
        os.rename(replay_info['file'],
                  os.getcwd() + "\\Patch " + patch + "\\" + matchup + "\\" + replay_info['file_name'])


def clean_up(loc):
    """
    Each matchup had a directory made, some might be empty and I delete them here.

    :param loc: the top level directory where the replays were sorted into patches
    :return: None
    """
    for dir_path, dir_names, file_names in os.walk(loc):
        if len(dir_names) == 0 and len(file_names) == 0:
            os.rmdir(dir_path)


def main():
    replay_location = input("Where are your StarCraft replays? ")
    starcraft_handle = input("What is your StarCraft handle? ")
    os.chdir(replay_location)
    data = grab_files()
    sort_replays_into_folders(starcraft_handle, data, replay_location)
    clean_up(replay_location)


if __name__ == "__main__":
    main()
