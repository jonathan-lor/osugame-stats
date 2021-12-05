import requests
import osufunctions


class RecentPlays:
    # think numTopPlay as 1st best play, 2nd best play, etc.
    def __init__(self, userName, numTopPlay=1):
        self.userName = userName
        self.numTopPlay = numTopPlay
        self.getUnfilteredData()

    # gets user id from inputted userName and returns it
    # also sets case sensitive username based on userprofile
    def getUserID(self):
        token = osufunctions.getToken()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        params = {
            'mode': 'osu',
            'limit': 1
        }
        userPage = requests.get(
            f'{osufunctions.API_URL}/users/{self.userName}', params=params, headers=headers)
        userID = userPage.json().get('id')
        self.caseSensitiveUserName = userPage.json().get('username')
        return userID

  # gets all of the score data for specified numTopPlay, even the unecessary data in order to pick out the relevant stuff
    def getUnfilteredData(self):
        #print("Hello my name is " + self.name)
        token = osufunctions.getToken()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        params = {
            'mode': 'osu',
            'limit': self.numTopPlay
        }
        unfiltered = requests.get(
            f'{osufunctions.API_URL}/users/{self.getUserID()}/scores/recent', params=params, headers=headers)
        # if no recent plays in last 24 hours
        if (len(list(unfiltered.json())) == 0):
            self.unfiltered = unfiltered.json()
            return
        unfiltered = unfiltered.json()[self.numTopPlay - 1]
        self.unfiltered = unfiltered

    # following functions pull relevant data from unfiltered data

    def getUserInfo(self):
        userInfo = self.unfiltered.get('user')
        return userInfo

    def getBeatmapInfo(self):
        beatmapInfo = self.unfiltered.get('beatmap')
        return beatmapInfo

    # song/beatmap info

    def getSongName(self):
        songName = self.unfiltered.get('beatmapset').get('title')
        return songName

    def getMods(self):
        mods = self.unfiltered.get('mods')
        modsFormatted = ''
        for modsUsed in mods:
            modsFormatted += modsUsed
        if(modsFormatted == ''):
            modsFormatted = 'NM'
        return modsFormatted

    def getPP(self):
        pp = self.unfiltered.get('pp')
        pp = str(pp) + " pp"
        if (pp == "None pp"):
            pp = "No pp gained"
        return pp

    def getDiffName(self):
        diffName = self.getBeatmapInfo().get('version')
        return diffName

    def getArtist(self):
        artist = self.unfiltered.get('beatmapset').get('artist')
        return artist

    def getAcc(self):
        acc = format(float(self.unfiltered.get('accuracy')) * 100, '.2f')
        return acc

    def getScore(self):
        score = self.unfiltered.get('score')
        score = "{:,}".format(score)
        return score

    def getStars(self):
        stars = self.getBeatmapInfo().get('difficulty_rating')
        return stars

    def getThreeHundred(self):
        threeHundred = self.unfiltered.get('statistics').get('count_300')
        return threeHundred

    def getHundred(self):
        hundred = self.unfiltered.get('statistics').get('count_100')
        return hundred

    def getFifty(self):
        fifty = self.unfiltered.get('statistics').get('count_50')
        return fifty

    def getMiss(self):
        miss = self.unfiltered.get('statistics').get('count_miss')
        return miss
    # can only be returned when getting single top or recent play, cant be displayed in discord embed w/ multiple plays

    def getBG(self):
        bg = self.unfiltered.get('beatmapset').get('covers').get('list@2x')
        return bg

    def getMapUrl(self):
        mapUrl = self.getBeatmapInfo().get('url')
        return mapUrl

    def getUserUrl(self):
        userUrl = f'https://osu.ppy.sh/users/{self.getUserID()}/osu'
        return userUrl
    # for displaying correct username incase inputted username wasnt case accurate

    def getCaseSensitiveUsername(self):
        caseSensitiveUsername = self.getUserInfo().get('username')
        return caseSensitiveUsername

    # dictionary containing all necessary info about the score
    def getTotalInfo(self):
        if len(list(self.unfiltered)) == 0:
            totalInfo = {
                "exists": False,
                "username": self.caseSensitiveUserName,
            }
        else:
            totalInfo = {
                "exists": True,
                "user_url": self.getUserUrl(),
                "username": self.caseSensitiveUserName,
                "artist": self.getArtist(),
                "songName": self.getSongName(),
                "diffName": self.getDiffName(),
                "stars": self.getStars(),
                "mods": self.getMods(),
                "acc": self.getAcc(),
                "score": self.getScore(),
                "threehundred": self.getThreeHundred(),
                "hundred": self.getHundred(),
                "fifty": self.getFifty(),
                "miss": self.getMiss(),
                "pp": self.getPP(),
                "map_url": self.getMapUrl(),
                "bg": self.getBG()
            }

        return totalInfo
