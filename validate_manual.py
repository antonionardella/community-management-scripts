
import time
import random
from tools import (get_zealy_api_data, logger, subdomain, x_api_key,
                   validate_zealy_api_data)

def get_quest_and_review(quest_id):
    """
    It repeatedly polls the Zealy API for new submissions in
    the quests that require manual validation and marks them as valid.
    """
    quest_completers = get_zealy_api_data(
        subdomain,
        x_api_key,
        quest_id,
        status="pending"
        )
    
    valid_quest_ids = []
    
    if not quest_completers:
        time.sleep(random.randint(6, 9) * 10)
        return

    # Iterate over submissions and validate shimmer addresses
    for item in quest_completers['data']:
        quest_submission_id = item['id']
        valid_quest_ids.append(quest_submission_id)

    # Make post request to the API
    if valid_quest_ids:
        # Give a random comment from the list
        comments = [
            "Thanks",
            "Great!",
            "Awesome",
            "Ayee",
            "Arr",
            "Well done 🎉",
            "Fantastic 💯",
            "Excellent 👏",
            "Terrific 😍",
            "Impressive 🤩",
            "Outstanding 🙌",
            "You rock 🤘",
            "Outstanding",
            "Excellent",
            "Impressive",
            "Fantastic",
            "Superb"
            ]
        comment = random.choice(comments)
        status = "success"
        valid_data = validate_zealy_api_data(
            subdomain,
            x_api_key,
            valid_quest_ids,
            status,
            comment
            )
        logger.debug(valid_data)

    # Wait for a random time between 60 and 90 seconds before polling again
    time.sleep(random.randint(6, 9) * 10)

# List of quest IDs that would require manual validation
quest_ids = ['d4967c9c-92b9-49c5-8ff7-bf78b43feb6b', 'e3bffb56-1040-4bb2-b35b-3aefd0675547', '75c73105-d8b7-4785-8569-2a48aadf573a', '7e59a1e5-91de-4aed-aa54-dcfdfea25e0b']

while True:
    for quest_id in quest_ids:
        logger.debug(f"quest id {quest_id}")
        get_quest_and_review(quest_id)
