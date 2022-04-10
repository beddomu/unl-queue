from utils.get_rank import get_rank

def is_player_gold_plus(summoner_id):
    try:
        rank = get_rank(summoner_id)
        if rank not in ["IRON", "BRONZE", "SILVER"]:
            return True
        elif not rank:
            return False
        else:
            return False
    except:
        return False