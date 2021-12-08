import getToken
import requests


class UserProfile:
    def __init__(self, userName):
        self.userName = userName
        self.getUserPage()

    def getUserPage(self):
        token = getToken.getToken()
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
            f'{getToken.API_URL}/users/{self.userName}', params=params, headers=headers)
        userPage = userPage.json()
        # gets correct username with regard to case sensitivity from user profile
        self.caseSensitiveUserName = userPage.get('username')
        self.userPage = userPage

    def getLevel(self):
        level = self.userPage.get('statistics').get('level').get('current')
        return level

    def getRank(self):
        rank = self.userPage.get('statistics').get('global_rank')
        if rank is None:
            return rank
        else:
            rank = "{:,}".format(rank)
            return rank

    def getPP(self):
        pp = self.userPage.get('statistics').get('pp')
        pp = "{:,}".format(pp)
        return pp

    def getRankedScore(self):
        rankedScore = self.userPage.get('statistics').get('ranked_score')
        rankedScore = "{:,}".format(rankedScore)
        return rankedScore

    def getProfileAcc(self):
        profileAcc = self.userPage.get('statistics').get('hit_accuracy')
        profileAcc = format(
            float(profileAcc), '.2f')
        return profileAcc

    def getPlayCount(self):
        playCount = self.userPage.get('statistics').get('play_count')
        playCount = "{:,}".format(playCount)
        return playCount

    # returns playtime in hours

    def getPlayTime(self):
        playTime = self.userPage.get('statistics').get('play_time')
        playTime = format(float(playTime / 3600), '.2f')
        return playTime

    def getProfilePic(self):
        profilePic = self.userPage.get('avatar_url')
        return profilePic

    def getUserUrl(self):
        userID = self.userPage.get('id')
        userUrl = f'https://osu.ppy.sh/users/{userID}/osu'
        return userUrl

    def getTotalInfo(self):
        if len(list(self.userPage)) == 1:
            totalInfo = {
                "exists": False,
                "username": self.caseSensitiveUserName
            }
        else:
            totalInfo = {
                "exists": True,
                "username": self.caseSensitiveUserName,
                "level": self.getLevel(),
                "rank": self.getRank(),
                "pp": self.getPP(),
                "rankedScore": self.getRankedScore(),
                "profileAcc": self.getProfileAcc(),
                "playCount": self.getPlayCount(),
                "playTime": self.getPlayTime(),
                "profilePic": self.getProfilePic(),
                "userUrl": self.getUserUrl()
            }

        return totalInfo
