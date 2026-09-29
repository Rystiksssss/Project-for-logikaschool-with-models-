audio_toggles = {
    "zvuky_hry": True,
    "muzyka": False,
    "zvuky_menu": True,
    "spovishchennya": False,
}



audio_volumes = {
    "zvuky": 70,
    "muzyka": 40,
}




privacy_toggles = {
    "dvofaktorna": False,
    "statystyka": True,
    "pokazuvaty_profil": True,
}

quality_toggles = {
    "pelyustky": True,
    "khmarky": True,
    "radar": True,
    "tini": False,
}

quality_selected = {
    "yakist": 1,
    "fps": 1,
}

kills_stats = {
    "total": 0,
    "rare": 0,
    "epic": 0,
    "legendary": 0,
    "gold": 0,
}


def load_settings(data):
    global audio_toggles, privacy_toggles, quality_toggles
    global quality_selected, kills_stats, audio_volumes

    if "audio_toggles" in data:
        audio_toggles.update(data["audio_toggles"])
    if "privacy_toggles" in data:
        privacy_toggles.update(data["privacy_toggles"])
    if "quality_toggles" in data:
        quality_toggles.update(data["quality_toggles"])
    if "quality_selected" in data:
        quality_selected.update(data["quality_selected"])
    if "kills_stats" in data:
        kills_stats.update(data["kills_stats"])

    if "audio_volumes" in data:
        audio_volumes.update(data["audio_volumes"])


def save_settings():
    return {
        "audio_toggles": audio_toggles,
        "privacy_toggles": privacy_toggles,
        "quality_toggles": quality_toggles,
        "quality_selected": quality_selected,
        "kills_stats": kills_stats,
        "audio_volumes": audio_volumes,
    }




















































