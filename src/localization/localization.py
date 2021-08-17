

class Localizer:

    localizations = {
        "en-us": {
            
        },
        "en-uk": {
            # perhaps we can get a wo'oh bo'oh on a chesday innit?
        }
    }

    locale = "en-us"

    @staticmethod
    def get_localized_text(key):
        return Localizer.localizations[Localizer.locale][key]