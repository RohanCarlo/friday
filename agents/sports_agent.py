# agents/sports_agent.py

import requests

def get_sports(team_or_league: str = "IPL") -> str:
    """Fetches latest scores from TheSportsDB (free, no key needed for basic use)"""
    
    # Search for the league/team
    search_url = f"https://www.thesportsdb.com/api/v1/json/3/search_all_leagues.php?c=India"
    
    try:
        # Get latest events for IPL (league ID 4512) as default
        league_id  = "4512"  # IPL
        events_url = f"https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id={league_id}"
        events     = requests.get(events_url, timeout=5).json().get("events", [])
        
        if not events:
            return "No recent sports results found."
        
        # Get last 3 results
        recent = events[-3:]
        results = []
        for e in recent:
            results.append(
                f"{e['strHomeTeam']} {e.get('intHomeScore','?')} vs "
                f"{e['strAwayTeam']} {e.get('intAwayScore','?')}"
            )
        
        return "Recent IPL results: " + ". ".join(results)
    
    except Exception as e:
        return f"Sports service unavailable. Error: {e}"