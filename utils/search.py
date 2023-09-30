import mtgsdk as mtg

def download_filtered(filter:dict) -> list:
    card_query = mtg.QueryBuilder(mtg.Card)
    card_query.params.update(filter)
    cards = card_query.all()
    return cards