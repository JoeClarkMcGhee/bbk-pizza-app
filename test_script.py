import datetime
import json
from datetime import datetime as dt

import requests


def test_case_runner(ip, test_cases):
    """
    We call a series of functions that each demonstrate a specific functionality. We dont make
    and assertions in the code as this could potential cause the programme to  terminate
    unexpectedly (assertions about API responses can be seen in the numerous test cases) rather
    we call on the user to enter "y" to cycle through the 20 different test cases and check the
    output themselves.

    NOTE: You can set the IP address in the `if __name__ == "__main__" block.
    """

    print(
        "\nThis app cycles through 20 test cases that demonstrate the Pizza API functionality.\n"
    )

    user_1 = input(
        "Enter (female) user name 1 or carriage return for default user 'Olga': "
    )
    if not user_1:
        user_1 = "Olga"
    user_2 = input(
        "Enter (male) user name 2 or carriage return for default user 'Nick': "
    )
    if not user_2:
        user_2 = "Nick"
    user_3 = input(
        "Enter (female) user name 3 or carriage return for default user 'Mary': "
    )
    if not user_3:
        user_3 = "Mary"
    user_4 = input(
        "Enter (male) user name 4 or carriage return for default user 'Nestor': "
    )
    if not user_4:
        user_4 = "Nestor"

    for idx, test in enumerate(test_cases):
        print(f"\n---- test case: {idx + 1} ----")
        test(ip, user_1, user_2, user_3, user_4)


def tc1(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1}, {user_2}, {user_3} and {user_4} register and are ready to access "
        f"the Pizza API.\n"
    )

    def create_users():
        for user in [user_1, user_2, user_3, user_4]:
            requests.post(
                url=f"{ip}create-user/",
                json={"username": user, "password": "password123"},
            )
            response = requests.get(url=f"{ip}users/{user}")
            print(
                f"Status code when retrieving details for {user}: {response.status_code}"
            )

    create_users()


def tc2(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1}, {user_2}, {user_3} and {user_4} use the oAuth v2 authorisation "
        f"service to register and get their tokens.\n"
    )

    print("SKIPPED")


def tc3(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1} makes a call to the API without using her token. This call should "
        f"be unsuccessful as the user is unauthorised.\n"
    )

    print("SKIPPED")


def tc4(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_1} posts a message in the Tech topic with an expiration time of now."
        f" After the end of the expiration time, the message will not accept any further user "
        f"interactions.\n"
    )

    # user_1 creates a post
    get_user_1 = requests.get(url=f"{ip}users/{user_1}")
    user_2_id = json.loads(get_user_1.content)["id"]
    data = {
        "expires_at": f"{dt.now()}",
        "author": user_2_id,
        "title": "My first post",
        "body": "A really long post body",
        "topics": ["Tech"],
    }
    create_post = requests.post(url=f"{ip}create-post", json=data)
    post_id = json.loads(create_post.content)["id"]

    # user_2 post a reaction against user_1's post
    get_user_2 = requests.get(url=f"{ip}users/{user_2}")
    user_2_id = json.loads(get_user_2.content)["id"]
    reaction = {
        "like_or_dislike": "Like",
        "comment": "I really like this post",
        "author": user_2_id,
        "post": post_id,
    }
    reaction = requests.post(url=f"{ip}add-reaction", json=reaction)

    print(
        "The post to 'add-reaction' should return a 400 as the post is no longer accepting "
        "request"
    )
    print(f"Status code of post to 'add-reaction': {reaction.status_code}")
    print(
        f"Returned message of post to 'add-reaction': "
        f"{json.loads(reaction.content)['non_field_errors'][0]}"
    )


def tc5(ip, user_1, user_2, user_3, user_4):
    # todo: need to add authentication

    print(
        f"TEST CASE: {user_2} posts a message in the Tech topic with an expiration time using his "
        "token.\n"
    )

    get_user_2 = requests.get(url=f"{ip}users/{user_2}")
    user_2_id = json.loads(get_user_2.content)["id"]
    data = {
        "expires_at": f"{dt.now() + datetime.timedelta(days=10)}",
        "author": user_2_id,
        "title": "My first post",
        "body": "A really long post body",
        "topics": ["Tech"],
    }
    post = requests.post(url=f"{ip}create-post", json=data)
    print(f"Status code of post: {post.status_code}")
    print(json.loads(post.content))


def tc6(ip, user_1, user_2, user_3, user_4):
    # todo: need to add authentication
    print(
        f"TEST CASE: {user_3} posts a message in the Tech topic with an expiration time using her "
        "token.\n"
    )

    get_user_3 = requests.get(url=f"{ip}users/{user_3}")
    user_3_id = json.loads(get_user_3.content)["id"]
    data = {
        "expires_at": f"{dt.now() + datetime.timedelta(days=10)}",
        "author": user_3_id,
        "title": "My first post",
        "body": "A really long post body",
        "topics": ["Tech"],
    }
    post = requests.post(url=f"{ip}create-post", json=data)
    print(f"Status code of post: {post.status_code}")
    print(json.loads(post.content))


def tc7(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} and {user_1} browse all the available posts in the Tech topic, "
        "there should be three posts available with zero likes, zero dislike and without and "
        "comments.\n"
    )


def tc8(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} and {user_1} 'like' {user_3}'s post in the Tech topic.\n"
    )


def tc9(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} 'likes' {user_2}'s post and 'dislikes' {user_3}'s post in the Tech "
        f"topic.\n"
    )


def tc10(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses all the available posts in the Tech topic; at this stage he "
        f"can see the number of likes and dislikes for each post ({user_3} has 2 likes and 1 "
        f"dislike and {user_2} has 1 like). There are not comments made yet.\n"
    )


def tc11(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} likes her post in the Tech topic. This call should be unsuccessful, "
        "as in Pizza a post owner cannot like their own messages.\n"
    )


def tc12(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} and {user_1} comment for {user_3}'s post in the Tech topic in a "
        f"round-robin fashion (on after the other adding at least 2 comments each).\n"
    )


def tc13(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses  all the available posts in the Tech topic; at this stage "
        f"he can see the number of like and dislikes of each post and the comments made.\n"
    )


def tc14(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} posts a message in the Health topic with an expiration time using "
        "her token.\n"
    )


def tc15(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} browses all the available posts in the Health topic; at this stage "
        f"she can only {user_4}'s post.\n"
    )


def tc16(ip, user_1, user_2, user_3, user_4):
    print(f"TEST CASE: {user_3} comments on {user_4}'s post in the Health topic.\n")


def tc17(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_3} dislikes {user_4}'s message in the Health topic after the end of "
        f"the post expiration time. This should fail.\n"
    )


def tc18(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} broses all the messages in the Health topic. There should be only "
        f"one post (his own) with one comment ({user_3}'s).\n"
    )


def tc19(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_2} browses all the expired messages in the Sport topic. These should "
        f"be empty.\n"
    )


def tc20(ip, user_1, user_2, user_3, user_4):
    print(
        f"TEST CASE: {user_4} queries fo an active post having the highest interest (maximum sum "
        f"of like and dislikes in the Tech topic. This should be {user_3}'s post.\n"
    )


if __name__ == "__main__":
    IP = "http://127.0.0.1:8000/"
    TEST_CASES = [value for key, value in globals().items() if key.startswith("tc")]
    test_case_runner(IP, TEST_CASES)
