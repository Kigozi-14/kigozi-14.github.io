import requests

def my_data(my_name):
    
    lis = []

    # Define the endpoint and headers for the request
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"  # This is just an example, use your own user agent or any generic one
    }

    # Define the query and the variables to be sent in the request
    username = my_name
    data = {
        "query": """
        query userProblemsSolved($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                problemsSolvedBeatsStats {
                    difficulty
                    percentage
                }
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """,
        "variables": {
            "username": username
        }
    }

    # Make the POST request to the LeetCode GraphQL API
    response = requests.post(url, json=data, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()

    # Check if matchedUser and submitStatsGlobal are not None
    matched_user = response_data.get('data', {}).get('matchedUser', None)
    if matched_user and matched_user.get('submitStatsGlobal', None):
        ac_submission_num = matched_user['submitStatsGlobal'].get('acSubmissionNum', None)
        if ac_submission_num:
            total_solved = next((item['count'] for item in ac_submission_num if item['difficulty'] == 'All'), 0)
            easy_solved = next((item['count'] for item in ac_submission_num if item['difficulty'] == 'Easy'), 0)
            medium_solved = next((item['count'] for item in ac_submission_num if item['difficulty'] == 'Medium'), 0)
            hard_solved = next((item['count'] for item in ac_submission_num if item['difficulty'] == 'Hard'), 0)
            lis.append(easy_solved)
            lis.append(medium_solved)
            lis.append(hard_solved)
            lis.append(total_solved)
            return lis


