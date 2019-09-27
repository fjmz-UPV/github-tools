import csv
import requests
import sys

PROMPT = "\nExample: python gt.py -o username password orgname"
DEBUG = False

class Gitub_Tools:
    def __init__(self, user_credential, orgname):
        self.ADMIN = user_credential
        self.ORG_NAME = orgname

    def add_to_org(self, fichero_csv):
        #with open('members.csv') as csv_file:
        with open(fichero_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for user_info in csv_reader:
                # send request and get response
                url = "https://" + self.ADMIN + "@api.github.com/orgs/" + \
                        self.ORG_NAME + "/memberships/" +  user_info[0]
                res = requests.put(url).json()
                if DEBUG:
                    print(res)
                # check if request fails
                if 'message' in res:
                    print(res['message'] + ".@ user:" + user_info[0])
                    return False
                else:
                    print('.') # print a dot to show progre
                    print(user_info[0]+' añadido a '+self.ORG_NAME)

        return True

    def add_to_team(self, teamname, fichero_csv):
        # send request to get teams info
        url = "https://" + self.ADMIN + "@api.github.com/orgs/" + \
                self.ORG_NAME + "/teams"
        print("URRRRRLLLLL"+url)        
        teams = requests.get(url).json()
        # get team id for api call
        print(teams);
        team_id = None
        for team in teams:
            if team['name'] == teamname:
                team_id = team['id']
                break
        if not team_id:
            print('Team not found.')
            return

        #with open('members.csv') as csv_file:
        with open(fichero_csv) as csv_file:        
            csv_reader = csv.reader(csv_file, delimiter=',')
            for user_info in csv_reader:
                # put together the api call
                url = "https://" + self.ADMIN + "@api.github.com" + "/teams/" +\
                    str(team_id) + "/members/" + user_info[0]
                # send request
                print("URL!!!!!" + url)
                res = requests.put(url)
                if DEBUG:
                    print(res.text)
                try:
                    # check if request fails
                    if 'message' in res.json():
                        print(res.json()['message'] + ".@ user:" + user_info[0])
                        return False
                except ValueError:
                    # when the user is added to the team, there's no response. 
                    # so .json() will yield a ValueError
                    print('.')

            return True

if __name__ == "__main__":
    # input check
    #if len(sys.argv) < 5 or (sys.argv[1] == '-t' and len(sys.argv) != 6):
    if len(sys.argv) < 6 or (sys.argv[1] == '-t' and len(sys.argv) != 7):
        print("Invalid arguments." + PROMPT)
        exit(-1)
    # flag check
    if sys.argv[1] != '-o' and sys.argv[1] != '-t':
        print("Invalid flag. " + sys.argv[1] + PROMPT)
        exit(-1)

    # get command-line arguments
    gt = Gitub_Tools(user_credential=sys.argv[2]+":"+sys.argv[3],orgname=sys.argv[4])
    # get flags o = organization, t = team
    if sys.argv[1] == '-o':
        status = gt.add_to_org(sys.argv[5])
    else:
        status = gt.add_to_team(sys.argv[5], sys.argv[6])

    if status:
        print('Done.')

    #Thanks for using Github Tools
