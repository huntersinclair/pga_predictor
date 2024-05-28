from datetime import datetime, timedelta

def number_to_words(n):
    if n == 0:
        return "zero"
    if n < 0:
        return "negative " + number_to_words(-n)
    if n < 20:
        return ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"][n]
    if n < 100:
        return ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"][n // 10] + \
               (" " + number_to_words(n % 10) if n % 10 != 0 else "")
    if n < 1000:
        return number_to_words(n // 100) + " hundred" + \
               (" " + number_to_words(n % 100) if n % 100 != 0 else "")
    for p, w in enumerate(("thousand", "million", "billion", "trillion"), 1):
        if n < 1000 ** (p + 1):
            return number_to_words(n // 1000 ** p) + " " + w + \
                   (" " + number_to_words(n % 1000 ** p) if n % 1000 ** p != 0 else "")
    return "Number too large"

def lowercase_first(s):
    return s[:1].lower() + s[1:] if s else ''


def convert_date_range(date_range_str):
    # Example usage
    # date_range = "Jan 4 - 7, 2024"
    # result = convert_date_range(date_range)

    # Define a dictionary to map month abbreviations to integers
    month_abbr = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }

    # Split the input string into two parts: start date and end date
    start_date_str, end_date_str = date_range_str.split('-')
    start_month_abbr, start_day = start_date_str.split()[:2]
    end_day = end_date_str.split(',')[0]
    year = int(end_date_str.split(',')[1].strip())

    # Convert start and end dates to datetime objects
    start_date = datetime(year, month_abbr[start_month_abbr], int(start_day))
    end_date = datetime(year, month_abbr[start_month_abbr], int(end_day))

    # Initialize an empty list to store the dates
    dates = []

    # Iterate over the date range and append each date to the list
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    # Join the dates with a semicolon and return the result
    return ';'.join(dates)

def fill_tournament_player_stats(player, scorecard, stats, schema_type='simple'):

    leadboardPlayerSchema = {
        "player": {
            "id": None,
            "firstName": None,
            "lastName": None,
            "amateur": None,
            "displayName": None,
            "country": None,
            "shortName": None
        },
        "scoringData": {
            "position": None,
            "total": None,
            "thru": None,
            "score": None,
            "courseId": None,
            "groupNumber": None,
            "currentRound": None,
            "rounds": {
                "1": None,
                "2": None,
                "3": None,
                "4": None
            },
            "movementDirection": None,
            "movementAmount": None,
            "playerState": None,
            "rankingMovement": None,
            "rankingMovementAmount": None,
            "totalStrokes": None,
            "official": None,
            "projected": None,
            "roundStatus": None
        },
        "tournamentName": None,
        "scorecard_id": None,
        "currentHole": None,
        "rounds": {
            "All": {
                "round": 1,
                "displayName": None,
                "performance": {
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "1": {
                "round": 1,
                "displayName": None,
                "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None,
                    "tourcastURL": None
                },
                "holes": {
                    "1": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "2": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "3": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "4": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "5": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "6": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "7": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "8": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "9": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "10": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "11": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "12": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "13": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "14": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "15": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "16": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "17": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "18": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    }
                },
                "performance": {
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:Total": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Long": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SandSaves": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Scrambling": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "PuttsPerGIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "FeetOfPuttsMade": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }                
                },
                "scoring": {
                    "Eagles": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "2": {
                "round": 2,
                "displayName": None,
                "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None,
                    "tourcastURL": None
                },
                "holes": {
                    "1": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "2": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "3": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "4": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "5": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "6": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "7": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "8": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "9": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "10": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "11": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "12": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "13": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "14": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "15": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "16": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "17": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "18": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    }
                },
                "performance": {
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:Total": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Long": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SandSaves": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Scrambling": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "PuttsPerGIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "FeetOfPuttsMade": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "3": {
                "round": 3,
                "displayName": None,
                "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None,
                    "tourcastURL": None
                },
                "holes": {
                    "1": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "2": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "3": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "4": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "5": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "6": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "7": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "8": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "9": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "10": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "11": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "12": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "13": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "14": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "15": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "16": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "17": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "18": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    }
                },
                "performance": {
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:Total": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Long": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SandSaves": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Scrambling": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "PuttsPerGIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "FeetOfPuttsMade": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "4": {
                "round": 4,
                "displayName": None,
                "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None,
                    "tourcastURL": None
                },
                "holes": {
                    "1": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "2": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "3": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "4": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "5": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "6": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "7": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "8": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "9": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "10": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "11": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "12": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "13": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "14": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "15": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "16": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "17": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    },
                    "18": {
                        "par": None,
                        "score": None,
                        "sequenceNumber": None,
                        "status": None,
                        "yardage": None,
                        "roundScore": None
                    }
                },
                "performance": {
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:Total": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Long": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "SandSaves": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Scrambling": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "PuttsPerGIR": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "FeetOfPuttsMade": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "rank": None,
                        "total": None,
                        "yearToDate": None
                    }
                }
            }
        }
    }

    leadboardPlayerSchemaSimple = {
        "player": {
            "id": None,
            "firstName": None,
            "lastName": None,
            "amateur": None,
            "displayName": None,
            "country": None,
            "shortName": None
        },
        "scoringData": {
            "position": None,
            "total": None,
            "thru": None,
            "score": None,
            "courseId": None,
            "groupNumber": None,
            "currentRound": None,
            "rounds": {
                "1": None,
                "2": None,
                "3": None,
                "4": None
            },
            "playerState": None,
            "totalStrokes": None,
            "projected": None,
            "roundStatus": None
        },
        "rounds": {
            "All": {
                "round": 1,
                "displayName": None,
                "performance": {
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "1": {
                "round": 1,
                "displayName": None,
                "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None
                },
                "performance": {
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "2": {
                "round": 2,
                "displayName": None,
                "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None
                },
                "performance": {
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "3": {
                "round": 3,
                "displayName": None,
                "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None
                },
                "performance": {
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "total": None,
                        "yearToDate": None
                    }
                }
            },
            "4": {
                "round": 4,
                "displayName": None,
                 "courseInfo": {
                    "courseId": None,
                    "courseName": None,
                    "groupNumber": None,
                    "parTotal": None,
                    "total": None,
                    "scoreToPar": None
                },
               "performance": {
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:APP": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:OTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:ARG": {
                        "total": None,
                        "yearToDate": None
                    },
                    "SG:PUTT": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DA": {
                        "total": None,
                        "yearToDate": None
                    },
                    "DD": {
                        "total": None,
                        "yearToDate": None
                    },
                    "GIR": {
                        "total": None,
                        "yearToDate": None
                    }
                },
                "scoring": {
                    "Eagles": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Birdies": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Pars": {
                        "total": None,
                        "yearToDate": None
                    },
                    "Bogeys": {
                        "total": None,
                        "yearToDate": None
                    }
                }
            }
        }
    }

    active_schema = leadboardPlayerSchema
    if schema_type == 'simple':
        active_schema = leadboardPlayerSchemaSimple
    elif schema_type == 'full':
        active_schema = leadboardPlayerSchema


    stat_mappings = {
        'SG: Off The Tee': 'SG:OTT',
        'SG: Approach to Green': 'SG:APP',
        'SG: Around The Green': 'SG:ARG',
        'SG: Putting': 'SG:PUTT',
        'Driving Accuracy': 'DA',
        'Driving Distance': 'DD',
        'Longest Drive': 'Long',
        'Greens in Regulation': 'GIR',
        'Sand Saves': 'SandSaves',
        'Scrambling': 'Scrambling',
        'Putts per GIR': 'PuttsPerGIR',
        'Feet of Putts Made': 'FeetOfPuttsMade',
        'Eagles': 'Eagles',
        'Birdies': 'Birdies',
        'Pars': 'Pars',
        'Bogeys': 'Bogeys'
    }
    stat_mapping_ids = {
        '02567': 'SG:OTT',
        '02568': 'SG:APP',
        '02569': 'SG:ARG',
        '02564': 'SG:PUTT',
        '102': 'DA',
        '101': 'DD',
        '159': 'Long',
        '103': 'GIR',
        '111': 'SandSaves',
        '130': 'Scrambling',
        '104': 'PuttsPerGIR',
        '438': 'FeetOfPuttsMade',
        '106': 'Eagles',
        '107': 'Birdies',
        '1005': 'Pars',
        '1002': 'Bogeys'
    }

    # Now fill out the schema object with values from player if they exist in the object
    for key in active_schema.keys():
        if key == 'player' and 'player' in player:
            for player_key in active_schema[key].keys():
                if player_key in player[key]:
                    active_schema[key][player_key] = player[key][player_key]
        elif key == 'scoringData' and 'scoringData' in player:
            for scoring_key in active_schema[key].keys():
                if scoring_key == 'rounds':
                    if scoring_key in player[key]:
                        for i, round_score in enumerate(player[key][scoring_key]):
                            active_schema[key][scoring_key][str(i+1)] = round_score
                elif scoring_key in player[key]:
                    active_schema[key][scoring_key] = player[key][scoring_key]
        elif key == 'tournamentName' and 'tournamentName' in scorecard:
            active_schema[key] = scorecard['tournamentName']
        elif key == 'scorecard_id' and 'id' in scorecard:
            active_schema[key] = scorecard['id']
        elif key == 'current_hole' and 'current_hole' in scorecard:
            active_schema[key] = scorecard['current_hole']
        elif key == 'rounds' and 'rounds' in stats:
            for i, round_stats in enumerate(stats['rounds']):
                round_value = str(round_stats['round'])
                if round_value == '-1':
                    round_value = 'All'
                if round_value in active_schema[key]:
                    for round_key in active_schema[key][round_value].keys():
                        if round_key == 'performance' and 'performance' in round_stats:
                            for j, stat in enumerate(round_stats['performance']):
                                if 'statId' in stat:
                                    stat_id = str(stat['statId'])
                                    if stat_id in stat_mapping_ids:
                                        stat_label_id = stat_mapping_ids[stat_id]
                                        if stat_label_id in active_schema[key][round_value][round_key]:
                                            for stat_key in active_schema[key][round_value][round_key][stat_label_id].keys():
                                                if stat_key in stat:
                                                    active_schema[key][round_value][round_key][stat_label_id][stat_key] = stat[stat_key]
                        elif round_key == 'scoring' and 'scoring' in round_stats:
                            for j, stat in enumerate(round_stats['scoring']):
                                if 'statId' in stat:
                                    stat_id = str(stat['statId'])
                                    if stat_id in stat_mapping_ids:
                                        stat_label_id = stat_mapping_ids[stat_id]
                                        if stat_label_id in active_schema[key][round_value][round_key]:
                                            for stat_key in active_schema[key][round_value][round_key][stat_label_id].keys():
                                                if stat_key in stat:
                                                    active_schema[key][round_value][round_key][stat_label_id][stat_key] = stat[stat_key]
                        elif round_key == "courseInfo" or round_key == "holes":
                            if "roundScores" in scorecard:
                                round_scores = scorecard['roundScores']
                                for j, round_score in enumerate(round_scores):
                                    if str(round_score['roundNumber']) == round_value:
                                        if round_key == "holes":
                                            this_hole = str(round_score_key)
                                            if 'firstNine' in round_score:
                                                if 'holes' in round_score['firstNine']:
                                                    for hole in round_score['firstNine']['holes']:
                                                        hole_num = str(hole['holeNumber'])
                                                        if hole_num in active_schema[key][round_value][round_key]:
                                                            for hole_key in active_schema[key][round_value][round_key][hole_num].keys():
                                                                if hole_key in hole:
                                                                    active_schema[key][round_value][round_key][hole_num][hole_key] = hole[hole_key]
                                        elif round_key == "courseInfo":
                                            for round_score_key in active_schema[key][round_value][round_key].keys():
                                                if round_score_key in round_score:
                                                    active_schema[key][round_value][round_key][round_score_key] = round_score[round_score_key]
                        elif round_key in round_stats:
                            active_schema[key][round_value][round_key] = round_stats[round_key]

            for round_key in active_schema[key].keys():
                if round_key in player:
                    active_schema[key][round_key] = player[round_key]
        else:
            print('Key not found in schema: ' + key)

    return active_schema

