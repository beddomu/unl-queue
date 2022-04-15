from utils.get_rank import get_rank

def is_player_gold_plus(summoner_id):
    try:
        rank = get_rank(summoner_id)
        if not rank:
            return False
        elif rank not in ["IRON", "BRONZE", "SILVER"]:
            return True
        else:
            return False
    except:
        return False